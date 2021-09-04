from flask_app.Backend.Databases.DatabaseHandlers.database_handler import DatabaseHandler
import sqlite3
from flask_app.Backend.Databases.DatabaseHandlers.cache_database_handler import CacheDatabaseHandler


class DatabaseHandlerOrchestrator:
    def run_orchestrator(self):
        connection = sqlite3.connect(r"../../news_texts.db")
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(connection, cursor, table_name)
        print("Successfully Connected to articles DB Table")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, newspaper TEXT,"
            "full_text TEXT, topic Text, title Text, morphed_title Text, cluster_id Text);")

        handler.delete_all_rows()
        print("Successfully deleted all rows in articles table")

        handler.start_consumption()

    def create_score_db(self):
        connection = sqlite3.connect(r"../../news_texts.db")
        cursor = connection.cursor()
        table_name = "scores"
        handler = DatabaseHandler(connection, cursor, table_name)
        print("Successfully Connected to scores DB Table")
        try:
            cursor.execute(
                "DROP TABLE {}".format(table_name)
            )
        except sqlite3.OperationalError:
            pass
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS scores "
            "(first_id Int, second_id Int, "
            "first_title Text, second_title Text, title_score Int, text_score Int, total_score Int);")

        handler.delete_all_score_rows()
        print("Successfully deleted all rows in scores table")

    def update_cluster_ids(self, cluster_ids_dict, path):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(connection, cursor, table_name)
        for cluster_id, articles in cluster_ids_dict.items():
            for article in articles:
                handler.update_cluster_id(article, cluster_id)

    def create_cache_db(self):
        connection = sqlite3.connect(r"../../news_texts.db")
        cursor = connection.cursor()
        table_name = "morph_cache"
        handler = CacheDatabaseHandler(connection, cursor, table_name)
        print("Successfully Connected to morph_cache DB Table")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS morph_cache (word TEXT, morphed_word TEXT);")

        handler.start_consumption()

    def get_all_rows_from_cache(self):
        connection = sqlite3.connect(r"../../news_texts.db")
        cursor = connection.cursor()
        table_name = "morph_cache"
        handler = CacheDatabaseHandler(connection, cursor, table_name)
        return handler.return_word_to_morph_dict()

    def get_all_rows(self):
        connection = sqlite3.connect(r"../../news_texts.db")
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(connection, cursor, table_name)
        print("Successfully Connected to SQLite")
        return handler.select_all_rows()

    def get_all_rows_for_graph(self, path):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(connection, cursor, table_name)
        print("Successfully Connected to SQLite")
        rows = handler.select_all_rows()
        rows_dict = {}
        for row in rows:
            rows_dict[row[0]] = row
        return rows_dict

    def get_all_rows_from_scores(self, path):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        table_name = "scores"
        handler = DatabaseHandler(connection, cursor, table_name)
        print("Successfully Connected to SQLite")
        return handler.select_all_rows()

    def get_all_rows_for_nlp(self, path):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(connection, cursor, table_name)
        print("Successfully Connected to SQLite")
        return handler.select_all_rows()

    def insert_scores(self, first_id, second_id, first_title, second_title, title_score, text_score, total_score, path):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        table_name = "scores"
        handler = DatabaseHandler(connection, cursor, table_name)
        handler.insert_article_scores(first_id, second_id, first_title, second_title, title_score, text_score,
                                      total_score)

    def delete_all_rows_in_scores(self):
        connection = sqlite3.connect(r"../../news_texts.db")
        cursor = connection.cursor()
        table_name = "scores"
        handler = DatabaseHandler(connection, cursor, table_name)
        handler.delete_all_score_rows()

    def get_url_by_id(self, _id, path):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(connection, cursor, table_name)
        return handler.get_url_by_id(_id)

    def get_url_to_url_score(self, path):
        url_to_url_score = []
        for score_row in self.get_all_rows_from_scores(path):
            first_url = self.get_url_by_id(score_row[0], path)
            second_url = self.get_url_by_id(score_row[1], path)
            first_title = self.get_title_by_id(score_row[0], path)
            second_title = self.get_title_by_id(score_row[1], path)
            url_to_url_score.append(
                [first_url, second_url, first_title, second_title, score_row[2], score_row[3], score_row[4]])
        return url_to_url_score

    def get_title_by_id(self, _id, path):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(connection, cursor, table_name)
        return handler.get_title_by_id(_id)
