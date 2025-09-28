#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Employee, Meeting, Project, Assignment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

# Simple test route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Employee API!"})

# Optional: view employees
@app.route('/employees')
def get_employees():
    employees = Employee.query.all()
    return jsonify([{"id": e.id, "name": e.name, "hire_date": e.hire_date.isoformat()} for e in employees])

if __name__ == "__main__":
    app.run(port=5555)
