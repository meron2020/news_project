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

urls_dict = {"https://www.ynet.co.il/news/article/sju500x4cu#autoplay": 'צבא וביטחון',
             "https://www.ynet.co.il/news/article/skfpuovcu#autoplay": 'מדיני',
             "https://www.ynet.co.il/news/article/s1arbdsru#autoplay": 'חדשות בעולם',
             "https://www.ynet.co.il/news/article/rjj00t4ea00": 'חדשות בעולם',
             "https://www.ynet.co.il/news/article/s1vo1i4ru#autoplay": 'צבא וביטחון',
             }

for url in urls_dict.keys():
    ynet_urls_list = list(urls_dict.keys())
    number_list = list(range(1, 5))
    cluster_ids = []
    for i in range(3):
        cluster_ids.append(str(random.choice(number_list)))
        number_list.remove(int(cluster_ids[-1]))
    cluster_ids_str = ",".join(cluster_ids)

    if "ynet" in url:
        worker = YnetWorker(url)
        newspaper = "ynet"
    elif "maariv" in url:
        worker = MaarivWorker(url)
        newspaper = "maariv"
    elif "mako" in url:
        worker = N12Worker(url)
        newspaper = "mako"
    else:
        worker = IsraelHayomWorker(url)
        newspaper = "israel hayom"

    full_text = worker.parse()
    full_text = full_text.replace("'", "")

    handler.insert_article(newspaper, url, full_text, urls_dict[url])
    handler.update_cluster_id(ynet_urls_list.index(url) + 1, cluster_ids_str)
