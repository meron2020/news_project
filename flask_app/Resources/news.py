from flask_restful import Resource, reqparse
from flask_app.Models.news import NewsModel


class News(Resource):
    parser = reqparse.RequestParser()

    def get(self):
        # conn = NewsModel.create_connection()
        rows_list = NewsModel.select_all_rows()
        return rows_list
