import os
from flask import Flask, session, render_template, jsonify, request
from models import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

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


@app.route("/reviews", methods=["POST"])
def reviews():
    # List all the books on the site
    reviews = Review.query.all()
    books = Book.query.all()
    return render_template("reviews.html",  books=books, reviews=review)


@app.route("/form", methods=["POST"])
def form():
    return render_template("form.html")
