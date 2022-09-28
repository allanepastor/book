from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    db = 'books_authors'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_who_favorite = []

    @classmethod
    def get_all_books(cls):
        query = """
        SELECT * FROM books
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        books = []
        for row in results:
            books.append(cls(row))
        return books
    
    @classmethod
    def create_book(cls, data):
        query = """
        INSERT INTO books (title, num_of_pages)
        VALUES (%(title)s, %(num_of_pages)s)
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def get_one_book(cls, data):
        query = """
        SELECT * FROM books
        LEFT JOIN favorites 
        ON books.id = favorites.book_id
        Left JOIN authors
        ON authors.id = favorites.author_id
        WHERE books.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        books = cls(results[0])
        for row in results:
            if row['authors.id'] == None:
                break
            data = {
                'id': row['authors.id'],
                'name': row['name'],
                'created_at': row['authors.created_at'],
                'updated_at': row['authors.updated_at']
            }
            books.authors_who_favorite.append(author.Author(data))
        return books
    
    @classmethod
    def unfavorite_books(cls, data):
        query = """
        SELECT * FROM books
        WHERE books.id
        NOT IN (SELECT book_id FROM favorites
        WHERE author_id = %(id)s )
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        books = []
        for row in results:
            books.append(cls(row))
        return books