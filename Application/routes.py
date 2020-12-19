from Application import app
from flask import render_template, request, url_for, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from Application import users, issues

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if session.get('name'):
        flash("Already Logged In", "info")
        return redirect('/')

    if request.method == "POST":
        if users.find_one({'email':request.form['email']}):
            if check_password_hash(users.find_one({'email':request.form['email']})['password'], request.form['password']):
                # flash("Logged In","success")
                session['name'] = users.find_one({'email':request.form['email']})['name']
                session['email'] = request.form['email']
                return redirect("/")
            else:
                # flash("Incorrect Password", "danger")
                return redirect("/login")
        else:
            # flash("Email Not Found, Register Here", "danger")
            return redirect("/register")
    return render_template('login.html')    

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if session.get('name'):
        flash("Already Registered", "info")
        return redirect('/')

    if request.method == "POST":
        if users.find_one({'email':request.form['email']}):
            flash("Email Already Exist's","danger")
            return redirect("/register")

        else:    
            password = generate_password_hash(request.form['password'])
            users.insert_one({'name':request.form['name'], 'phone_number':request.form['phonenumber'], 'email':request.form['email'], 'password':password})
            flash("You are Successfully Registered","success")
            return redirect("/login")

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('name',None)
    session.pop('email',None)
    flash("Successfully logged out",'success')
    return redirect('/')
    