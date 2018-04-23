from flask import Flask,request,redirect,render_template,flash,session

from datetime import datetime
import re
import bcrypt

from mysqlconnection import MySQLConnector
app = Flask(__name__)

app.secret_key = "vsdkjnfskj/nsknjscdckj"

mysql = MySQLConnector(app, 'login')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-._]+@[a-zA-Z0-9+-._]+\.[a-zA-Z]+$')


@app.route('/')
def user():

	return render_template('login.html',users=mysql.query_db("SELECT * FROM users"))

@app.route('/validate', methods=['POST'])
def create():

	valid = True
	#for all

	if request.form["first_name"]=='' or request.form["last_name"]=='' or request.form["email"]=='' or request.form["email"]=='' or request.form["confirm"]=='':
		flash("Please fill out all fields")
	#for first name
	
	if len(request.form["first_name"])< 2:
		flash("First name must be 2 characters or longer")
		valid = False
	elif  not request.form["first_name"].isalpha():
		flash("Name field cannot have numbers")
		valid=False

	#for last name
	
	if len(request.form["last_name"])< 2:
		flash("Last name must be 2 characters or longer")
		valid = False
	elif  not request.form["last_name"].isalpha():
		flash("Name field cannot have numbers")
		valid=False

	# f0r email
	
	if not EMAIL_REGEX.match(request.form["email"]):
		flash("Invalid Email")
		valid = False
	#for password

	if len(request.form["password"])<8:
		flash("password must be 8 characters or long")
		valid=False
	#for confirm password

	if request.form["password"] != request.form["confirm"]:
		flash("Password donot match")
		valid=False

	if not valid:
		return redirect('/')


	else:

		query="INSERT INTO users (first_name,last_name,email,password,created_at,updated_at)VALUES(:first_name,:last_name,:email,:password,NOW(),NOW())"


	data={
		'first_name':request.form['first_name'],
		'last_name':request.form['last_name'],
		'email':request.form['email'],
		'password': bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())
	}
	# print data
	mysql.query_db(query,data)	

	return redirect('/success')


@app.route('/success')
def display():
	return render_template('loginresult.html', users=mysql.query_db("SELECT * FROM users"))

@app.route('/login_page', methods=['POST'])
def login():
	
	my_query=mysql.query_db("SELECT * FROM users WHERE email = :email", {"email": request.form['email']})  
	if len(my_query)>0:
		if my_query[0][u'password']==request.form['password']:
			if  bcrypt.checkpw(request.form["password"].encode(), users[0]['password'].encode()):
				return redirect('/success')
		else:
			flash('Invalid Password')
			return redirect('/')
	else:
		flash('Email doest exit')
		return redirect('/')

	 

app.run(debug=True)


