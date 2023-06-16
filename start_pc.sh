#!/bin/bash

docker start cassandra1 cassandra2

sleep 30

python3 fill_library.py
