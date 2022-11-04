
import db

from flask import Flask, render_template, jsonify, request
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
        ORDER BY id DESC, created DESC LIMIT {PAGE_LIMIT}")
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
        ORDER BY id DESC, created DESC LIMIT {} OFFSET {}""".format(per_page, offset)
    else:
        sql = """
        SELECT title, created, body, id FROM post
        ORDER BY id DESC, created DESC"""

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


@app.route("/api",methods=['GET'])
def api_test():
    sql = "SELECT id, title, created, body FROM post"
    dba = db.get_db()
    result = dba.execute(sql)
    
    rlist = result.fetchall()
    return (jsonify([dict(r) for r in rlist]))


@app.route("/api/<int:article_id>",methods=['GET'])
def api_get_article(article_id):
    sql = "SELECT title, created, body FROM post WHERE id=?"
    dba = db.get_db()
    result = dba.execute(sql, (str(article_id),))
    res_title, res_created, res_body = result.fetchone()
    return jsonify({'id': article_id, 'title': res_title, 'created_date': res_created, 'body': res_body, })

@app.route("/api/<int:article_id>", methods=['DELETE'])
def api_delete_article(article_id):
    sql = "DELETE FROM post WHERE id=?"
    dba = db.get_db()
    cur = dba.execute(sql, (str(article_id),))
    if cur.rowcount > 0:
        dba.commit()
        return jsonify({'id': article_id, 'state':'delete'})
    else:
        dba.rollback()
        return jsonify({'error':'no rows deleted'})
    
    
@app.route("/api",methods=['POST'])
def api_post_article():
    title = request.form['title']
    body = request.form['body']
    sql = "INSERT INTO post(title, body) VALUES(?,?)"
    if title and body:
        dba = db.get_db()
        dba.execute(sql, (title, body,))
        dba.commit()
        return jsonify({'title':title,'body':body})
    else:
        return jsonify({'error':'error'})
    
@app.route("/api/<int:article_id>",methods=['PUT'])
def api_put_article(article_id):
    title = request.form['title']
    body = request.form['body']
    sql = "UPDATE post SET title = ?, body = ? WHERE id = ?"
    if title and body:
        dba = db.get_db()
        dba.execute(sql, (title,body,article_id,))
        dba.commit()
        return jsonify({'id':article_id,'title':title,'body':body})
    else:
        return jsonify({'error': 'form error'})
