import os
from flask import Flask, session, render_template, jsonify, request, redirect, url_for
# from models import *
from goodreads import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text, select

from flask_sqlalchemy import SQLAlchemy

from datetime import timedelta

# export FLASK_APP=application.py
# export DATABASE_URL = postgres://xhwfyyyajrayzc:98be0231bd360be4522c1e5afcec40a58d1ab3999c9f9457a9e1d21d182edd55@ec2-34-232-147-86.compute-1.amazonaws.com: 5432/db51ts8th98q5a
# export FLASK_DEBUG=1

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# DEBUG = True
wrongLogin = "Try Again - username or password does not match"
db = SQLAlchemy()

# Configure session to use filesystem
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Secret Key
app.secret_key = os.urandom(12)
# Lifetime of this session
app.permanent_session_lifetime = timedelta(minutes=20)
db.init_app(app)
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# Returns the selected book information from the book table
def select_book(isbn):
    book_table = db.execute(
        "SELECT * FROM books WHERE isbn = :isbn",
        {"isbn": isbn})
    if book_table.rowcount == 0:
        return render_template("error.html", message="No book with this isbn on table select_book", isbn=isbn)
    return book_table.fetchall()


# Inserts a rating and review into the book table
def insert_review(isbn, note, rating):
    if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).rowcount == 0:
        return render_template("error.html", message="No book with this isbn on table insert_review", isbn=isbn)
    db.execute("INSERT INTO reviews (rating, isbn, note) VALUES (:rating, :isbn, :note)",
               {"rating": int(rating), "isbn": isbn, "note": note})
    db.commit()
    # return "success"


# Selects the reviews for the corresponding isbn book
def select_review(isbn):
    review_table = db.execute(
        "SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn})
    if review_table.rowcount == 0:
        return 0
    return review_table.fetchall()


# Returns the information from the GoodReads API
def goodreads_api(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "yGgwZLPLZpqS8IAGXcPA", "isbns": isbn})
    try:
        json = res.json()
    except:
        return render_template("error.html", message="No book with this name on gr", isbn=isbn)
    return json


@app.route("/", methods=["POST", "GET"])
def index():
    if 'user' not in session:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            potato_table = db.execute(
                "SELECT * FROM potatos WHERE log = :log", {"log": username})
            # print("posted")
            if potato_table.rowcount == 1:
                # print("selected user")
                # print(potato_table.fetchall())
                potato_pass = db.execute(
                    "SELECT pass FROM potatos WHERE log = :log", {"log": username})
                if potato_pass == password:
                    session['user'] = username
                    return "wohoo looged in <br> <a href=\"/logout\">Logout</a> <br> <a href=\"/main\">continue</a>"
                else:
                    return render_template("index.html", message=wrongLogin)

            elif potato_table.rowcount > 1:
                return "beep boop error - <a href=\"/\">try again</a>"
            else:
                return render_template("index.html", message=wrongLogin)
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")


@ app.route("/logout")
def logout():
    session.pop("user", None)
    print("logged out")
    return redirect("/")


@ app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # check if this username already exists
        name = db.execute(
            "SELECT * FROM potatos WHERE log = :log", {"log": username})
        if name.rowcount > 0:
            return render_template("register.html", message="Sorry, this user already exists")
        db.execute("INSERT INTO potatos (log, pass) VALUES (:username, :password)", {
                   "username": username, "password": password})
        db.commit()
        return "registered account! <a href=\"/\">login</a>"
    else:
        return render_template("register.html")


@ app.route("/main", methods=["GET", "POST"])
def main():
    return render_template("main.html")


# List all the books on the site
@ app.route("/display")
def display():
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("display.html", books=books)


# Searches for the book with the corresponding isbn or title or author
@ app.route("/book", methods=["POST"])
def book():

    search = request.form.get("search")
    if db.execute("SELECT * FROM reviews WHERE isbn = :search", {"search": search}).rowcount != 0:
        # isbn = search
        return books(search)
    elif db.execute("SELECT isbn FROM books WHERE (title LIKE :search) OR (author LIKE :search);", {"search": f'%{search}%'}) != 0:
        result = db.execute("SELECT * FROM books WHERE (title LIKE :search) OR (author LIKE :search);", {
            "search": f'%{search}%'}).fetchall()
        vooks = []
        for line in result:
            vooks.append(line["isbn"])
        return results(vooks, search)


# Dispaly the books that are a result of the search
@ app.route("/results")
def results(vooks, search):
    if len(vooks) == 0:
        return render_template("results.html", message="There are no results with matching terms. \n Try again")
    else:
        books = []
        for v in vooks:
            book = db.execute(
                "SELECT * FROM books WHERE isbn = :v", {"v": v}).fetchall()
            books = books + book
            # print(book)
        # print(books)
        return render_template("results.html", books=books, search=search)


# Returns the information for the given book with isbn
@ app.route("/books/<isbn>")
def books(isbn):

    goodreads = goodreads_api(isbn)
    book_table = select_book(isbn)
    review_table = select_review(isbn)

    info = {}
    json_info = goodreads['books'][0]
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
            if line['rating']:
                rating = rating + int(line['rating'])
                i = 1+i
                usr = {'potato': line['potato'],
                       'note': line['note'], 'rating': line['rating']}
            else:
                rating = rating
                usr = {'potato': line['potato'], 'note': line['note']}
            info['review'].append(usr)
        info['rating'] = round(rating/i, 2)
    return render_template("book.html", info=info)


# Submits the review form
@ app.route("/form", methods=["GET", "POST"])
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
            insert_review(isbn, rev, rating)
            res = select_review(isbn)
            return redirect(url_for('submission', isbn=isbn))
    return render_template("form.html")


# Displays the success message after submitting a review
@ app.route('/submission/<isbn>', methods=["GET"])
def submission(isbn):
    return render_template("submission.html", message="success!", var=isbn)


# Returns a json about the book with the isbn
@ app.route("/api/books/<isbn>")
def book_api(isbn):
    book_table = select_book(isbn)
    goodreads = goodreads_api(isbn)

    json_info = goodreads['books'][0]

    return jsonify({
        "title": book_table[0][1],
        "author": book_table[0][2],
        "year": book_table[0][3],
        "isbn": isbn,
        "review_count": json_info["ratings_count"],
        "average_score": json_info["average_rating"]
    })
