import uuid
import threading
import time
import random
from cassandra.cluster import Cluster
from read_book import read_book

num_requests = 120
concurrency = 3

def send_request(item):
    try:
        start_time = time.time()
        read_book(item)
        end_time = time.time()
        response_time = end_time - start_time
        response_times.append(response_time)
    except(Exception):
        print("ooops")


cluster = Cluster(['172.18.0.2'])
session = cluster.connect('library')


select_stmt = session.prepare("SELECT book_id FROM books")
results = session.execute(select_stmt)
book_ids = [row.book_id for row in results]

threads = []
response_times = []

for _ in range(concurrency):
    for _ in range(num_requests // concurrency):
        item1 = random.choice(book_ids)
        thread = threading.Thread(target=send_request, args=[item1])
        threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

average_response_time = sum(response_times) / len(response_times)
print(f"Average Response Time: {average_response_time:.2f} seconds")
