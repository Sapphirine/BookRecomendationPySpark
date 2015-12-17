from flask import Flask,render_template, session, request, redirect, url_for, send_from_directory
from cloudDatabaseUtil import loginReader, registerReader, rateBook, getRating
from app import BigDataProcessor
import os, sys

os.environ['PYSPARK_PYTHON'] = sys.executable

app = Flask(__name__)
sparkCore = BigDataProcessor()

app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

'''index entry'''
@app.route("/",methods=['GET'])
def index():
	if 'username' in session:
		return render_template('index.html')
	else:
		return render_template('login.html')

'''login entry'''
@app.route("/login",methods=['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if(loginReader(username, password)):
			session['username'] = username
			return redirect(url_for('index'))
		else:
			return render_template('login.html')
	else:
		return render_template('login.html')

'''logout'''
@app.route("/logout",methods=['GET','POST'])
def logout():
	session.clear()
	return redirect(url_for('index'))

'''register function'''
@app.route("/register",methods=['GET','POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if (registerReader(username, password)):
			return render_template('login.html')
		else:
			return render_template('register.html')
	else:
		return render_template('register.html')

@app.route("/getRecommendation",methods=['GET'])
def getRecommendation():
	if (len(getRating(session['username']))==0):
		return sparkCore.collaborativeFilter([(0,1,5)])
	else:
		return sparkCore.collaborativeFilter(getRating(session['username']))

@app.route("/rate",methods=['POST'])
def rate():
	if (rateBook(session['username'], request.form['bookid'], request.form['score'])):
		return "rate successful"
	else:
		return "rate fail"


@app.route('/<path:path>')
def send_js(path):
	if path.endswith('png'):
		return send_from_directory('lib/images', path)
	else:
		return send_from_directory('./', path)

if __name__ == "__main__":
    app.run(port = 5004)