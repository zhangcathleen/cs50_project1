import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)


class Potato(db.Model):
    __tablename__ = "potatos"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)
    ratings_gr = db.Column(db.Float, nullable=False)
    ratings_web = db.Column(db.Float)
    potato = db.Column(db.Integer, db.ForeignKey("potatos.id"), nullable=False)
    note = db.Column(db.String)
