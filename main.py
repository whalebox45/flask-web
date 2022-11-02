from email.policy import default
import sqlite3
from unittest import result
from flask import Flask, render_template, g, current_app
from flask_paginate import Pagination, get_page_args
from blogpost import blogpost_bp
import os

app = Flask(__name__)

PAGE_LIMIT = 5

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


@app.route("/bloglist", defaults={"page":1})
@app.route("/bloglist/page/<int:page>")
def bloglist(page):
    db = sqlite3.connect("instance/posts.sqlite")

    total = db.execute("SELECT count(*) FROM post").fetchone()[0]

    page, per_page, offset = get_page_args(
        per_page_parameter="pp",pp=PAGE_LIMIT
    )

    print(page, per_page, offset,)

    if per_page:
        sql = """select title, created, body, id FROM post 
        ORDER BY created DESC LIMIT {} OFFSET {}""".format(per_page,offset)
    else:
        sql = """
        SELECT title, created, body, id FROM post
        ORDER BY created DESC"""

    result = db.execute(sql)
    rlist = result.fetchall()

    pagination = Pagination(
        p=page,
        pp=per_page,
        total=total,
        page_parameter="p",
        per_page_parameter="pp",
    )
    
    print(pagination.page+1)

    return render_template('blog-list.html', result = rlist, pagination=pagination)

@app.route("/about")
def about():
    return render_template('about.html')

