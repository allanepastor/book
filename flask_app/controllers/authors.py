from  flask import Flask, render_template, redirect, request
from flask_app import app
from flask_app.models import author, book


@app.route('/')
def index():
    return redirect('/authors')

@app.route('/authors')
def authors():
    authors = author.Author.get_all_authors()
    return render_template('authors.html', all_authors = authors)

@app.route('/create-author', methods = ['POST'])
def add_author():
    data = {
        'id': id,
        'name': request.form['name'],
    }
    author.Author.create_author(data)
    return redirect('/')

@app.route('/authors/<int:id>')
def show_author(id):
    data = {
        'id': id
    }
    authors = author.Author.get_one_author(data)
    books = book.Book.unfavorite_books(data)
    results = render_template('author_show.html', author = authors, unfavorite_books = books)
    return results

@app.route('/join/book', methods=['POST'])
def join_book():
    data = {
        'author_id' : request.form['author_id'],
        'book_id' : request.form['book_id'],
    }
    author.Author.add_favorite(data)
    return redirect(f"/authors/{request.form['author_id']}")
