
import db

from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args
from blogpost import blogpost_bp
import os

app = Flask(__name__)

PAGE_LIMIT = 5

db.init_app(app)
app.config.from_mapping(
    # a default secret that should be overridden by instance config
    # SECRET_KEY="dev",
    # store the database in the instance folder
    DATABASE=os.path.join(app.instance_path, "posts.sqlite"),
)

app.register_blueprint(blogpost_bp)


@app.route("/")
def index():
    dba = db.get_db()
    result = dba.execute(f"SELECT title, created, body, id FROM post\
        ORDER BY created DESC LIMIT {PAGE_LIMIT}")
    rlist = result.fetchall()
    return render_template('index.html', result=rlist)


@app.route("/bloglist", defaults={"page": 1})
@app.route("/bloglist/page/<int:page>")
def bloglist(page):
    dba = db.get_db()

    total = dba.execute("SELECT count(*) FROM post").fetchone()[0]

    page, per_page, offset = get_page_args(
        per_page_parameter="pp", pp=PAGE_LIMIT
    )

    # print(page, per_page, offset,)

    if per_page:
        sql = """select title, created, body, id FROM post 
        ORDER BY created DESC LIMIT {} OFFSET {}""".format(per_page, offset)
    else:
        sql = """
        SELECT title, created, body, id FROM post
        ORDER BY created DESC"""

    result = dba.execute(sql)
    rlist = result.fetchall()

    pagination = Pagination(
        p=page,
        pp=per_page,
        total=total,
        page_parameter="p",
        per_page_parameter="pp",
    )

    return render_template('blog-list.html', result=rlist, pagination=pagination)


@app.route("/about")
def about():
    return render_template('about.html')
