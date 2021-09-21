from datetime import timedelta
import re, sqlite3
from flask import Flask, request, LoginManager, render_template, redirect, session
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



@app.route('/')
def main():
    return redirect("login")

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/login',methods=["POST","GET"])
def login():
    if 'login' not in session:
        session['login'] = 0
    if 'stuff' not in session:
        session['stuff'] = []
    if request.method == "POST":
        uid = request.form["uid"]
        upass = request.form["upass"]
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        try:
            cursor = c.execute("SELECT PASSWORD from SYS_USERS where USER='{}'".format(uid))
            result = list(cursor)[0][0]
            print(result)
            if result == upass:
                return render_template("admin.html",uid = uid)
        except:
            return render_template("login.html",errorMsg="錯誤的使用者帳號密碼")
    else:
        return render_template("login.html",errorMsg=" ")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=8080, debug=True)
    login_manager = LoginManager(app)  
    app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
    SESSION_COOKIE_NAME="WHATDOUWANT",
    #SESSION_COOKIE_DOMAIN=""
)