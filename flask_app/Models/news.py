import sqlite3


class NewsModel:
    def __init__(self):
        pass

    @classmethod
    def create_connection(cls):
        conn = sqlite3.connect(r"..\news_texts.db")
        return conn

    @classmethod
    def select_all_topic_rows(cls, topic):
        conn = NewsModel.create_connection()
        cur = conn.cursor()
        rows_list = []

        cur.execute("SELECT * FROM {} WHERE topic={}".format("articles", '"' + topic + '"'))
        rows = cur.fetchall()
        for row in rows:
            rows_list.append({"newspaper": row[2], "url": row[1], "topic": row[4],
                              "title": row[5], "cluster_id": row[7]})

        return rows_list
