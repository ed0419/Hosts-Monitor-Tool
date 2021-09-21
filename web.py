from logging import debug
import re
from flask import Flask, request, render_template, redirect, url_for
import json
from threading import Thread
app = Flask(__name__,static_folder='static/')

@app.route('/')
def main():
    return render_template("body.html")

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        uid = request.form["uid"]
        upass = request.form["upass"]
        print(uid,upass)
        return render_template("admin.html",uid = uid)
    else:
        return render_template("login.html")

def run():
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    server = Thread(target=run)
    server.start()