import sqlite3
import pika
import json
import random
from flask_app.Backend.Databases.DatabaseHandlers.queue_publisher import QueuePublisher
from flask_app.Backend.Models.article import Article
from flask_app.Backend.Models.score import Score


class DatabaseHandler:
    def __init__(self):
        self.queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.queue_connection.channel()
        self.result = self.channel.queue_declare(queue='database', durable=True)
        self.publisher = QueuePublisher("event_notifications")

        self.topic_dict = {}

        self.article_amount = 0
        self.articles_sent = 0

        self.articles_inserted_num = 0
        self.articles_not_inserted_num = 0

        self.create_topic_dict()

    def insert_article(self, newspaper, url, full_text, topic, title, morphed_title):
        if topic == "צבא ובטחון":
            topic = "צבא וביטחון"
        try:
            article = Article(newspaper, url, full_text, topic, title, morphed_title, None)
            article.save_to_db()
            self.articles_inserted_num += 1
            if self.articles_inserted_num % 50 == 0:
                # print(" [+] {} articles inserted successfully.".format(self.find_articles_inserted_num()))
                # print(" [-] {} articles failed to insert.".format(self.articles_not_inserted_num))
                self.find_each_newspaper_num()

            if (self.articles_inserted_num + self.articles_not_inserted_num) == self.article_amount:
                self.find_each_newspaper_num()
                print("[+] Inserted {} articles out of {}".format(self.articles_inserted_num, self.article_amount))
                self.publisher.send_event_notification("Finished Webscraping")
        except sqlite3.Error as error:
            self.articles_not_inserted_num += 1
            print("Failed to insert data into sqlite table", error)
        return self.cursor.lastrowid

    def insert_article_scores(self, first_id, second_id, first_title, second_title, title_score, text_score,
                              total_score):
        try:
            score = Score(first_id, second_id, first_title, second_title, title_score, text_score,
                          total_score)
            score.save_to_db()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        return

    def find_articles_inserted_num(self):
        cur_result = Article.count()
        return cur_result

    def find_each_newspaper_num(self):
        newspaper_dict = {'ynet': 0, 'maariv': 0, 'walla': 0, 'mako': 0}
        cur_result = self.select_all_articles()
        for result in cur_result:
            for newspaper in newspaper_dict.keys():
                if newspaper in result[1]:
                    newspaper_dict[newspaper] += 1
        print("\n")
        for newspaper in newspaper_dict:
            print("{} - {}".format(newspaper, newspaper_dict[newspaper]))

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        if body == "Error in Parsing.":
            self.articles_not_inserted_num += 1
            self.articles_sent += 1
        elif type(body) == int:
            self.article_amount = body
        else:
            _id = self.insert_article(body[0], body[1], body[2], body[3], body[4], body[5])
            # cluster_id = self.random_clustering(body[3])
            # self.update_cluster_id(_id, cluster_id)
            self.articles_sent += 1

    def start_consumption(self):
        self.channel.basic_consume(
            queue="database", on_message_callback=self.callback, auto_ack=True
        )

        self.channel.start_consuming()

    def create_topic_dict(self):
        topic_dict = {'צבא וביטחון': [],
                      'מדיני': [],
                      'המערכת הפוליטית': [],
                      'פלסטינים': [],
                      'כללי': [],
                      'משפט ופלילים': [],
                      'חינוך ובריאות': [],
                      'חדשות בעולם': []}

        for topic in topic_dict.keys():
            topic_index = list(topic_dict.keys()).index(topic) * 4
            topic_dict[topic] = list(range(topic_index, topic_index + 4))

        self.topic_dict = topic_dict

    def update_cluster_id(self, _id, cluster_id):
        try:
            Article.update_cluster_id(_id, cluster_id)
        except sqlite3.Error as error:
            print(" [-] Failed to insert cluster id.", error)

    def random_clustering(self, topic_arg):
        cluster_list = self.topic_dict[topic_arg]
        cluster_ids = []
        for i in range(2):
            cluster_ids.append(str(random.choice(cluster_list)))

        cluster_ids_str = ",".join(cluster_ids)
        return cluster_ids_str

    def select_all_articles(self):
        articles = Article.query.all()
        row_list = []
        for article in articles:
            article_tuple = (article.id, article.newspaper, article.url, article.full_text,
                             article.topic, article.title, article.morphed_title, article.cluster_id)
            row_list.append(article_tuple)

        return row_list

    def select_all_scores(self):
        scores = Score.query.all()
        row_list = []
        for score in scores:
            score_tuple = (score.first_id, score.second_id, score.first_title,
                           score.second_title, score.title_score, score.text_score, score.total_score)

            row_list.append(score_tuple)
        return row_list

    def delete_all_rows(self):
        Article.delete_all()
        # delete_key_query = "UPDATE SQLITE_SEQUENCE SET SEQ=0;".format(self.table_name)
        # second_count = self.cursor.execute(delete_key_query)
        # self.connection.commit()

    def delete_all_score_rows(self):
        Score.delete_all()

    def get_url_by_id(self, _id):
        url = Article.get_url_by_id(_id)
        return url
