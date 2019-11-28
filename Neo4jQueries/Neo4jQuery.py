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
        return "CREATE (p:Paper {id:{id}, authors:{authors}, journal_Id:{journal_id}, title:{title}, abstract:{abstract}})", [
            "id", "authors", "journal_id", "title", "abstract"]

    def insert_topic(self, paper_id, topic_indices):
        paper_topic_rel_str = "MATCH (p:Paper), (t:Topic) WHERE p.id={0} AND t.no={1} CREATE (p)-[:TopicOf]->(t)"
        value_str = self.construct_topic_vector(topic_indices)
        query_str = []
        for i in range(len(value_str)):
            if value_str == "1":
                query_str.append(paper_topic_rel_str.format(paper_id, i))

        return ';'.join(query_str)  # TODO: Check if we can use this to execute multple queries

    def delete_paper(self):
        return "MATCH (p:Paper) WHERE p.id={id} DETACH DELETE p", ["id"]

    def search_journal(self):
        return "MATCH (p:Paper) WHERE p.journal_id={id} RETURN p", ["id"]

    def search_paper(self):
        return "MATCH (p:Paper) WHERE p.id={id} RETURN p", ["id"]

    def search_authors(self):
        return "MATCH (p:Paper) WHERE p.authors=~ '.*{authors}.*' RETURN p", ["authors"]

    def execute_query(self, query_str, args=[], commit=True):
        query_str, keys = query_str
        if len(keys) == 0:
            assign_dict = {}
        else:
            assign_dict = dict(zip(keys, args))
        try:
            output = self.graph.run(query_str, assign_dict).evaluate()
        except Exception as e:
            print("Error :" + str(e))
            return False, e

        return True, output


if __name__ == '__main__':
    import os
    import yaml

    with open(os.path.join(os.getcwd(), "config_neo.yml"), 'r') as stream:
        config = yaml.safe_load(stream)

    obj = Neo4jQuery(10, config)

    import code
    code.interact(local={**locals(), **globals()})
