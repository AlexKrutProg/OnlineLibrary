from importlib.resources import path
from app import app, db
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from flask import render_template, redirect, session, url_for, request
from app.forms import LoginForm, RegistrationForm, BorrowForm
from app.models import User, Book, Usage, Author, Authorship
from app.template_classes.classes import ImpBook 


@app.route('/')
@app.route('/index')
@login_required
def index():
    books = [ImpBook(book, [aship.author for aship in Authorship.query.filter_by(book=book)]) for book in Book.query]
    for book in books:
        if Usage.query.filter_by(user=current_user).filter_by(book=book.book).first():
            book.is_borrowed = True
    return render_template('index.html', books = books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/book_view/<_book>', methods=['GET', 'POST'])
@login_required
def book_view(_book):
    book = ImpBook(Book.query.get(int(_book)), [aship.author for aship in Authorship.query.filter_by(book=Book.query.get(int(_book)))])
    if Usage.query.filter_by(user=current_user).filter_by(book=book.book).first():
            book.is_borrowed = True
    borrow = BorrowForm()
    if borrow.validate_on_submit():
        usage = Usage(user=current_user, book=book.book)
        book.is_borrowed = True
        db.session.add(usage)
        db.session.commit()
        return render_template('book_view.html', book=book)
    return render_template('book_view.html', book=book, borrow=borrow)


@app.route('/profile/<_user>', methods=['GET', 'POST'])
@login_required
def profile(_user):
    user = User.query.get(int(_user))
    books = [usage.book for usage in Usage.query.filter_by(user=user)]
    return render_template('profile.html', books=books)


@app.route('/book_read/<_book>')
@login_required
def book_read(_book):
    book = Book.query.get(int(_book))
    return render_template('book_read.html', book=book)


@app.route('/book_return/<_book>')
@login_required
def book_return(_book):
    usage = Usage.query.filter_by(user=current_user).filter_by(book=Book.query.get(int(_book))).first()
    db.session.delete(usage)
    db.session.commit()
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    return redirect(next_page)