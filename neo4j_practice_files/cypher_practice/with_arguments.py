#!/usr/bin/env python

'''
@authors: Neo4j AuraDB (https://console.neo4j.io/#databases/88d63c49/detail),  includes function additions from Katie Christensen

Practice with the Cypher query language on user input.
'''

import logging
import argparse
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class App():
    def __init__(self, uri, user, password, label, name):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, label, name):
        with self.driver.session() as session:
            result = session.read_transaction(self._create_and_return_node, label, name)
            for row in result:
                print("Created ", label, ": {row}".format(row=row))

    @staticmethod
    def _create_and_return_node(tx, label, name):   
        if label == 'Person':
            query = (
                "CREATE (p:Person {name: $name})"
                "RETURN p.name AS name"
            )
        if label == 'Movie':
            query = (
                "CREATE (m:Movie {title: $name})"
                "RETURN m.title AS name"
            )
        result = tx.run(query, name=name)
        return [row["name"] for row in result]

    def find_node(self, label, name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_node, label, name)
            if len(result) == 0:
                print("Could not find ", label,": ", name)
            else:
                for row in result:
                   print("Found ", label,": {row}".format(row=row))

    @staticmethod
    def _find_and_return_node(tx, label, name):
        if label == 'Person':
            query = (
                "MATCH (p:Person) "
                "WHERE p.name = $name "
                "RETURN p.name AS name"
            )
        if label == 'Movie':
            query = (
                "MATCH (m:Movie) "
                "WHERE m.title = $name "
                "RETURN m.title AS name"
            )
        result = tx.run(query, name=name)
        return [row["name"] for row in result]

    def remove_node(self, label, name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_remove_node, label, name)
            print("Removed ", label, " :", name)
    
    @staticmethod
    def _find_and_remove_node(tx, label, name):
        if label == 'Person':
            query = (
                "MATCH (p:Person) "
                "WHERE p.name = $name "
                "DETACH DELETE p"
            )
        if label == 'Movie':
            query = (
                "MATCH (m:Movie) "
                "WHERE m.title = $name "
                "DETACH DELETE m"
            )
        result = tx.run(query, name=name)
        return [row["name"] for row in result]

def parse_all_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-label",type=str,help="The node label: \"Person\", \"Movie\", (string) [default: \"Person\"]",default="Person")
    parser.add_argument("-name",type=str,help="The name property of the node, (string) [default: \"Name\"]",default="Name")

    return parser.parse_args()

def main():
    args = parse_all_args()

    uri = "neo4j+s://88d63c49.databases.neo4j.io"
    user = "neo4j"
    
    path = '../../password.txt'
    with open(path, "r") as f:
        for pwd in f:
            password = pwd

    name = args.name
    label = args.label
    app = App(uri, user, password, name, label)

    #example run:   ./with_arguments.py -label Person -name Katie
    app.remove_node(args.label, args.name)
    app.create_node(label, name)
    app.find_node(label, name)
    app.remove_node(args.label, args.name)
    app.find_node(args.label, args.name)

    app.close()

if __name__ == "__main__":
    main()