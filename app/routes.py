from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Book
from .forms import RegistrationForm, LoginForm, BookForm
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Akun berhasil dibuat! Silakan login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Pastikan untuk menggunakan hashing password di aplikasi nyata
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Login gagal. Periksa username dan password Anda.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, year=form.year.data)
        db.session.add(book)
        db.session.commit()
        flash('Buku berhasil ditambahkan!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_book.html', form=form)

@bp.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm()
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.year = form.year.data
        db.session.commit()
        flash('Buku berhasil diperbarui!', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.year.data = book.year
    return render_template('edit_book.html', form=form, book=book)

@bp.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Buku berhasil dihapus!', 'success')
    return redirect(url_for('main.index'))