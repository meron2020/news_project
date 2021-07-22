from Parsers.ynet_parser import YnetWorker
from Parsers.N12_parser import N12Worker
from Parsers.israel_hayom_parser import IsraelHayomWorker
from Parsers.maariv_parser import MaarivWorker
from DatabaseHandlers.database_handler import DatabaseHandler
import sqlite3
import random


def create_db():
    connection = sqlite3.connect("mini_nlp.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, newspaper TEXT,"
        "full_text TEXT, topic Text,cluster_id Text);")
    print("Successfully Connected to SQLite")

    return DatabaseHandler(str(0), connection, cursor, "articles")


handler = create_db()

ynet_urls_dict = {"https://www.ynet.co.il/news/article/sju500x4cu#autoplay": 'צבא וביטחון',
                  "https://www.ynet.co.il/news/article/skfpuovcu#autoplay": 'מדיני',
                  "https://www.ynet.co.il/news/article/s1arbdsru#autoplay": 'חדשות בעולם',
                  "https://www.ynet.co.il/news/article/rjj00t4ea00": 'חדשות בעולם',
                  "https://www.ynet.co.il/news/article/s1vo1i4ru#autoplay": 'צבא וביטחון'}

for url in ynet_urls_dict.keys():
    ynet_urls_list = list(ynet_urls_dict.keys())
    number_list = range(1, 5)
    cluster_id = ""
    for i in range(3):
        cluster_id += str(random.choice(number_list))
        cluster_id += " "

    worker = YnetWorker(url)
    full_text = worker.parse()
    handler.insert_article("ynet", url, full_text, ynet_urls_dict[url])
    handler.update_cluster_id(ynet_urls_list.index(url) + 1, cluster_id)



