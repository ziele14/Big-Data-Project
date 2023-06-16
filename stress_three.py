import concurrent.futures
import random
import threading
import time
from cassandra.cluster import Cluster
from make_reservation import add_reservation

male_names = [
    "Jakub",
    "Kacper",
    "Mateusz",
    "Adam",
    "Michał",
    "Filip",
    "Szymon",
    "Jan",
    "Paweł",
    "Adrian",
    "Karol",
    "Piotr",
    "Dawid",
    "Kamil",
    "Tomasz",
    "Grzegorz",
    "Rafał",
    "Patryk",
    "Łukasz",
    "Marcin"
]


def stress_test(book_list):
    for book_id in book_list:
        start_time = time.time()
        add_reservation(random.choice(male_names), book_id)
        end_time = time.time()
        response_time = end_time - start_time
        response_times.append(response_time)


cluster = Cluster(['172.18.0.3'])
session = cluster.connect('library')

books = session.execute("SELECT book_id FROM books")
books = [row.book_id for row in books]

num_threads = 2
threads = []
response_times = []

thread_one = threading.Thread(target=stress_test, args=[books])
threads.append(thread_one)

thread_two = threading.Thread(target=stress_test, args=[books])
threads.append(thread_two)

thread_one.start()
thread_two.start()

for thread in threads:
    thread.join()

cluster.shutdown()
average_response_time = sum(response_times) / len(response_times)
print(f"Average Response Time: {average_response_time:.2f} seconds")