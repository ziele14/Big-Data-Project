import random
import threading
import time
from cassandra.cluster import Cluster
from make_reservation import add_reservation
from read_book import read_book
from see_reservation import see_reservation
from update_reservation import update_reservation

cluster = Cluster(['172.18.0.2'])
session = cluster.connect('library')


def stress_test():
    for _ in range(50):
        select_stmt = session.prepare("SELECT book_id FROM books")
        results = session.execute(select_stmt)
        book_ids = [row.book_id for row in results]

        select_stmt = session.prepare("SELECT res_id FROM reservation")
        result = session.execute(select_stmt)
        res_ids = [row.res_id for row in result]

        start_time = time.time()
        action = random.choice(["add", "see", "update","see_book"])
        if action == "add":
            item1 = random.choice(book_ids)
            add_reservation('antek', item1)
        elif action == "see":
            if result:
                item2 = random.choice(res_ids)
                see_reservation(item2)
            else:
                print("There aren't any reservations yet")
        elif action == "update":
            item2 = random.choice(res_ids)
            item3 = random.choice(['extend', 'give back'])
            if result:
                update_reservation('antek', item2, item3)
            else:
                print("There aren't any reservations yet")
        elif action == "see_book":
            item = random.choice(book_ids)
            read_book(item)
        end_time = time.time()
        response_time = end_time - start_time
        response_times.append(response_time)


num_threads = 4
threads = []
response_times = []

for i in range(num_threads):
    thread = threading.Thread(target=stress_test)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

cluster.shutdown()
average_response_time = sum(response_times) / len(response_times)
print(f"Average Response Time: {average_response_time:.2f} seconds")