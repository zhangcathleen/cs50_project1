import requests

import json


class GoodRead:

    def __init__(self, isbn):
        key = "yGgwZLPLZpqS8IAGXcPA"
        id = isbn
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": key, "isbn": id})

    def print_json(self):
        print(res.json())
