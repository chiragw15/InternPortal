#!/usr/bin/env python

import json

from bottle import get, run, request, response, static_file
from py2neo import Graph

graph = Graph("http://neo4j:Chirag@1234@localhost:7474/db/data/")

@get("/")
def get_index():
    graph.cypher.execute(
        "create (n:test{name:\"Chirag2\"})"
    )
    print("query called")
    return static_file("index.html", root="static")

if __name__ == "__main__":
    run(port=8080)
