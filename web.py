from logging import debug
import re, sqlite3
from flask import Flask, request, render_template, redirect, url_for
import json
from threading import Thread
app = Flask(__name__,static_folder='static/')
# def init_sqlite():
#     conn = sqlite3.connect('test.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE SYS_USERS
#         (ID INT PRIMARY KEY     NOT NULL,
#         NAME           TEXT    NOT NULL,
#         USER            INT     NOT NULL,
#         PASSWORD        CHAR(50),
#         SALARY         REAL);''')
#     conn.commit()
#     conn.close()

conn = sqlite3.connect('test.db')
c = conn.cursor()

@app.route('/')
def main():
    return render_template("body.html")

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        uid = request.form["uid"]
        upass = request.form["upass"]
        cursor = c.execute("SELECT PASSWORD from SYS_USERS where USER='{}'".format(uid))
        result = list(cursor)[0][0]
        print(result)
        if result == upass:
            return render_template("admin.html",uid = uid)
        else:
            return render_template("login.html",errorMsg="錯誤的使用者帳號密碼")
    else:
        return render_template("login.html",errorMsg=" ")

def run():
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    server = Thread(target=run)
    server.start()