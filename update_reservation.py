from cassandra.cluster import Cluster
import uuid
from datetime import  timedelta


def update_reservation(name, res_id, decision):
    cluster = Cluster(['172.18.0.2'])
    session = cluster.connect('library')

    select_stmt = session.prepare("SELECT * FROM reservation WHERE res_id = ?")
    binded_select = select_stmt.bind([res_id])
    result = session.execute(binded_select)
    if result:
        for values in result:
            book_id = values[1]
            user = values[5]
            borrow_end = values[2]

        if user != name:
            print("You got something mixed up")
        else:
            if decision == 'give back':
                delete_stmt = session.prepare("DELETE FROM reservation WHERE res_id = ?")
                binded_delete = delete_stmt.bind([res_id])
                session.execute(binded_delete)

                updater = session.prepare("UPDATE books SET borrow_date = NULL WHERE book_id = ?")
                binded_update = updater.bind([book_id])

                session.execute(binded_update)

                print("Everything went smoothly, cheers")
            elif decision == 'extend':

                new_date = borrow_end.date() + timedelta(days=7)
                updater = session.prepare("UPDATE reservation SET borrow_end = ? WHERE res_id = ?")
                binded_update = updater.bind([new_date, res_id])

                session.execute(binded_update)

                updater = session.prepare("UPDATE books SET borrow_date = ? WHERE book_id = ?")
                binded_update = updater.bind([new_date, book_id])
                session.execute(binded_update)

                session.shutdown()
                cluster.shutdown()
                print("It's updated")
    else:
        print("No such reservation mate")


def main():

    name = input("Enter username: ")
    res_id = uuid.UUID(input("Enter reservation ID: "))
    if name == '':
        print("Username not valid")
    else:
        decision = input("Do you want to give the book back or extend the time of borrowing? Type 'extend' or 'give back' : ")
        if decision == 'extend' or decision =='give back':
            update_reservation(name, res_id, decision)
        else:
            print("That's not a valid decision mate")


if __name__ == "__main__":
    main()
