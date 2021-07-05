import sqlite3


class DatabaseHandler:
    def __init__(self):
        self.connection = sqlite3.connect("news_texts.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, newspaper TEXT, url TEXT,"
            "full_text TEXT);")
        print("Successfully Connected to SQLite")

    def insert_article(self, newspaper, url, full_text):
        try:
            sqlite_insert_query = """INSERT INTO articles
            (newspaper, url, full_text)
            VALUES
            ('{}', '{}', '{}');""".format(newspaper, url, full_text)
            count = self.cursor.execute(sqlite_insert_query)
            self.connection.commit()
            print(" [+] {} article inserted successfully.".format(newspaper))
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

