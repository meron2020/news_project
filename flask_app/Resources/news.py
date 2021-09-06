from flask_restful import Resource, reqparse
from flask_app.Models.news import NewsModel


class News(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        self.topic_dict = {"military": 'צבא וביטחון',
                           "state": 'מדיני',
                           "politics": 'המערכת הפוליטית',
                           "palestine": 'פלסטינים',
                           "general": 'כללי',
                           "law": 'משפט ופלילים',
                           "health and education": 'חינוך ובריאות',
                           "world": 'חדשות בעולם'}

    def get(self, topic):
        rows_list = []
        if topic == "state and politics":
            rows_list.extend(NewsModel.select_all_topic_rows(self.topic_dict["state"]))
            rows_list.extend(NewsModel.select_all_topic_rows(self.topic_dict["politics"]))
        else:
            topic = self.topic_dict[topic]
            rows_list = NewsModel.select_all_topic_rows(topic)
        return {"rows_list": rows_list}
