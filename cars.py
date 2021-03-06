from flask import (Flask, render_template, abort, jsonify, request,
                    redirect, url_for, escape)

import logging

from model import db, save_db, db_pers, save_db_pers, get_db_car, get_db_pers_id, list_sort_cars

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,format='%(process)d-%(levelname)s-%(message)s')

@app.route("/")
def welcome():
    logging.debug('logging is active')
    db.sort(key=list_sort_cars)
    return render_template(
        "welcome.html",
        cars=db
    )


@app.route("/car/<int:index>")
def car_view(index):
    try:
        car = db[index]
        owner = car['owner']
        return render_template("car.html",
                               car=car,
                               owner=db_pers[owner]['name'],
                               index=index,
                               max_index=len(db)-1)
    except IndexError:
        abort(404)


@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    if request.method == "POST":
        name = str(escape(request.form['name'])).upper()
        brand = str(escape(request.form['brand']))
        model = str(escape(request.form['model']))
        regnr = str(escape(request.form['regnr'])).upper()
        exist = get_db_car(db, regnr)
        if exist < 0 and len(name) and len(brand) and len(model) and len(regnr):
            owner = get_db_pers_id(name)
            if owner < 0:
                person = {"name": name}
                db_pers.append(person)
                save_db_pers()
                owner = len(db_pers) - 1

            car = {"brand": brand,
                  "model": model,
                  "regnr": regnr,
                  "owner": owner}
            db.append(car)
            save_db()
            db.sort(key=list_sort_cars)
            index = get_db_car(db, regnr)
            return redirect(url_for('car_view', index=index))
        else:
            return render_template("add_car.html")
    else:
        return render_template("add_car.html")

@app.route("/get_car", methods=["GET", "POST"])
def get_car():
    if request.method == "POST":
        regnr = str(escape(request.form['regnr'])).upper()
        logging.debug(regnr)
        if len(regnr):
            index = get_db_car(db, regnr)
            logging.debug(index)
            if index > -1:
                logging.debug(db[index])
                owner = db[index]['owner']
                logging.debug(owner)
                car = db[index]
                return render_template("car.html",
                                       car=car,
                                       owner=db_pers[owner]['name'],
                                       index=index,
                                       max_index=len(db) - 1)
        return render_template("get_car.html")
    else:
        return render_template("get_car.html")


@app.route("/remove_car/<int:index>", methods=["GET", "POST"])
def remove_car(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            if index > 0:
                return redirect(url_for('car_view', index=len(db) - 1))
            else:
                return redirect(url_for('welcome'))
        else:
            return render_template("remove_car.html", car=db[index])
    except IndexError:
        abort(404)


@app.route("/person/<int:index>")
def person_view(index):
    try:
        pers = db_pers[index]
        return render_template("person.html",
                               pers=pers,
                               index=index,
                               max_index=len(db_pers)-1)
    except IndexError:
        abort(404)


@app.route("/get_person", methods=["GET", "POST"])
def get_person():
    if request.method == "POST":
        name = str(escape(request.form['name'])).upper()
        if len(name):
            owner = get_db_pers_id(name)
            cars = []
            for index in range(len(db)):
                if db[index]['owner'] == owner:
                    cars.append(db[index])
                    logging.debug(db[index]['model'])

            return render_template("get_person.html",
                                   cars=cars,
                                   owner=name)

        return render_template("get_person.html")
    else:
        return render_template("get_person.html")

@app.route("/api/car/")
def api_car_list():
    db.sort(key=list_sort_cars)
    return jsonify(db)


@app.route("/api/owner/")
def api_owner_list():
    return jsonify(db_pers)

@app.route("/api/owner/<int:index>")
def api_owner_id_list(index):
    cars = []
    for x in range(len(db)):
        if db[x]['owner'] == index:
            cars.append(db[x])
    return jsonify(cars)
