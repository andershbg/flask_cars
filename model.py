"""
model.py
--------
Implements the model for our website by simulating a database.

Note: although this is nice as a simple example, don't do this in a real-world
production setting. Having a global object for application data is asking for
trouble. Instead, use a real database layer, like
https://flask-sqlalchemy.palletsprojects.com/.
"""

import json

import logging

logging.basicConfig(level=logging.DEBUG,format='%(process)d-%(levelname)s-%(message)s')


def load_db():
    with open("cars_db.json", encoding='utf-8') as f:
        return json.load(f)


def save_db():
    with open("cars_db.json", 'w') as f:
        return json.dump(db, f)


def get_db_car(db, regnr):
    #sorted db, not read from disk
    index = 0
    for car in range(len(db)):
        if db[car]['regnr'] == regnr:
            return index
        index = index + 1
    return -1


def get_db_cars(owner):
    with open("db.json", encoding='utf-8') as f:
        cars = json.load(f)
        ownerlist = []
        for car in cars:
            if car['owner'] == owner:
                ownerlist.append(db_pers['name'])
        return ownerlist


def load_db_pers():
    with open("pers_db.json", encoding='utf-8') as f:
        return json.load(f)


def save_db_pers():
    with open("pers_db.json", 'w') as f:
        return json.dump(db_pers, f)


def get_db_pers_id(name):
    with open("pers_db.json", encoding='utf-8') as f:
        persons = json.load(f)
#        logging.debug(regnr)
        index = 0
        for person in persons:
            if person['name'] == name:
                return index
            index = index + 1
        return -1


def list_sort_cars(e):
    return e["brand"].upper()


db = load_db()
db_pers = load_db_pers()