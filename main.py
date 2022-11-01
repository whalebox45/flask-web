from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/blogpost")
def blogpost():
    return render_template('blog-post.html')

@app.route("/bloglist")
def bloglist():
    return render_template('blog-list.html')

@app.route("/about")
def about():
    return render_template('about.html')
