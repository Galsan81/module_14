import sqlite3



connection = sqlite3.connect('dbproduct.db')
cursor = connection.cursor()
def initiate_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products(id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL DEFAULT 1000)''')

def add_users(username, email, age):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)", (username,
                                                                                            email, age, 1000))
    connection.commit()

def is_included(username):
    res = cursor.execute('''SELECT username FROM Users WHERE username = ?''', (username,)).fetchone()
    connection.commit()
    if res:
        return True
    else:
        return False

def get_all_products():
    cursor.execute("SELECT * FROM Products")
    prods = cursor.fetchall()
    return prods
'''for i in range(4):
    cursor.execute(" INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", (f"Продукт {i+1}", f'Описание {i+1}',
    f'{(i+1)*100}'))'''


connection.commit()
#connection.close()