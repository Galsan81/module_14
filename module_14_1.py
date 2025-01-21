import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Users(id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL)''')

for i in range(10):
    cursor.execute(" INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)", (f"User{i+1}", f'example{i+1}@gmail.com',
    f'{(i+1)*10}', f'{(i+1)*1000}'))

for i in range(10):
    cursor.execute("UPDATE Users SET balance = ? WHERE id % 2 == 0", (1000,))
    cursor.execute("UPDATE Users SET balance = ? WHERE id % 2 == 1", (500,))

for i in range(10):
    cursor.execute("DELETE FROM Users WHERE (id+2)%3==0")


cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
users = cursor.fetchall()
for n in users:
    #print(n)
    print(f'Имя: {n[0]} | Почта: {n[1]} | Возраст: {n[2]} | Баланс: {n[3]}')
connection.commit()
connection.close()
