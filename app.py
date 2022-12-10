from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/main')
def index():
    return render_template("index.html")


@app.route('/posts')
def posts():
    return render_template("posts.html")


@app.route('/new-ad')
def new_ad():
    return render_template("new-ad.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/form-add/find')
def find():
    return render_template("form-add/find.html")


@app.route('/form-add/lost')
def lose():
    return render_template("form-add/lost.html")


@app.route('/create/<string:id>')
def create(id):
    return "Create post " + id


if __name__ == '__main__':
    app.run(debug=True)