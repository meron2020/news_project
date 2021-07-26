from DatabaseHandlers.database_handler import DatabaseHandler
import sqlite3


class DatabaseHandlerOrchestrator:

    def run_orchestrator(self):
        connection = sqlite3.connect("news_texts.db")
        cursor = connection.cursor()
        table_name = "articles"
        handler = DatabaseHandler(str(0), connection, cursor, table_name)
        print("Successfully Connected to SQLite")
        handler.delete_all_rows()
        print("Successfully deleted all rows")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, newspaper TEXT,"
            "full_text TEXT, topic Text,cluster_id Text);")

        handler.start_consumption()
