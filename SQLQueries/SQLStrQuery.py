class SQLStrQuery(object):
    def __init__(self, k):
        self.num_topics = k

    def create_tables(self):
        table_acad_journal = "CREATE TABLE Academic_Journal " \
                             "(Journal_Id INTEGER NOT NULL, Journal_Name CHAR(255), Category VARCHAR(255), " \
                             "PRIMARY KEY(Journal_Id));"

        table_acad_paper = "CREATE TABLE Academic_Paper " \
                           "(Paper_Id INTEGER NOT NULL, Authors CHAR(64), Journal_Id INTEGER NOT NULL, Title CHAR(255), Abstract TEXT, " \
                           "PRIMARY KEY(Paper_Id), FOREIGN KEY(Journal_Id) REFERENCES Academic_Journal(Journal_Id));"

        topic_values = ["Paper_Id INTEGER NOT NULL"]
        for i in range(self.num_topics):
            topic_values.append("Topic{0} INTEGER".format(i))
        value_str = ",".join(topic_values)
        table_topic = "CREATE TABLE Topics_per_Paper (" + value_str + ", FOREIGN KEY(Paper_Id) REFERENCES Academic_Paper(Paper_Id));"

        return [table_acad_journal, table_acad_paper, table_topic]

    def insert_journal(self):
        return "INSERT INTO Academic_Journal (Journal_Id, Journal_Name, Category) VALUES (%s, %s, %s)"

    # TODO: INSERT
    # TODO: UPDATE


if __name__ == '__main__':
    obj = SQLStrQuery(5)
    obj.create_tables()
