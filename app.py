from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/main')
def index():
    return render_template("index.html")


@app.route('/posts')
def posts():
    return render_template("posts.html")


@app.route('/create/<string:id>')
def create(id):
    return "Create post " + id


if __name__ == '__main__':
    app.run(debug=True)