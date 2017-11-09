#!/usr/bin/env python

import json

from bottle import get, run, request, response, static_file
from py2neo import Graph

graph = Graph("http://neo4j:Chirag@1234@localhost:7474/db/data/")

@get("/")
def get_index():
    return static_file("index.html", root="static")

@get("/register") 
def get_register():
	return static_file("register.html", root="static")

@get("/register.json")
def get_registerJSON():
    try:
        name = request.query["name"]
        research = request.query["research"]
        email = request.query["email"]
        password = request.query["password"]
        vacancy = request.query["vacancy"]
    except KeyError:
        return {"respose": "Some error occurred"}
    else:
        results = graph.cypher.execute(
        "create (n:professor{name:" + "\"" + name + "\"" + "," + 
                            "research:" + "\"" + research + "\"" + "," +
                            "email:" + "\"" + email + "\"" + "," +
                            "password:" + "\"" + password + "\"" + "," +
                            "vacancy:" + "\"" + vacancy + "\"" + "});"
        )
        print(results)
        return {"response": "Registered successfully"}


if __name__ == "__main__":
    run(port=8080)
