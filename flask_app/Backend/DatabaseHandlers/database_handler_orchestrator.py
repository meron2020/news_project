from flask_app.Backend.DatabaseHandlers.database_handler import DatabaseHandler
import sqlite3
from flask_app.Backend.DatabaseHandlers.cache_database_handler import CacheDatabaseHandler


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

    def update_cluster_ids(self, cluster_ids_dict):
        connection = sqlite3.connect(r"../../news_texts.db")
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

    def get_all_rows_for_nlp(self):
        connection = sqlite3.connect(r"../../news_texts.db")
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(connection, cursor, table_name)
        print("Successfully Connected to SQLite")
        return handler.select_all_rows()

    def get_url_by_id(self, _id):
        connection = sqlite3.connect(r"../../news_texts.db")
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(connection, cursor, table_name)
        return handler.get_url_by_id(_id)
