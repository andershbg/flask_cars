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


def load_db():
    with open("cars_db.json", encoding='utf-8') as f:
        return json.load(f)


def save_db():
    with open("cars_db.json", 'w') as f:
        return json.dump(db, f)


def load_db_pers():
    with open("pers_db.json", encoding='utf-8') as f:
        return json.load(f)


db = load_db()
db_pers = load_db_pers()