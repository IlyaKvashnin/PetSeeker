from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import exc
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///petsSeeker.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phoneNumber = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % self.id


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200), nullable=True)
    date_of_publication = db.Column(db.DateTime, default=datetime.utcnow)
    date_of_accident = db.Column(db.DateTime, nullable=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'))
    type_of_pet_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    isActual = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.id


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case = db.Column(db.String(20), nullable=False)
    posts = db.relationship('Post', backref='case', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % self.id


class Gender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(20), nullable=False)
    posts = db.relationship('Post', backref='gender', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % self.id


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_of_pet = db.Column(db.String(10), nullable=False)
    posts = db.relationship('Post', backref='type', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % self.id


@app.route('/')
@app.route('/main')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def post():
    posts = Post.query.order_by(Post.date_of_publication).all()
    return render_template("posts.html", posts=posts)


@app.route('/new-ad')
def new_ad():
    return render_template("new-ad.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/form-add/find')
def find():
    if request.method == "POST":
        address = request.form['address']
        description = request.form['description']
        gender = request.form.get('genders')
        type_of_pet = request.form.get('types')
        date_of_accident = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        name = request.form['firstName'] + ' ' + request.form['lastName']
        phone = request.form['phone']
        email = request.form['email']
        user = User(name=name, phoneNumber=phone, email=email)
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
        except:
            return "При добавлении пользователя произошла ошибка"
        post = Post(description=description, isActual=1, address=address, gender_id=gender, type_of_pet_id=type_of_pet,
                    date_of_accident=date_of_accident, user_id=user.id, case_id=2)

        try:

            db.session.add(post)
            db.session.commit()
            return redirect('/posts')
        except exc.IntegrityError:
            db.session.rollback()
        except:
            return "При добавлении объявления произошла ошибка"

    else:
        return render_template("form-add/find2.html")


@app.route('/form-add/lost', methods=['POST', 'GET'])
def lost():
    if request.method == "POST":
        address = request.form['address']
        description = request.form['description']
        gender = request.form.get('genders')
        type_of_pet = request.form.get('types')
        date_of_accident = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        name = request.form['firstName'] + ' ' + request.form['lastName']
        phone = request.form['phone']
        email = request.form['email']
        user = User(name=name, phoneNumber=phone, email=email)
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
        except:
            return "При добавлении пользователя произошла ошибка"
        post = Post(description=description, isActual=1, address=address, gender_id=gender, type_of_pet_id=type_of_pet,
                    date_of_accident=date_of_accident, user_id=user.id, case_id=1)

        try:

            db.session.add(post)
            db.session.commit()
            return redirect('/posts')
        except exc.IntegrityError:
            db.session.rollback()
        except:
            return "При добавлении объявления произошла ошибка"

    else:
        return render_template("form-add/lost.html")


@app.route('/create/<string:id>')
def create(id):
    return "Create post " + id


@app.route('/create-post')
def create_post():
    return render_template("create-post.html")


if __name__ == '__main__':
    app.run(debug=True)
