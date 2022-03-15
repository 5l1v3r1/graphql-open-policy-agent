import sys
from app import db

from flask import request, session

# Models
class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(60),nullable=True)
    maker = db.Column(db.String(60),nullable=True)
    color = db.Column(db.String(60),nullable=True)
    price = db.Column(db.Integer,nullable=True)
    tier = db.Column(db.String(10), nullable=True)
    discountcode = db.Column(db.String(10), nullable=True)

