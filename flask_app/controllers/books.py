from flask import render_template, redirect, request
from flask_app import app
from flask_app.models import book, author

@app.route('/books')
def books():
    books = book.Book.get_all_books()
    return render_template('books.html', all_books = books)

@app.route('/add-book', methods = ['POST'])
def add_book():
    data = {
        'id': id,
        'title': request.form['title'],
        'num_of_pages': request.form['num_of_pages'],
    }
    book.Book.create_book(data)
    return redirect('/books')

@app.route('/book/<int:id>')
def show_book(id):
    data = {
        "id": id
    }
    books = book.Book.get_one_book(data)
    authors = author.Author.unfavorite_authors(data)
    result = render_template('book_show.html', book = books, unfavorite_authors = authors)
    return result

@app.route('/join/author', methods=['POST'])
def join_author():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    author.Author.add_favorite(data)
    return redirect(f"/book/{request.form['book_id']}")
