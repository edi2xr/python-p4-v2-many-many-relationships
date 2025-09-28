from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey, Date, DateTime, String
from sqlalchemy.orm import relationship, backref

# Naming convention for Alembic migrations
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Association table for Employee ↔ Meeting many-to-many
employee_meeting = Table(
    'employee_meeting',
    db.Model.metadata,
    Column('employee_id', Integer, ForeignKey('employees.id'), primary_key=True),
    Column('meeting_id', Integer, ForeignKey('meetings.id'), primary_key=True)
)

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)

    meetings = relationship(
        "Meeting",
        secondary=employee_meeting,
        back_populates="employees"
    )

    assignments = relationship("Assignment", back_populates="employee")

    def __repr__(self):
        return f"<Employee {self.id}, {self.name}, {self.hire_date}>"

class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String, nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String, nullable=False)

    employees = relationship(
        "Employee",
        secondary=employee_meeting,
        back_populates="meetings"
    )

    def __repr__(self):
        return f"<Meeting {self.id}, {self.topic}, {self.scheduled_time}, {self.location}>"

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    budget = db.Column(db.Integer, nullable=False)

    assignments = relationship("Assignment", back_populates="project")

    def __repr__(self):
        return f"<Project {self.id}, {self.title}, {self.budget}>"

# Association object for Employee ↔ Project with extra fields
class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    role = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)

    employee = relationship("Employee", back_populates="assignments")
    project = relationship("Project", back_populates="assignments")

    def __repr__(self):
        return f"<Assignment {self.id}, Employee {self.employee_id}, Project {self.project_id}, Role {self.role}>"
