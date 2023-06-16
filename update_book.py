from cassandra.cluster import Cluster
import uuid


def update_book(book_id, isbn, title, author, description):
    cluster = Cluster(['172.18.0.3'])
    session = cluster.connect('library')

    select_stmt = session.prepare("SELECT * FROM books WHERE book_id = ?")
    binded_select = select_stmt.bind([book_id])
    result = session.execute(binded_select)

    if result:
        updater = session.prepare("UPDATE books SET isbn = ?, title = ?, author = ?, description = ? WHERE book_id = ?")
        binded_update = updater.bind([isbn, title, author, description, book_id])

        session.execute(binded_update)

        print("Book updated successfully!")
    else:
        print("There is no such book")

    session.shutdown()
    cluster.shutdown()


def main():
    try:
        book_id = uuid.UUID(input("Enter Book ID: "))
        isbn = input("Enter ISBN: ")
        title = input("Enter title: ")
        author = input("Enter author: ")
        description = input("Enter description: ")

        update_book(book_id, isbn, title, author, description)
    except Exception:
        print("Wrong format")

if __name__ == "__main__":
    main()
