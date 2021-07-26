import sqlite3


class NewsModel:
    def __init__(self):
        pass

    @classmethod
    def create_connection(cls, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)

        return conn

    @classmethod
    def select_all_rows(cls, conn, table_name):
        cur = conn.cursor()
        cur.execute("SELECT * FROM {}".format(table_name))
        rows_list = []
        rows = cur.fetchall()
        for row in rows:
            rows_list.append({"newspaper": row[1], "url": row[2],
                              "full_text": row[3], "topic": row[4]})
        return rows_list
