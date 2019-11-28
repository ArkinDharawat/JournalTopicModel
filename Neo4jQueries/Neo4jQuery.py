from py2neo import Graph, Node, Relationship


class Neo4jQuery(object):
    def __init__(self, k, config):
        self.num_topics = k
        self.config = config
        self.graph = Graph(auth=(config["user"], config["password"]))

    def insert_journal(self):
        return "CREATE (j:Journal {id:%s, name:%s, field:%s, ranking:%s)"

    def execute_query(self, query_str, args=[], commit=True):
        import code
        code.interact(local={**locals(), **globals()})


if __name__ == '__main__':
    import os
    import yaml

    with open(os.path.join(os.getcwd(), "config_neo.yml"), 'r') as stream:
        config = yaml.safe_load(stream)

    obj = Neo4jQuery(10, config)
    obj.execute_query(obj.insert_journal(), ["1", "Hi Hello", "Economics", "10000"])
