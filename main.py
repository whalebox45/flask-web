import sqlite3
from unittest import result
from flask import Flask, render_template, g, current_app
from blogpost import blogpost_bp
import os

app = Flask(__name__)

@app.cli.command("init-db")
def init_db():
    db = sqlite3.connect("instance/posts.sqlite")
    cur = db.cursor()
    with open('schema.sql','r', encoding='utf-8') as f:
        cur.executescript(f.read())
    


app.register_blueprint(blogpost_bp)

@app.route("/")
def index():
    db = sqlite3.connect("instance/posts.sqlite")
    result = db.execute("""
        SELECT title, created, body, id FROM post
        ORDER BY created DESC LIMIT 5
    """)
    rlist = result.fetchall()
    return render_template('index.html',result = rlist)


@app.route("/bloglist")
def bloglist():
    db = sqlite3.connect("instance/posts.sqlite")
    result = db.execute("""
        SELECT title, created, body, id FROM post
        ORDER BY created DESC
    """)
    rlist = result.fetchall()
    return render_template('blog-list.html', result = rlist)

@app.route("/about")
def about():
    return render_template('about.html')

