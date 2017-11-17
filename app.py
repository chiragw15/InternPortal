#!/usr/bin/env python

import json

import os
from os import environ as env
from sys import argv

import bottle
from bottle import get, run, request, response, static_file

from py2neo import Graph, authenticate
#from urllib.parse import urlparse, urlunparse

'''
from neo4jrestclient.client import GraphDatabase

from urllib.parse import urlparse, urlunparse

bottle.debug(True)

url = urlparse(GRAPHENEDB_URL)
url_without_auth = urlunparse((url.scheme, "{0}:{1}".format(url.hostname, url.port), url.path, None, None, None))

gdb = GraphDatabase(url_without_auth, username = url.username, password = url.password)

'''
graph = Graph("http://neo4j:Chirag@1234@localhost:7474/db/data/")

#graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
#graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
#graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
#graph = Graph(graphenedb_url, user=graphenedb_user, password=graphenedb_pass, bolt = True, secure = True, http_port = 24789, https_port = 24780)

@get("/")
def get_index():
    return static_file("index.html", root="static")

@get("/professor")
def get_professor():
    return static_file("professor.html", root="static")

@get("/student")
def get_student():
    return static_file("student.html", root="static")

@get("/register") 
def get_register():
	return static_file("register.html", root="static")

@get("/login") 
def get_login():
    return static_file("login.html", root="static")

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

@get("login.json")
def get_loginJSON():
    try:
        email = request.query["email"]
        password = request.query["password"]
    except KeyError:
        return {"respose": "Some error occurred"}
    else:
        #results = graph.cypher.execute( * )
        #enter graph query here (in place of star in above line) to find prof from email and password
        return {"response":"Success"}

@get("/getProfs.json")
def get_prof_list():
    try: 
        research = request.query["research"]
    except KeyError:
        return {"response":"No professor found"}
    else:
        #results = graph.cypher.execute( * )
        #enter graph query here (in place of star in above line) to find prof from research area
        return {"response":"Success"}



bottle.run(host='0.0.0.0', port=argv[1])
