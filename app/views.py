import os

import yaml
from SQLQueries.SQLStrQuery import SQLStrQuery
from Neo4jQueries.Neo4jQuery import Neo4jQuery
from TopicModel.TextProcessor import remove_non_ascii
from TopicModel.TopicExtractor import TopicModel
from app import app
from flask import request, render_template, g

INSERT = "Insert"
DELETE = "Delete"
UPDATE = "Update"
SEARCH = "Search"
RECOMMEND = "Recommend"


@app.before_first_request
def before_first_request_func():
    db_type = app.config.get('DB_TYPE')
    if db_type not in ["sql", "neo"]:
        app.config["DB_TYPE"] = "sql"  # Default config database in SQL
        app.config["AUTH_FILE"] = "config.yml"
    print(app.config.get('DB_TYPE'), app.config.get('AUTH_FILE'))


@app.before_request
def before_request_func():
    g.db_type = app.config.get('DB_TYPE')  # Database type
    auth_file_path = app.config.get('AUTH_FILE')  # File name of database credentials

    with open(os.path.join(os.getcwd(), auth_file_path), 'r') as stream:
        config = yaml.safe_load(stream)

    if g.db_type == "sql":
        g.DatabaseObj = SQLStrQuery(10, config)  # Create the database interface object
    else:
        g.DatabaseObj = Neo4jQuery(10, config)

    g.TopicModelobj = TopicModel(
        os.path.join(os.path.expanduser('~'), "../project/data/"))  # Load topic model with correct files
    g.default = ''  # Default value of page field


# static url
@app.route('/')
def index():
    return render_template('index.html')  # Index Page


@app.route('/query', methods=['POST'])
def insert_endpoint():
    """ Run the query and return the result.
    Returns: render_template to render the HTML page
    """
    action = str(request.form.get('action'))

    if action == INSERT:
        return insert_data(request)
    elif action == DELETE:
        return delete_data(request)
    elif action == UPDATE:
        return update_data(request)
    elif action == SEARCH:
        return search_data(request)
    elif action == RECOMMEND:
        return recommend_data(request)


def insert_data(request):
    """ Insert data into the database
    Args:
        request: request object from the form
    Returns: render_template with error-string or output-string
    """
    DatabaseObj = g.DatabaseObj  # Get database object
    TopicModelobj = g.TopicModelobj  # Get topic model

    paper_id = str(request.form['paper_id'])  # convert all fields to strings
    authors = str(request.form['authors'])
    title = str(request.form['title'])
    abstract = str(request.form['abstract'])
    journal_id = str(request.form['journal_id'])

    default = g.default
    if g.db_type == "neo" and paper_id != default:
        paper_id = int(request.form['paper_id'])  # Neo4J driver needs ints
        journal_id = int(request.form['journal_id'])

    title = remove_non_ascii(title)  # clean up title
    abstract = remove_non_ascii(abstract)  # clean up abstract

    insert_paper_query = DatabaseObj.insert_paper()  # returns insert_paper query-string

    topics = TopicModelobj.get_topics(title=title, abstract=abstract)  # returns topic vector for title & abstract

    insert_topic_query = DatabaseObj.insert_topic(paper_id, topics)  # returns insert_topic query-string
    query_bool, result = DatabaseObj.execute_query(insert_paper_query, [paper_id, authors, journal_id, title, abstract])
    # executes query and returns (Bool, Cursor)
    if not query_bool:
        return render_template("error_response.html", error_str=str(result))  # render Error template

    query_bool, result = DatabaseObj.execute_query(insert_topic_query)
    if not query_bool:
        return render_template("error_response.html", error_str=str(result))

    return render_template('insert_successful.html')  # render successful insertion template


def delete_data(request):
    """ Delete data in the database
    Args:
        request: request object from the form
    Returns: render_template with error-string or output-string
    """
    DatabaseObj = g.DatabaseObj
    default = g.default

    paper_id = str(request.form['paper_id'])
    if g.db_type == "neo" and paper_id != default:
        paper_id = int(request.form['paper_id'])

    delete_paper_query = DatabaseObj.delete_paper()
    delete_topic = DatabaseObj.delete_topic()

    query_bool, result = DatabaseObj.execute_query(delete_topic, [paper_id])
    if not query_bool:
        return render_template("error_response.html", error_str=str(result))

    query_bool, result = DatabaseObj.execute_query(delete_paper_query, [paper_id])
    if not query_bool:
        return render_template("error_response.html", error_str=str(result))

    return render_template('delete_successful.html')


def filter_update_data(request):
    """ Return data map between update field and update value
    Args:
        request: request object from the form
    Returns: Dictionary mapping field->value
    """
    default = g.default
    data_map = {}

    authors = str(request.form['authors'])
    if authors != default:
        data_map["authors"] = authors  # Do not map field -> value if field is blank

    title = str(request.form['title'])
    if title != default:
        data_map["title"] = title

    abstract = str(request.form['abstract'])
    if abstract != default:
        data_map["abstract"] = abstract

    journal_id = str(request.form['journal_id'])
    if journal_id != default:
        data_map["journal_id"] = journal_id

    return data_map


def update_data(request):
    """ Update data in the database
    Args:
        request: request object from the form
    Returns: render_template with error-string or output-string
    """
    DatabaseObj = g.DatabaseObj
    default = g.default

    paper_id = str(request.form['paper_id'])
    if g.db_type == "neo" and paper_id != default:
        paper_id = int(request.form['paper_id'])

    data_map = filter_update_data(request)
    column = []
    data = []
    for col in data_map:
        column.append(col)
        data.append(data_map[col])
    data.append(paper_id)

    # TODO: Add Update for Topics if title/abstract updated
    if column != [] and data != []:
        update_query = DatabaseObj.update_paper(column)
        query_res, err = DatabaseObj.execute_query(update_query, data)

        if not query_res:
            return render_template("error_response.html", error_str=str(err))

    return render_template('update_successful.html')


def search_data(request):
    """ Search for data in the database
    Args:
        request: request object from the form
    Returns: render_template with error-string or output-string
    """
    DatabaseObj = g.DatabaseObj
    default = g.default

    paper_id = str(request.form['paper_id'])
    authors = str(request.form['authors'])
    journal_id = str(request.form['journal_id'])

    if paper_id == default and authors == default and journal_id == default:
        return render_template("error_response.html", error_str=str("Cannot Search For Result"))
    elif authors != default:
        # Note: We execute the query here manually since this was more convient
        if g.db_type == "neo":
            query_str = "MATCH (p:Paper) WHERE p.authors=~ '.*" + authors + ".*' RETURN p.id, p.authors, p.journal_id, p.title", []
        else:
            query_str = 'SELECT * FROM Academic_Paper WHERE Authors LIKE "%' + authors + '%";'

        query_bool, result = DatabaseObj.execute_query(query_str, commit=False)
        if not query_bool:
            return render_template("error_response.html", error_str=str(result))

    elif journal_id != default:
        if g.db_type == "neo":
            journal_id = int(journal_id)  # Neo4j can't take strs

        search_journal = DatabaseObj.search_journal()
        query_bool, result = DatabaseObj.execute_query(search_journal, [journal_id], False)
        if not query_bool:
            return render_template("error_response.html", error_str=str(result))
        results = DatabaseObj.get_results(result)
        return render_template("search_result_journal.html", results=results)

    elif paper_id != default:
        if g.db_type == "neo":
            paper_id = int(paper_id)

        search_paper = DatabaseObj.search_paper()
        query_bool, result = DatabaseObj.execute_query(search_paper, [paper_id], False)
        if not query_bool:
            return render_template("error_response.html", error_str=str(result))
    else:
        return render_template("error_response.html", error_str=str("Nothing Searched For"))

    results = DatabaseObj.get_results(result)  # Parse returned results from cursor.
    return render_template("search_results.html", results=results)


def recommend_data(request):
    """ Recommend data in the database
    Args:
        request: request object from the form
    Returns: render_template with error-string or output-string
    """
    DatabaseObj = g.DatabaseObj
    TopicModelobj = g.TopicModelobj
    default = g.default

    paper_id = str(request.form['paper_id'])
    authors = str(request.form['authors'])
    title = str(request.form['title'])
    abstract = str(request.form['abstract'])
    journal_id = str(request.form['journal_id'])

    if title != default and abstract != default:
        title = remove_non_ascii(title)
        abstract = remove_non_ascii(abstract)

        topics = TopicModelobj.get_topics(title=title, abstract=abstract)
        # Topic model functions differ between Neo4J and SQL
        if g.db_type == "neo":
            topic_vec = [int(x) for x in DatabaseObj.construct_topic_vector(topics)]
            get_top_recommendations = DatabaseObj.get_recommended_papers()

            query_bool, result = DatabaseObj.execute_query(get_top_recommendations, [
                topic_vec])  # single query to calculate and rank recoomended papers
            if not query_bool:
                return render_template("error_response.html", error_str=str(result))
        else:
            query_bool, result = DatabaseObj.execute_topic_proc(topics)  # execute the stored procedure in case of SQL
            if not query_bool:
                return render_template("error_response.html", error_str=str(result))

            get_top_recommendations = DatabaseObj.get_recommended_papers(
                top_k=10)  # get SQL query to grab the recommended papers

            query_bool, result = DatabaseObj.execute_query(get_top_recommendations, [], False)
            if not query_bool:
                return render_template("error_response.html", error_str=str(result))
    else:
        return render_template("error_response.html", error_str="Cannot Recommend Any Articles. Try Search")

    results = DatabaseObj.get_results(result)
    return render_template("reco_results.html", results=results)


@app.after_request
def after_request_func(response):
    g.DatabaseObj.close_db()
    return response
