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

        rows_list = {}

        rows = cur.fetchall()
        for row in rows:

            if len(row) == 3:
                rows_list[row[1]] = list(row[2])
            else:
                rows_list[row[1]] = list(row[2:])

        return rows_list


