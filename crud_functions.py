import sqlite3



connection = sqlite3.connect('dbproduct.db')
cursor = connection.cursor()
def initiate_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products(id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)''')
initiate_db()
def get_all_products():
    cursor.execute("SELECT * FROM Products")
    prods = cursor.fetchall()
    return prods
'''for i in range(4):
    cursor.execute(" INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", (f"Продукт {i+1}", f'Описание {i+1}',
    f'{(i+1)*100}'))'''


connection.commit()
#connection.close()