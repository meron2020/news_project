import sqlite3

connection = sqlite3.connect("names.db")
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS names (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT);")
print("Successfully Connected to SQLite")


def insert(first_name, last_name):
    try:
        sqlite_insert_query = """INSERT INTO names
        (first_name, last_name)
        VALUES
        ('{}', '{}');""".format(first_name, last_name)
        count = cursor.execute(sqlite_insert_query)
        connection.commit()
        print(" [+] name inserted successfully.")
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)


def select_all_rows():
    cursor.execute("SELECT * FROM {}".format("names"))

    rows_list = {}

    rows = cursor.fetchall()
    for row in rows:
        rows_list[row[1]] = row[2]

    print(rows_list)
    print(rows)


insert("yoav", "meron")
insert("tomer", "meron")
insert("yair", "meron")
insert("tzur", "meron")
insert("michal", "meron")

select_all_rows()

something = ('sdfs', 'fdasf', 'fasef')
print(len(something))

print(list(['5']))

def func():
    return 0

num, num1 = func()
print(num1)