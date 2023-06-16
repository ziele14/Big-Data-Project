import signal
import sys
import random
import threading
import time
from cassandra.cluster import Cluster
from make_reservation import add_reservation
from update_reservation import update_reservation

total_requests = 0
responses = []
running = True

cluster = Cluster(['172.18.0.3'])
session = cluster.connect('library')

def calculate_average_response_time(responses, total_requests):
    if total_requests > 0:
        average_response_time = sum(responses) / total_requests
        print(f"Average response time: {average_response_time:.2f} seconds")

def reservation_actor():
    global total_requests, responses
    while running:
        select_stmt = session.prepare("SELECT book_id FROM books")
        results = session.execute(select_stmt)
        book_ids = [row.book_id for row in results]

        start_time = time.time()
        add_reservation('antek', random.choice(book_ids))
        end_time = time.time()
        response_time = end_time - start_time
        responses.append(response_time)
        total_requests += 1

def update_actor():
    global total_requests, responses
    while running:
        select_stmt = session.prepare("SELECT res_id FROM reservation")
        result = session.execute(select_stmt)
        if result:
            res_ids = [row.res_id for row in result]
            start_time = time.time()
            update_reservation('antek', random.choice(res_ids),'give back')
            end_time = time.time()
            response_time = end_time - start_time
            responses.append(response_time)
            total_requests += 1

def signal_handler(sig, frame):
    global running
    running = False
    print("\nProgram interrupted. Calculating average response time...")
    calculate_average_response_time(responses, total_requests)
    print("Total requests: ", total_requests)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

reservation_thread = threading.Thread(target=reservation_actor)
reservation_thread.start()

update_thread = threading.Thread(target=update_actor)
update_thread.start()

reservation_thread.join()
update_thread.join()
