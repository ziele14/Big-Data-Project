from cassandra.cluster import Cluster
import uuid

def read_book(book_id):
    cluster = Cluster(['172.18.0.2'])
    session = cluster.connect('library')

    select_stmt = session.prepare("SELECT * FROM books WHERE book_id = ?")
    binded_select = select_stmt.bind([book_id])
    result = session.execute(binded_select)

    if result:
        for values in result:
            print("Title =",values[5])
            print("Author =", values[1])
            print("Description =", values[3])
            print("ISBN =", values[4])
            print("Borrow date =", values[2])

    else:
        print("Something went wrong, the book is not here chap")

    session.shutdown()
    cluster.shutdown()

def main():
    try:
        book_id = uuid.UUID(input("Enter Book ID: "))

        read_book(book_id)
    except Exception:
        print("Wrong format")

if __name__ == "__main__":
    main()