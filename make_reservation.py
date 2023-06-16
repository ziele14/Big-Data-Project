import cassandra
from cassandra.cluster import Cluster
import uuid
from datetime import date, timedelta


def add_reservation(name, book_id):
    cluster = Cluster(['172.18.0.2'])
    session = cluster.connect('library')

    select_stmt = session.prepare("SELECT * FROM books WHERE book_id = ?")
    binded_select = select_stmt.bind([book_id])
    result = session.execute(binded_select)
    if result:
        for values in result:
            title = values[5]
            borrow_date = values[2]

        if type(borrow_date) == cassandra.util.Date:
            print("This book is already being borrowed")
        else:
            reservation_id = generate_reservation_id()

            current_date = date.today()
            end_date = current_date + timedelta(days=30)

            updater = session.prepare("UPDATE books SET borrow_date = ? WHERE book_id = ?")
            binded_update = updater.bind([end_date, book_id])

            session.execute(binded_update)

            adder = session.prepare("INSERT INTO reservation (res_id, book_id, borrow_end, borrow_start, title, user) VALUES (?, ?, ?, ?, ?, ?)")
            binded = adder.bind([reservation_id, book_id, end_date, current_date, title, name])
            session.execute(binded)

            session.shutdown()
            cluster.shutdown()
            print("Reservation has been made with ID = ", reservation_id)
    else:
        print("No such book mate")


def generate_reservation_id():
    return uuid.uuid4()


def main():
    try:
        name = input("Enter username: ")
        book_id = uuid.UUID(input("Enter Book ID: "))
        if name != '':
            add_reservation(name, book_id)
        else:
            print("Username not valid")
    except(Exception):
        print("Wrong format")


if __name__ == "__main__":
    main()
