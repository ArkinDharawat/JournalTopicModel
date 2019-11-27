import os

import pandas as pd
import yaml
from py2neo import Graph, Node, Relationship

with open(os.path.join(os.getcwd(), "config_neo.yml"), 'r') as stream:
    config = yaml.safe_load(stream)

class Neo4JQuery():
    def __init__(self, k):
        self.topics = k
        self.graph = Graph(auth=(config["user"], config["password"]))


    def get_recommended_papers(self, top_k):
        query = """ 
                // get target user and their neighbors pairs and count // of distinct movies that they have rented in common 
                MATCH (p1:Paper)-[:RENTED]->(t:Topic)<-[:RENTED]-(p2:Paper) 
                WHERE p1 <> p2 AND p1.customerID = {cid} 
                WITH p1, p2, COUNT(DISTINCT t) as intersection 
                
                // get count of all the distinct movies that they have rented in total (Union) 
                MATCH (p:Paper)-[:RENTED]->(t:Topic) 
                WHERE p in [p1, p2] WITH p1, p2, intersection, COUNT(DISTINCT t) as union 
                
                // compute Jaccard index 
                WITH p1, p2, intersection, union, (intersection * 1.0 / union) as jaccard_index 
                
                // get top k nearest neighbors based on Jaccard index 
                ORDER BY jaccard_index DESC, p2.id 
                WITH p1, COLLECT([p2.id, jaccard_index, intersection, union])[0..{k}] as neighbors WHERE SIZE(neighbors) = {k}   
                
                // return users with enough neighbors 
                RETURN p1.id as id, neighbors 
            """
        x = -1
        for i in self.graph.cypher.execute(query, cid=int(x), k=int(top_k)):
            print(i)


if __name__ == '__main__':
    neo_obj = Neo4JQuery(10)

