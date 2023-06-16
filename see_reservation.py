from cassandra.cluster import Cluster
import uuid

def see_reservation(res_id):
    cluster = Cluster(['172.18.0.3'])
    session = cluster.connect('library')

    select_stmt = session.prepare("SELECT * FROM reservation WHERE res_id = ?")
    binded_select = select_stmt.bind([res_id])
    result = session.execute(binded_select)

    if result:
        for values in result:
            print("Book ID =",values[1])
            print("Borrowed at =", values[3])
            print("Give back date =", values[2])
            print("Title =", values[4])
            print("User name =", values[5])

    else:
        print("No such reservation")

    session.shutdown()
    cluster.shutdown()

def main():
    try:
        res_id = uuid.UUID(input("Enter Reservation ID: "))

        see_reservation(res_id)
    except Exception:
        print("Wrong formatinho")

if __name__ == "__main__":
    main()