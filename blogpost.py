from logging import Logger
import sqlite3
from flask import Blueprint, render_template

blogpost_bp = Blueprint('blogpost_bp',__name__)

@blogpost_bp.route('/blogpost/<int:id>')
def blog_post(id):
    db = sqlite3.connect("instance/posts.sqlite")
    blog_title, blog_created, blog_body = db.execute("""
        SELECT title, created, body FROM post WHERE id = ?
    """,(id,)).fetchone()
    return render_template("blog-post.html", title=blog_title, created=blog_created, body=blog_body)
