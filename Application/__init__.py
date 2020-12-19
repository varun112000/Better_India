from flask import Flask
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


cluster = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
db = cluster["BetterIndia"]
users = db["Users"]
issues = db["Issues"]


from Application import routes