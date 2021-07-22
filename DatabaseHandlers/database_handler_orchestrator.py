from DatabaseHandlers.database_handler import DatabaseHandler
import sqlite3


class DatabaseHandlerOrchestrator:
    @classmethod
    def run_orchestrator(cls):
        connection = sqlite3.connect("news_texts.db")
        cursor = connection.cursor()
        table_name = "articles"
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, newspaper TEXT,"
            "full_text TEXT, topic Text,cluster_id Text);")
        print("Successfully Connected to SQLite")

        handler = DatabaseHandler(str(0), connection, cursor, table_name)

        handler.start_consumption()
