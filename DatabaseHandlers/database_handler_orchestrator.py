from DatabaseHandlers.database_handler import DatabaseHandler
import sqlite3
from DatabaseHandlers.cache_database_handler import CacheDatabaseHandler


class DatabaseHandlerOrchestrator:
    def run_orchestrator(self):
        connection = sqlite3.connect(r"C:\\Users\\coolermaster\\PycharmProjects\\NewsProject\\news_texts.db")
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(connection, cursor, table_name)
        print("Successfully Connected to SQLite")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, newspaper TEXT,"
            "full_text TEXT, topic Text,cluster_id Text);")

        handler.delete_all_rows()
        print("Successfully deleted all rows")

        handler.start_consumption()

    def create_cache_db(self):
        connection = sqlite3.connect(r"C:\\Users\\coolermaster\\PycharmProjects\\NewsProject\\news_texts.db")
        cursor = connection.cursor()
        table_name = "morph_cache"
        handler = CacheDatabaseHandler(connection, cursor, table_name)
        print("Successfully Connected to SQLite")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS morph_cache (word TEXT, morphed_word TEXT);")

        handler.start_consumption()

    def get_all_rows_from_cache(self):
        connection = sqlite3.connect(r"C:\\Users\\coolermaster\\PycharmProjects\\NewsProject\\news_texts.db")
        cursor = connection.cursor()
        table_name = "morph_cache"
        handler = CacheDatabaseHandler(connection, cursor, table_name)
        return handler.return_word_to_morph_dict()

    def get_all_rows(self):
        connection = sqlite3.connect(r"C:\\Users\\coolermaster\\PycharmProjects\\NewsProject\\news_texts.db")
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(connection, cursor, table_name)
        print("Successfully Connected to SQLite")
        return handler.select_all_rows()

    def get_url_by_id(self, _id):
        connection = sqlite3.connect(r"C:\\Users\\coolermaster\\PycharmProjects\\NewsProject\\news_texts.db")
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(connection, cursor, table_name)
        return handler.get_url_by_id(_id)
