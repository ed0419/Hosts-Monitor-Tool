import sqlite3
def init_sqlite():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

     c.execute('''CREATE TABLE SYS_USERS
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         USER            CHAR(50)     NOT NULL,
         PASSWORD        CHAR(50)   NOT NULL);''')

    c.execute("INSERT INTO SYS_USERS (ID,NAME,USER,PASSWORD) \
      VALUES (1, 'administrator', 'admin', 'pass')")
    conn.commit()
    conn.close()
init_sqlite()
conn = sqlite3.connect('test.db')
c = conn.cursor()
uid = input()
cursor = c.execute("SELECT NAME, PASSWORD from SYS_USERS where USER='{}'".format(uid))
print(list(cursor)[0][0]) 