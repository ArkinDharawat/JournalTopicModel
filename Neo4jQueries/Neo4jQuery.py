from py2neo import Graph, Node, Relationship


class Neo4jQuery(object):
    def __init__(self, k, config):
        self.num_topics = k
        self.config = config
        self.graph = Graph(auth=(config["user"], config["password"]))

    def construct_topic_vector(self, topic_indices):
        value_str = ["0"] * self.num_topics
        for k in topic_indices:
            value_str[k - 1] = "1"
        return value_str

    def insert_journal(self):
        return "CREATE (j:Journal {id:{id}, name:{name}, field:{field}, ranking:{ranking})", ["id", "name", "field",
                                                                                              "ranking"]

    def insert_paper(self):
        return "CREATE (p:Paper {id:{id}, authors:{authors}, journal_id:{journal_id}, title:{title}, abstract:{abstract}})", [
            "id", "authors", "journal_id", "title", "abstract"]

    def insert_topic(self, paper_id, topic_indices):
        paper_topic_rel_str = "MATCH (p:Paper), (t:Topic) WHERE p.id={0} AND t.no IN [{1}] CREATE (p)-[:TopicOf]->(t)"
        value_str = self.construct_topic_vector(topic_indices)
        topic_nodes = []
        for i in range(len(value_str)):
            if value_str[i] == "1":
                topic_nodes.append(str(i))
        query_str = paper_topic_rel_str.format(paper_id, ','.join(topic_nodes))
        return query_str, []

    def delete_paper(self):
        return "MATCH (p:Paper) WHERE p.id={id} DETACH DELETE p", ["id"]  # Deletes nodes and all edges

    def delete_topic(self):
        return "", []  # Empty bc delete_paper handles it

    def search_journal(self):
        return "MATCH (p:Paper) WHERE p.journal_id={id} RETURN p.id, p.authors, p.journal_id, p.title", ["id"]

    def search_paper(self):
        return "MATCH (p:Paper) WHERE p.id={id} RETURN p.id, p.authors, p.journal_id, p.title", ["id"]

    def search_authors(self):
        return "MATCH (p:Paper) WHERE p.authors=~ '.*{authors}.*' RETURN p.id, p.authors, p.journal_id, p.title", [
            "authors"]

    def get_recommended_papers(self):
        query = "MATCH (j:Journal)<-[pub1:PUBLISHED]-(p1:Paper)-[r1:TopicOf]->(Topic) WHERE p1.id < 3000 " \
                "WITH p1 AS p1, j AS j, algo.similarity.cosine({topic_vec}, collect(r1.score)) AS similarity " \
                "RETURN  p1.id, similarity " \
                "ORDER BY similarity DESC, j.ranking LIMIT 10;"

        return query, ["topic_vec"]

    def execute_query(self, query_str, args=[], commit=True):
        tx = self.graph.begin()
        query_str, keys = query_str

        if len(query_str) == 0:
            return True, None  # No Query to execute

        if len(keys) == 0:
            assign_dict = {}
        else:
            assign_dict = dict(zip(keys, args))

        try:
            cursor = tx.run(query_str, assign_dict)
            tx.commit()
        except Exception as e:
            print("Error :" + str(e))
            return False, e

        return True, cursor

    def close_db(self):
        return  # py2neo use a REST API


if __name__ == '__main__':
    import os
    import yaml

    with open(os.path.join(os.getcwd(), "config_neo.yml"), 'r') as stream:
        config = yaml.safe_load(stream)

    obj = Neo4jQuery(10, config)
    topic_vec = [0, 1, 0, 1, 0, 0, 1, 0, 1, 1]
    import code

    code.interact(local={**locals(), **globals()})
