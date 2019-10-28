class SQLStrQuery(object):
    def __init__(self, k):
        self.num_topics = k

    def create_procedure(self):
        part1 = "CREATE PROCEDURE GetTopicCosDist(" + ','.join(
            [" IN B_Topic{0} INTEGER".format(i) for i in range(self.num_topics)]) + ") BEGIN \n"

        part2 = "DECLARE finished INTEGER DEFAULT 0; DECLARE Paper_Id INTEGER; DECLARE AB INTEGER; DECLARE A REAL; DECLARE B REAL; DECLARE CosDist REAL;" + ';'.join(
            [" DECLARE A_Topic{0} INTEGER".format(i) for i in range(self.num_topics)]) + ";\n"

        part3 = "DECLARE stdcur CURSOR FOR SELECT T.Paper_Id," + ','.join(["T.Topic{0}".format(i) for i in range(
            self.num_topics)]) + " FROM Topics_per_Paper T; DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;\n"

        part4 = "DROP TABLE IF EXISTS temp_topic_table; CREATE TABLE temp_topic_table (Paper_Id INTEGER, CosineDistance REAL);  OPEN stdcur; REPEAT FETCH stdcur INTO Paper_Id," + ','.join(
            ["A_Topic{0}".format(i) for i in range(self.num_topics)]) + ";\n"

        part5 = "SET AB = " + ' + '.join(["A_Topic{0} * B_Topic{0}".format(i) for i in range(self.num_topics)]) + ";\n"

        part6 = "SET A = SQRT(" + ','.join(
            ["A_Topic{0}".format(i) for i in range(self.num_topics)]) + "); SET B = SQRT(" + ','.join(
            ["B_Topic{0}".format(i) for i in range(
                self.num_topics)]) + "); SET CosDist = ROUND(AB / (A * B), 2); INSERT INTO temp_topic_table VALUES (Paper_Id, CosDist)" + ";\n"

        part7 = "UNTIL finished END REPEAT; CLOSE stdcur; END//"

        total_sql_str = "DELIMITER //" + part1 + part2 + part3 + part4 + part5 + part6 + part7 + "DELIMITER ;"

        return total_sql_str

    def create_tables(self):
        table_acad_journal = "CREATE TABLE Academic_Journal " \
                             "(Journal_Id INTEGER NOT NULL, Journal_Name CHAR(255), Category VARCHAR(1024), " \
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
        return "INSERT INTO Academic_Journal (Journal_Id, Journal_Name, Category) VALUES (%s, %s, %s);"

    def insert_paper(self):
        return "INSERT INTO Academic_Paper (Paper_Id, Authors, Journal_Id, Title, Abstract) VALUES (%s, %s, %s, %s, %s);"

    def update_paper(self, col_names):
        alter_str = ','.join([x + "=%s" for x in col_names])
        return "UPDATE Academic_Paper SET " + alter_str + " WHERE Paper_Id = %s;"

    def delete_paper(self):
        return "DELETE FROM Academic_Paper WHERE Paper_Id = %s;"

    def insert_topic(self, paper_id, topic_indices):
        topic_str = ','.join(["Topic{0}".format(i) for i in range(self.num_topics)])
        value_str = ["0"] * self.num_topics
        for k in topic_indices:
            value_str[k - 1] = "1"
        value_str = ",".join(value_str)

        return "INSERT INTO Topics_per_Paper (Paper_Id, " + topic_str + ") VALUES (" + \
               str(paper_id) + "," + value_str + ");"

    def update_topic(self, topic_indices):
        value_str = ["0"] * self.num_topics
        for k in topic_indices:
            value_str[k - 1] = "1"

        alter_str = ','.join(["Topic" + str(i) + "=" + value_str[i] for i in range(self.num_topics)])

        return "UPDATE Topics_per_Paper SET " + alter_str + " WHERE Paper_Id = %s;"

    def delete_topic(self):
        return "DELETE FROM Topics_per_Paper WHERE Paper_Id = %s;"


if __name__ == '__main__':
    obj = SQLStrQuery(10)
    obj.create_procedure()
    # print(obj.update_paper([2, 4]))
    # obj.create_tables()
    # obj.insert_topic([2, 4])
