""" 
Author: Adefemi Adegite
Date written: 02/07/24 
Assignment: M04 Lab-Case Study
 """
from flask_sqlalchemy import SQLAlchemy

# initializing a flask application
app = Flask(__name__)

#setting up path for sqlite db where data will be stored
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

#initializing SQLAlchemy class which will interact with database.
db = SQLAlchemy(app)

# Book model class for each row in our table.
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'book_name': self.book_name,
            'author': self.author,
            'publisher': self.publisher
        }

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()  # returns all rows present in the table as objects of Book class.
    # get the dict representation of book class and create http response.
    return jsonify([book.to_dict() for book in books]) 

# Get a specific book. Here book_id can be passed in url.
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # query the db to get row with specific book_id
    book = Book.query.get(book_id) 
    if book:
        return jsonify(book.to_dict())
    else:
        return jsonify({'message': 'Book not found'})

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    # create an instance of book class for insertion in db
    new_book = Book(
        book_name=request.json['book_name'],
        author=request.json['author'],
        publisher=request.json['publisher']
    )
    db.session.add(new_book)  # insert the data in db to create new entry
    db.session.commit()  # commit the query to save it in db
    return jsonify(new_book.to_dict())

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)  # get the book object that needs updation
    if book:
        # fetch new values from request object and update the book object
        book.book_name = request.json.get('book_name', book.book_name)
        book.author = request.json.get('author', book.author)
        book.publisher = request.json.get('publisher', book.publisher)
        db.session.commit()
        return jsonify(book.to_dict())
    else:
        return jsonify({'message': 'Book not found'})

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id) # fetch the book object to be deleted
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted'})
    else:
        return jsonify({'message': 'Book not found'})

if __name__ == '__main__':
    # this is the entry point of code. Here we create the DB and run the application.
    with app.app_context():
        db.create_all()
    app.run(debug=True)