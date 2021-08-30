from flask import (Flask, render_template, abort, jsonify, request,
                    redirect, url_for, escape)

import logging

from model import db, save_db, db_pers

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
        return render_template("car.html",
                               car=car,
                               index=index,
                               max_index=len(db)-1)
    except IndexError:
        abort(404)


@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    if request.method == "POST":
        brand = str(escape(request.form['brand']))
        model = str(escape(request.form['model']))
        car = {"brand": brand,
              "model": model}
        db.append(car)
        save_db()
        return redirect(url_for('car_view', index=len(db) - 1))
    else:
        return render_template("add_car.html")

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

@app.route("/api/car/")
def api_car_list():
    return jsonify(db)

@app.route("/add_person", methods=["GET", "POST"])
def add_person():
    if request.method == "POST":
        name = str(escape(request.form['name']))
        person = {"name": name}
        db_pers.append(person)
        save_person_db()
        return redirect(url_for('person_view', index=len(db_pers) - 1))
    else:
        return render_template("add_person.html")
