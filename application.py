import os
from flask import Flask, session, render_template, jsonify, request
from models import *
from goodreads import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text

# export FLASK_APP=application.py
# export DATABASE_URL = postgres://xhwfyyyajrayzc:98be0231bd360be4522c1e5afcec40a58d1ab3999c9f9457a9e1d21d182edd55@ec2-34-232-147-86.compute-1.amazonaws.com: 5432/db51ts8th98q5a
# export FLASK_DEBUG=1

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
    if request.method == "POST":
        if review is None:
            return render_template("error.html", message="No book with this isbn")
        return redirect(url_for("book"))

    # List all the books on the site
    # reviews = Review.query.all()
    # books = Book.query.all()
    return render_template("book.html", books=books)


@app.route("/book", methods=["POST"])
def book():

    isbn = request.form["isbn_number"]
    return books(isbn)


@app.route("/books/<isbn>")
def books(isbn):

    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "yGgwZLPLZpqS8IAGXcPA", "isbns": isbn})
    try:
        json = res.json()
    except:
        return render_template("error.html", message="No book with this name on gr", isbn=isbn)

    try:
        t = (isbn,)
        # print(t)
        cmd = "SELECT * FROM books WHERE isbn = :x "
        # x = isbn
        book_table = db.execute(text(cmd), {'x': isbn}).fetchall()
        db.commit()
    except Exception as e:
        return render_template("error.html", message="No book with this isbn on table", isbn=isbn, e=e)

    info = {}
    json = res.json()
    json_info = json['books'][0]
    info['isbn'] = isbn
    info['isbn13'] = json_info['isbn13']
    info['review_count'] = json_info['reviews_count']
    info['average_rating'] = json_info['average_rating']
    # print(book_table)
    # print(book_table.json())
    info['title'] = book_table[0][1]
    info['author'] = book_table[0][2]
    info['year'] = book_table[0][3]

    # print(info)
    return render_template("book.html", info=info)


@ app.route("/form", methods=["POST"])
def form():
    return render_template("form.html")
