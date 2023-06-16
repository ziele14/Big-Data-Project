#!/bin/bash

docker exec -it cassandra1 cqlsh -e "TRUNCATE library.books;"

docker exec -it cassandra1 cqlsh -e "TRUNCATE library.reservation;"
