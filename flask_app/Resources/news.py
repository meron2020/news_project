from flask_restful import Resource, reqparse
from ..Models.news import NewsModel


class News(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file_name',
                        type=str)
    parser.add_argument('table_name',
                        type=str)

    def get(self):
        data = News.parser.parse_args()
        conn = NewsModel.create_connection(data['file_name'])
        rows_list = NewsModel.select_all_rows(conn, data['table_name'])
        return rows_list
