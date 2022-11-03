from flask import Blueprint, render_template
import db
blogpost_bp = Blueprint('blogpost_bp', __name__)


@blogpost_bp.route('/blogpost/<int:id>')
def blog_post(id):
    dba = db.get_db()
    blog_title, blog_created, blog_body = dba.execute("""
        SELECT title, created, body FROM post WHERE id = ?
    """, (id,)).fetchone()
    return render_template("blog-post.html", title=blog_title, created=blog_created, body=blog_body)
