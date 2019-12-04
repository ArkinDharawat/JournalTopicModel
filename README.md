# Scientific Paper Recommendation System
CS 411 Final Project
Version 1.1.0
### Repository description
1. [Neo4JQueries](Neo4jQueries): Class for the Neo4J queries and Neo4J driver.
2. [SQLQueries](SQLQueries): Class for the SQL queries and SQL driver.
3. [TopicModel](TopicModel): Library for pre-processing and extracting relevant topics from text. Can also be used to train topic model new corpus.
4. [app](app): Flask application with templates and views. 
5. [scripts](scripts): Scripts used to load data into the databases and perform other miscellaneous tasks.  
6. `config.py`: Configuration file used by the server to access the database of your choice.
    If you want to use a SQL database use:
    ```python
    DB_TYPE="sql"
    AUTH_FILE="config.yml"
    ```
    If you want to use Neo4J database use:
    ```python
    DB_TYPE="neo"
    AUTH_FILE="config_neo.yml"
    ```
7. `requirements.txt`: Required python libraries for running the server
8. `run.py`: Script to run the server. However we suggest another way to run it, See Below.

### How To Run
1. You first need to have a `config.yml` or `config_nep.yml` if you want to use a SQL/ Neo4J database respectively.
   The files must have the following format:
   ```yaml
    user: 
    password: 
    host: 
    database: 
    ```
2. Make sure you have the model files for using the Gensim topic model. They should be present in the folder and provided 
   to the `TopicExtractor` class in `views.py`

3. Run the command `flask run -host=0.0.0.0` in the repository to start the server. 
    
### [Project Report](https://drive.google.com/file/d/17RjdVVvUDzoNn1tZOC4_onLCtGK6Zf_F/view)