from Application import app
from flask import render_template, request, url_for, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

@app.route('/')
@app.route('/Home')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')    

@app.route('/register', methods = ['GET', 'POST'])
def register():
    return render_template('register.html')
