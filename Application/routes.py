from Application import app
from flask import render_template, request, url_for, flash, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from Application import db, users, issues, grid_fs
import base64

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about_us')
def aboutus():
    return render_template('aboutus.html')

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
    
@app.route('/addissue', methods = ["GET", "POST"])
def addissue():
    if request.method == "POST":
        if issues.find_one({'Title':request.form['title'], 'location':request.form['location'], 'time':request.form['time'], 'details':request.form['details'], 'name':session.get('name'), 'email':session.get('email')}):
            # flash("Email Already Exist's","danger")
            return redirect("/issues")

        else:
            with grid_fs.new_file(filename = request.form['image']) as fp:
                fp.write(request.data)
                file_id = fp._id
            if grid_fs.find_one(file_id) is not None:
                issues.insert_one({'Title':request.form['title'], 'location':request.form['location'], 'time':request.form['time'], 'details':request.form['details'], 'name':session.get('name'), 'email':session.get('email'), 'image':file_id})
            # flash("You are Successfully Registered","success")
            return redirect("/issues")
        
    return render_template('addissue.html')    

@app.route('/issues')
def allissues():
    informations = issues.find({})
    return render_template('issues.html', informations= informations)