from flask import Flask,render_template, session, request, redirect, url_for, send_from_directory
app = Flask(__name__)

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
		#if 1==1:
		session['username'] = username
		return redirect(url_for('index'))
		#else:
		#return render_template('login.html')
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
		#if success
		#return render_template('login.html')
		#else:
		return render_template('register.html')
	else:
		return render_template('register.html')

@app.route("/getRecommendation",methods=['GET'])
def getRecommendation():
	return "recommendation list in json"

@app.route("/rate",methods=['POST'])
def rate():
	return "user x rate y on movie z"

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

if __name__ == "__main__":
    app.run(port = 5003)