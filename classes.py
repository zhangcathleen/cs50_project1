

class Book:

    def __init__(self, isbn, title, author, year):

        # details about this book
        self.isbn = isbn

        self.title = title
        self.author = author
        self.year = year


# can be used to print all the reviews of this book
"""
    def print_info(self):
        print(f"Flight origin: {self.origin}")
        print(f"Flight destination: {self.destination}")
        print(f"Flight duration: {self.duration}")

        print()
        print("Passengers:")
        for passenger in self.passengers:
            print(passenger)
"""


class Review:
    def __init__(self, id, link, ratings_gr, ratings_web, user), note:
        self.id = id

        self.link = link
        self.ratings_gr = ratings_gr
        self.ratings_web = ratings_web
        self.user = user
        self.note = note

    def __repr__(self):
        return self.id
