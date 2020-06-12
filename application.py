import os
from flask import Flask, session, render_template, jsonify, request, redirect, url_for
# from models import *
from goodreads import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text, select

from flask_sqlalchemy import SQLAlchemy

# export FLASK_APP=application.py
# export DATABASE_URL = postgres://xhwfyyyajrayzc:98be0231bd360be4522c1e5afcec40a58d1ab3999c9f9457a9e1d21d182edd55@ec2-34-232-147-86.compute-1.amazonaws.com: 5432/db51ts8th98q5a
# export FLASK_DEBUG=1

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# DEBUG = True

db = SQLAlchemy()

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


def select_book(isbn):
    book_table = db.execute(
        "SELECT * FROM books WHERE isbn = :isbn",
        {"isbn": isbn})
    if book_table.rowcount == 0:
        return render_template("error.html", message="No book with this isbn on table select_book", isbn=isbn)
    return book_table.fetchall()
    # try:
    #     cmd = "SELECT * FROM books WHERE isbn = :x "
    #     book_table = db.execute(text(cmd), {'x': isbn}).fetchall()
    #     db.commit()
    # except Exception as e:
    #     return render_template("error.html", message="No book with this isbn on table", isbn=isbn, e=e)
    # return book_table


def insert_review(isbn, note, rating):
    if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).rowcount == 0:
        return render_template("error.html", message="No book with this isbn on table insert_review", isbn=isbn)
    db.execute("INSERT INTO reviews (rating, isbn, note) VALUES (:rating, :isbn, :note)",
               {"rating": int(rating), "isbn": isbn, "note": note})
    db.commit()
    return "success"
    # try:
    #     # cmd = 'INSERT INTO reviews (link, note) VALUES ('
    #     print(num)
    #     print(rev)
    #     cmd = reviews.insert().values(link=num, note=rev)
    #     # review_table = db.execute(text(cmd), {'x': num, 'y': rev})
    #     # review_table = db.execute(text(cmd) + num + ', ' + y + ')')
    #     review_table = db.execute(cmd)
    #     db.commit()
    #     print(review_table.inserted_primary_key)
    #     return
    # except Exception as e:
    #     print('exception insert_review')
    #     return render_template("error.html", message="No book with this isbn on table submit review", isbn=num, e=e)


def select_review(isbn):
    review_table = db.execute(
        "SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn})
    if review_table.rowcount == 0:
        return 0
        # return render_template("error.html", message="No book with this isbn on table select review", isbn=isbn)
    return review_table.fetchall()
    # try:
    #     print('select_review')
    #     cmd = select([reviews.c.link, reviews.c.note])
    #     # cmd = 'SELECT note FROM reviews WHERE link = '
    #     # review_table = db.execute(text(cmd), {'x': isbn}).fetchall()
    #     # review_table = db.execute(text(cmd) + x).fetchall
    #     review_table = db.execute(cmd)
    #     db.commit()
    #     return review_table
    # except Exception as e:
    #     print('exception select_review')
    #     print(e)
    #     return render_template("error.html", message="No book with this isbn on table select review", isbn=isbn, e=e)
    # # return review_table


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main", methods=["POST"])
def main():
    return render_template("main.html")


@app.route("/display", methods=["GET", "POST"])
def display():

    # List all the books on the site
    # reviews = Review.query.all()
    # books = Book.query.all()
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("display.html", books=books)


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

    book_table = select_book(isbn)
    review_table = select_review(isbn)

    info = {}
    json_info = json['books'][0]
    info['isbn'] = isbn
    info['isbn13'] = json_info['isbn13']
    info['review_count'] = json_info['reviews_count']
    info['average_rating'] = json_info['average_rating']
    info['title'] = book_table[0][1]
    info['author'] = book_table[0][2]
    info['year'] = book_table[0][3]
    info['review'] = []

    if review_table == 0:
        print("no reviews")
    else:
        rating = 0
        i = 0
        for line in review_table:
            rating += line['rating']
            i += 1
            usr = {'potato': line['potato'], 'note': line['note']}
            info['review'].append(usr)
            print(str(line['potato']) + " : " + str(line['note']))
        info['rating'] = round(rating/i, 2)

    # print(info)
    return render_template("book.html", info=info)


@app.route("/form", methods=["GET", "POST"])
def form():
    isbn = request.form.get("isbn_review")
    rev = request.form.get('text_review')
    rating = request.form.get('rating')
    book_table = db.execute(
        "SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn})
    if request.method == "POST":
        if book_table.rowcount == 0:
            return render_template("error.html", message="No book with this isbn form", isbn=isbn)
        else:
            print(insert_review(isbn, rev, rating))
            res = select_review(isbn)
            return redirect(url_for('submission', isbn=isbn))
    return render_template("form.html")


@app.route('/submission/<isbn>', methods=["GET"])
def submission(isbn):
    return render_template("submission.html", message="success!", var=isbn)
