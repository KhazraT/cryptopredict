import sqlite3

connection = sqlite3.connect("server.db")
cursor = connection.cursor()

def create_table():
    global connection, cursor
    cursor.execute("""CREATE TABLE IF NOT EXISTS "cryptoprices" (
        "Название"	TEXT NOT NULL UNIQUE,
        "Стоимость"	REAL NOT NULL,
        "Дата"	INTEGER NOT NULL
    )""")
    connection.commit()

def insert_into_db(name: str, price: float, data):
    global connection, cursor
    data = 10000*data.year + 100*data.month + data.day
    cursor.execute("""SELECT "Название" FROM cryptoprices""")
    n = cursor.fetchall()
    if name not in list(map(lambda x: x[0], n)):
        cursor.execute(f"""INSERT INTO cryptoprices VALUES (?, ?, ?)""", (name, price, data))
    else:
        cursor.execute("""SELECT "Дата" FROM cryptoprices WHERE "Название"=(?)""", (name,))
        n = cursor.fetchone()
        if n[0] < data:
            cursor.execute("""UPDATE cryptoprices SET "Стоимость"=?, "Дата"=? WHERE "Название"=?""", (price, data, name))
    connection.commit()

def get_cpyptoprice(name):
    global connection, cursor
    cursor.execute("""SELECT "Стоимость" FROM cryptoprices WHERE "Название"=(?)""", (name,))
    return cursor.fetchone()[0]

create_table()