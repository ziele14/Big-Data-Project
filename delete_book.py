from cassandra.cluster import Cluster
import uuid

def delete_book(book_id):
    cluster = Cluster(['172.18.0.2'])
    session = cluster.connect('library')

    select_stmt = session.prepare("SELECT * FROM books WHERE book_id = ?")
    binded_select = select_stmt.bind([book_id])
    result = session.execute(binded_select)

    if result:
        delete_stmt = session.prepare("DELETE FROM books WHERE book_id = ?")
        binded_delete = delete_stmt.bind([book_id])

        session.execute(binded_delete)

        print("Book deleted successfully!")
    else:
        print("There's no such book in the database")

    session.shutdown()
    cluster.shutdown()


def main():
    try:
        book_id = uuid.UUID(input("Enter Book ID: "))
        delete_book(book_id)
    except Exception:
        print("Wrong format (it has to be a uuid)")


if __name__ == "__main__":
    main()
