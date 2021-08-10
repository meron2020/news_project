import sqlite3


class CacheDatabaseHandler:
    def __init__(self, connection, cursor, table_name):
        self.connection = connection
        self.cursor = cursor
        self.table_name = table_name

    def insert_morphology_words(self, word, morphed_word):
        try:
            sqlite_insert_query = """INSERT INTO {} 
            (word, morphed_words)
            VALUES 
            ({}, {});""".format(self.table_name, word, morphed_word)
            count = self.cursor.execute(sqlite_insert_query)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def return_word_to_morph_dict(self):
        self.cursor.execute("SELECT * FROM {}".format(self.table_name))

        rows = self.cursor.fetchall()

        row_list = {}
        for row in rows:
            row_list[row(0)] = row[1]

        return row_list
