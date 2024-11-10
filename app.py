from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = 'employees'

    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    address = db.Column("address", db.String(100))

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def to_dictionary(self):
        return {"id": self._id, "name": self.name, "address": self.address}
    
db.create_all()

@app.route("/view", methods = ["GET"])
def get():
    employees = Employee.query.all()
    
    return jsonify([employee.to_dictionary() for employee in employees])

@app.route("/add", methods = ["POST"])
def add():
    data = request.get_json()
    name = data.get("name")
    address = data.get("address")

    newEmployee = Employee(name = name, address = address)
    db.session.add(newEmployee)
    db.session.commit()

    return "201"
# 201 = success