import os

import pandas as pd
import yaml
from py2neo import Graph,  Node, Relationship

with open(os.path.join(os.getcwd(), "config_neo.yml"), 'r') as stream:
    config = yaml.safe_load(stream)

graph = Graph(auth=(config["user"], config["password"]))

journal_df = pd.read_csv(os.path.join(os.path.expanduser('~'), "../project/data/journalslist.csv"))
papers_df = pd.read_csv(os.path.join(os.path.expanduser('~'), "../project/data/AllArticles_Subset.csv"))

import code
code.interact(local={**locals(), **globals()})

