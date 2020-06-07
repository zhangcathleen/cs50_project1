CREATE TABLE books (
    isbn VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE potatos (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL, 
    password VARCHAR NOT NULL
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    link VARCHAR NOT NULL REFERENCES books(isbn), -- the isbn
    ratings_gr FLOAT NOT NULL,
    ratings_web FLOAT,
    potato INTEGER NOT NULL REFERENCES potatos(id),
    note TEXT

);

ALTER TABLE reviews DROP COLUMN book;