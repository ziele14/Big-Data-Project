import pandas as pd

from add_book import add_book

df = pd.read_csv('books.csv', usecols=['title', 'isbn', 'authors'], nrows=50)

for _, row in df.iterrows():
        title = row['title']
        isbn = row['isbn']
        authors = row['authors']
        add_book(isbn, title, authors, 'a book innit')





