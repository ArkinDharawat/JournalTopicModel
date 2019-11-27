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


def add_topic_nodes(k=10):
    # Add topic nodes
    topic_nodes = [Node("Topic", no=int(x)) for x in range(k)]
    for topic_node in topic_nodes:
        graph.create(topic_node)

    topic_df = pd.read_csv(os.path.join(os.path.expanduser('~'), "../project/data/id_topic.csv"))
    for id, row in topic_df.iterrows():
        vals = row.values
        index = vals[0]
        paper_node = graph.nodes.match("Paper", id=int(index)).first()
        import code
        code.interact(local={**locals(), **globals()})
        for i in range(1, len(vals)):
            if vals[i] == 1:
                topic_node = graph.nodes.match("Topic", id=int(i-1)).first()
                graph.create(Relationship(paper_node, "TopicOf", topic_node))




# add_journal_nodes()
# add_paper_nodes()
add_topic_nodes()
# Exmaplee query: d = graph.run("MATCH (p:Paper)-[:PUBLISHED]->(j:Journal {id:1}) RETURN p.title").data()