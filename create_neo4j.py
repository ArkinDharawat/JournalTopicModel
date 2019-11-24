import os

import pandas as pd
import yaml
from py2neo import Graph,  Node, Relationship

with open(os.path.join(os.getcwd(), "config_neo.yml"), 'r') as stream:
    config = yaml.safe_load(stream)

model_folder = "/Users/arkin/Desktop/CS411/project/data"

graph = Graph(auth=(config["user"], config["password"]))

journal_df = pd.read_csv(os.path.join(model_folder, "journalslist.csv"))
papers_df = pd.read_csv(os.path.join(model_folder, "AllArticles_Subset.csv"))

import code
code.interact(local={**locals(), **globals()})

