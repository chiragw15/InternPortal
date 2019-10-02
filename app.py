#!/usr/bin/env python

import json

import os
from os import environ as env
from sys import argv

import bottle
from bottle import get, run, request, response, static_file

from py2neo import Graph, authenticate
#from urllib.parse import urlparse, urlunparse


'''from neo4jrestclient.client import GraphDatabase

from urllib.parse import urlparse, urlunparse

bottle.debug(True)

url = urlparse(GRAPHENEDB_URL)
url_without_auth = urlunparse((url.scheme, "{0}:{1}".format(url.hostname, url.port), url.path, None, None, None))

gdb = GraphDatabase(url_without_auth, username = url.username, password = url.password)'''


graph = Graph("http://neo4j:mamakancha@localhost:7474/db/data/")

#graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
#graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
#graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
#graph = Graph(graphenedb_url, user=graphenedb_user, password=graphenedb_pass, bolt = True, secure = True, http_port = 24789, https_port = 24780)

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
        results = graph.run(
        "create (n:professor{name:" + "\"" + name + "\"" + "," + 
                            "research:" + "\"" + research + "\"" + "," +
                            "email:" + "\"" + email + "\"" + "," +
                            "password:" + "\"" + password + "\"" + "," +
                            "vacancy:" + "\"" + vacancy + "\"" + "});"
        )
        print(results)
        return {"response": "Registered successfully"}

bottle.run(host='0.0.0.0', port=argv[1])
