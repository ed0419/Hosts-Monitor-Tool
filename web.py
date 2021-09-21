from flask import Flask, request, render_template, redirect, url_for
import json
app = Flask(__name__,static_folder='static/')

@app.route('/')
def main():
    render_template("body.html")

@app.route('/login',methods=["POST","GET"])
def login():
   if request.method == "POST":
       