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
        journal_node = Node("Journal", name=name, id=id, field=field, ranking=ranking)
        graph.create(journal_node)


def add_paper_nodes():
    pass

add_journal_nodes()
import code
code.interact(local={**locals(), **globals()})
