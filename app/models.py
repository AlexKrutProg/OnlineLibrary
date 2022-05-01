from importlib.resources import path
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    surename = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '{} {}'.format(self.name, self.surename)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    path = db.Column(db.Text)

    def __repr__(self):
        return '{}'.format(self.title)


class Usage(db.Model):
    __tablename__ = 'usages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user = db.relationship(User, backref=db.backref("usages", cascade="all, delete-orphan"))
    book = db.relationship(Book, backref=db.backref("usages", cascade="all, delete-orphan"))


class Authorship(db.Model):
    __tablename__ = 'authorships'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    author = db.relationship(Author, backref=db.backref("authorships", cascade="all, delete-orphan"))
    book = db.relationship(Book, backref=db.backref("authorships", cascade="all, delete-orphan"))
