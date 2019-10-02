#!/usr/bin/env python

import json

import os
from os import environ as env
from sys import argv
from Crypto.Cipher import AES

import bottle
from bottle import get, run, request, response, static_file

from py2neo import Graph, authenticate
#from urllib.parse import urlparse, urlunparse



from neo4jrestclient.client import GraphDatabase

'''
from neo4jrestclient.client import GraphDatabase

from urllib.parse import urlparse, urlunparse

bottle.debug(True)

url = urlparse(GRAPHENEDB_URL)
url_without_auth = urlunparse((url.scheme, "{0}:{1}".format(url.hostname, url.port), url.path, None, None, None))

gdb = GraphDatabase(url_without_auth, username = url.username, password = url.password)'''



graph = Graph("http://neo4j:mamakancha@localhost:7474/db/data/")

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

        results = graph.run(

        results = graph.cypher.execute(

        "create (n:professor{name:" + "\"" + name + "\"" + "," + 
                            "research:" + "\"" + research + "\"" + "," +
                            "email:" + "\"" + email + "\"" + "," +
                            "password:" + "\"" + password + "\"" + "," +
                            "vacancy:" + "\"" + vacancy + "\"" + "});"
        )
        print(results)
        return {"response": "Registered successfully"}

@get("/login.json")
def get_loginJSON():
    try:
        email = request.query["email"]
        password = request.query["password"]
    except KeyError:
        return {"respose": "Some error occurred"}
    else:
        results = graph.cypher.execute( 
        "match (n: professor) where n.email = \"" + email + 
        "\" and n.password = \"" + password + "\" return n;" 
        )
        response.content_type = "application/json"
        print(results)
        c = 0
        for row in results:
            c = c+1
        if(c == 0):
            return {"response":"Incorrect username or password"}
        else:
            obj = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
            message = results[0].n.properties['password']
            ciphertext = obj.encrypt(message)

            #obj2 = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
            #obj2.decrypt(ciphertext)

            return {"response":"Login Success",
                    "name": results[0].n.properties['name'],
                    "email": results[0].n.properties['email'],
                    "research": results[0].n.properties['research'],
                    "vacancy": results[0].n.properties['vacancy'],
                    "api-token": ciphertext.decode('ISO-8859-1')}

@get("/getProfs.json")
def get_prof_list():
    try: 
        research = request.query["research"]
    except KeyError:
        return {"response":"No professor found"}
    else:
        results = graph.cypher.execute( 
        "match (n: professor) where n.research = \"" + research + "\" return n;" 
        )
        response.content_type = "application/json"
        print(results)
        return json.dumps([{"professors": row.n.properties} for row in results])


bottle.run(host='0.0.0.0', port=argv[1])
