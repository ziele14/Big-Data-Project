from cassandra.cluster import Cluster
import uuid


def add_book(isbn, title, author, description):

    cluster = Cluster(['172.18.0.2'])
    session = cluster.connect('library')

    book_id = generate_book_id()

    adder = session.prepare("INSERT INTO books (book_id, isbn, title, author, description) VALUES (?, ?, ?, ?, ?)")
    binded = adder.bind([book_id, isbn, title, author, description])

    session.execute(binded)

    session.shutdown()
    cluster.shutdown()

    print("Book added successfully with the following id = ", book_id)


def generate_book_id():
    return uuid.uuid4()


def main():
    isbn = input("Enter ISBN: ")
    title = input("Enter title: ")
    author = input("Enter author: ")
    description = input("Enter description: ")

    add_book(isbn, title, author, description)


if __name__ == "__main__":
    main()
