import os

import pandas as pd
import yaml
from py2neo import Graph, Node, Relationship

with open(os.path.join(os.getcwd(), "config_neo.yml"), 'r') as stream:
    config = yaml.safe_load(stream)

graph = Graph(auth=(config["user"], config["password"]))


def add_journal_nodes():
    journal_df = pd.read_csv(os.path.join(os.path.expanduser('~'), "../project/data/journalslist.csv"))
    journal_rankings = pd.read_csv(os.path.join(os.path.expanduser('~'), "../project/data/JournalIdRankings.csv"))

    for id, row in journal_df.iterrows():
        name, id, field = row.values
        ranking = journal_rankings[journal_rankings["journal_id"] == id]["ranking"].values
        if len(ranking) == 0:
            ranking = -1
        else:
            ranking = ranking[0]
        # print(name, id, field, ranking)
        journal_node = Node("Journal", name=name, id=int(id), field=field, ranking=int(ranking))
        graph.create(journal_node)


def add_paper_nodes():
    articles_df = pd.read_csv(os.path.join(os.path.expanduser('~'), "../project/data/AllArticles_Subset.csv"))
    for id, row in articles_df.iterrows():
        title, author, url, abstract, journal_id = row.values
        paper_node = Node("Paper", title=title, id=int(id), authors=author, abstract=abstract)
        graph.create(paper_node)
        journal_node = graph.nodes.match("Journal", id=int(journal_id)).first()
        graph.create(Relationship(paper_node, "PUBLISHED", journal_node))


def update_paper_nodes():
    articles_df = pd.read_csv(os.path.join(os.path.expanduser('~'), "../project/data/AllArticles_Subset.csv"))
    for id, row in articles_df.iterrows():
        title, author, url, abstract, journal_id = row.values
        dict = {"id": int(id), "journal_id": int(journal_id)}
        output = graph.run("MATCH (p:Paper) WHERE p.id={idim} SET p.journal_id={journal_id}", dict).evaluate()


def add_topic_nodes(k=10):
    # Add topic nodes
    # topic_nodes = [Node("Topic", no=int(x)) for x in range(k)]
    # for topic_node in topic_nodes:
    #     graph.create(topic_node)

    topic_df = pd.read_csv(os.path.join(os.path.expanduser('~'), "../project/data/id_topic.csv"))
    for id, row in topic_df.iterrows():
        vals = row.values
        index = vals[0]
        if index < 2180:
            continue

        for i in range(1, len(vals)):
            r = 0
            if vals[i] == 1:
                r = 1
            query = "MATCH (p:Paper),(t:Topic) WHERE p.id={id} AND t.no={no} MERGE (p)-[r:TopicOf {score:{s}}]->(t)"
            graph.run(query, {"id": int(index), "no": int(i - 1), "s": int(r)})
        print(index)


# def update_topic_rel():
#     topic_df = pd.read_csv(os.path.join(os.path.expanduser('~'), "../project/data/id_topic.csv"))
#     for id, row in topic_df.iterrows():
#         vals = row.values
#         index = vals[0]
#
#         for i in range(1, len(vals)):
#             r = 0
#             if vals[i] == 1:
#                 r = 1
#             query = "MATCH (a:Paper {id: {id}})-[r:TopicOf]->(t:Topic {no: {no}}) SET r.score = {s}"
#             graph.run(query, {"id": int(index), "no": int(i - 1), "s": int(r)})


# add_journal_nodes()
# add_paper_nodes()
add_topic_nodes()
# update_paper_nodes()
# Exmaplee query: d = graph.run("MATCH (p:Paper)-[:PUBLISHED]->(j:Journal {id:1}) RETURN p.title").data()
