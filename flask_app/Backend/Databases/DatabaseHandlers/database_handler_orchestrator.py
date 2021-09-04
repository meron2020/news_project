from flask_app.Backend.Databases.DatabaseHandlers.database_handler import DatabaseHandler
import sqlite3
from flask_app.Backend.Databases.DatabaseHandlers.cache_database_handler import CacheDatabaseHandler


class DatabaseHandlerOrchestrator:
    def run_orchestrator(self):
        handler = DatabaseHandler()
        print("Successfully Connected to articles DB Table")
        handler.delete_all_rows()
        print("Successfully deleted all rows in articles table")
        handler.start_consumption()

    def create_score_db(self):
        handler = DatabaseHandler()
        print("Successfully Connected to scores DB Table")
        try:
            handler.delete_all_score_rows()
        except sqlite3.OperationalError:
            pass
        handler.delete_all_score_rows()
        print("Successfully deleted all rows in scores table")

    def update_cluster_ids(self, cluster_ids_dict):
        handler = DatabaseHandler()
        for cluster_id, articles in cluster_ids_dict.items():
            for article in articles:
                handler.update_cluster_id(article, cluster_id)

    def create_cache_db(self):
        handler = CacheDatabaseHandler()
        print("Successfully Connected to morph_cache DB Table")
        handler.start_consumption()

    def get_all_rows_from_cache(self):
        handler = CacheDatabaseHandler()
        return handler.return_word_to_morph_dict()

    def get_all_rows(self):
        handler = DatabaseHandler()
        print("Successfully Connected to SQLite")
        return handler.select_all_articles()

    def get_all_rows_for_graph(self, path):
        handler = DatabaseHandler()
        print("Successfully Connected to SQLite")
        rows = handler.select_all_articles()
        rows_dict = {}
        for row in rows:
            rows_dict[row[0]] = row
        return rows_dict

    def get_all_rows_from_scores(self):
        handler = DatabaseHandler()
        print("Successfully Connected to SQLite")
        return handler.select_all_scores()

    def get_all_rows_for_nlp(self):
        handler = DatabaseHandler()
        print("Successfully Connected to SQLite")
        return handler.select_all_articles()

    def insert_scores(self, first_id, second_id, first_title, second_title, title_score, text_score, total_score, path):
        handler = DatabaseHandler()
        handler.insert_article_scores(first_id, second_id, first_title, second_title, title_score, text_score,
                                      total_score)

    def delete_all_rows_in_scores(self):
        handler = DatabaseHandler()
        handler.delete_all_score_rows()

    def get_url_by_id(self, _id):
        handler = DatabaseHandler()
        return handler.get_url_by_id(_id)
