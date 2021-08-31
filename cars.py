from flask import (Flask, render_template, abort, jsonify, request,
                    redirect, url_for, escape)

import logging

from model import db, save_db, db_pers, save_db_pers, get_db_car, get_db_pers, get_db_person

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,format='%(process)d-%(levelname)s-%(message)s')

@app.route("/")
def welcome():
    logging.debug('logging is active')
    return render_template(
        "welcome.html",
        cars=db
    )


@app.route("/car/<int:index>")
def car_view(index):
    try:
        car = db[index]
        owner = get_db_pers(car['regnr'])
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
        if len(name) and len(brand) and len(model) and len(regnr):
            regnr = str(escape(request.form['regnr'])).upper()
            person = {"name": name,
                      "regnr": regnr}
            db_pers.append(person)
            save_db_pers()

            car = {"brand": brand,
                  "model": model,
                  "regnr": regnr}
            db.append(car)
            save_db()
            return redirect(url_for('car_view', index=len(db) - 1))
        else:
            return render_template("add_car.html")
    else:
        return render_template("add_car.html")

@app.route("/get_car", methods=["GET", "POST"])
def get_car():
    if request.method == "POST":
        regnr = str(escape(request.form['regnr'])).upper()
#        logging.debug(regnr)
        if len(regnr):
            index = get_db_car(regnr)
            if index > -1:
                owner = get_db_pers(regnr)
                logging.debug(db_pers[owner]['name'])
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


@app.route("/add_person", methods=["GET", "POST"])
def add_person():
    if request.method == "POST":
        name = str(escape(request.form['name'])).upper()
        regnr = str(escape(request.form['regnr'])).upper()
        person = {"name": name,
                 "regnr": regnr}
        db_pers.append(person)
        save_db_pers()
        return redirect(url_for('person_view', index=len(db_pers) - 1))
    else:
        return render_template("add_person.html")


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
            ownerlist = get_db_person(name)
            logging.debug(ownerlist)
            cars = []
            for regnr in ownerlist:
                logging.debug(regnr)
                index = get_db_car(regnr)
                cars.append(db[index])
                logging.debug(cars)

            return render_template("get_person.html",
                                   cars=cars,
                                   owner=name)

        return render_template("get_person.html")
    else:
        return render_template("get_person.html")

@app.route("/api/car/")
def api_car_list():
    return jsonify(db)


@app.route("/api/owner/")
def api_owner_list():
    return jsonify(db_pers)

