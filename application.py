import os
from flask import Flask, session, render_template, jsonify, request
from models import *
from goodreads import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

DEBUG = True

# Configure session to use filesystem
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main", methods=["POST"])
def main():
    return render_template("main.html")


@app.route("/display", methods=["POST"])
def display():
    # if request.method == "POST":
    #     isbn = request.form.get("isbn_number")
    #     review = GoodRead(isbn)
    #     if review is None:
    #         return render_template("error.html", message="No book with this isbn")

    #     result = review.print_json
    #     return render_template("book.html", result=result)

    # List all the books on the site
    # reviews = Review.query.all()
    # books = Book.query.all()
    return render_template("book.html", books=books)


@app.route("/book/<int:isbn_number>", methods=["POST"])
def book(review_id):

    isbn = request.form.get("isbn_number")
    review = GoodRead(isbn)
    if review is None:
        return render_template("error.html", message="No book with this isbn")

    result = review.get_res
    book_info = Book.query.filter(Book.isbn == isbn)
    print(book_info)
    return render_template("book.html", result=result, book=book_info, isbn=isbn)


@app.route("/form", methods=["POST"])
def form():
    return render_template("form.html")
