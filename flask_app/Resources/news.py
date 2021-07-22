from flask_restful import Resource
from ..Models.news import NewsModel


class News(Resource):
    def __init__(self):
        nlp_file = ""
        nlp_table_name = ""
        conn = NewsModel.create_connection(nlp_file)
        nlp_dict = NewsModel.select_all_rows(conn, nlp_table_name)

        webscraper_conn = NewsModel.create_connection("news_texts.db")
        self.webscraper_dict = NewsModel.select_all_rows(conn, webscraper_conn)

        for key, value in self.webscraper_dict.items():
            value.append(nlp_dict[key])

    def get(self):
        return self.webscraper_dict
