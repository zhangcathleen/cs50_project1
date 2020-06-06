import requests

import json

res = requests.get("https://www.goodreads.com/book/review_counts.json",
                   params={"key": "yGgwZLPLZpqS8IAGXcPA", "isbns": "9781632168146"})
print(res.json())
