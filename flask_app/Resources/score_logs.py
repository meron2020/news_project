from flask_restful import Resource, reqparse
from flask_app.Backend.Databases.Models import ScoreLogsModel


class ScoreLogs(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        self.logs = ScoreLogsModel()

    def get(self):
        rows_list = self.logs.select_url_to_url_score()
        return {"rows_list": rows_list}
