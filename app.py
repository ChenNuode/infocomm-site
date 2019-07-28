from flask import *
import sqlite3, security
#import mailing

UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# disallow html, php files

mysiteurl = "http://127.0.0.1:5000"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'RafflesIndianCulturalClub'

conn = sqlite3.connect('club_data.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS members(Id integer NOT NULL PRIMARY KEY AUTOINCREMENT, username text NOT NULL, password text NOT NULL, email text NOT NULL, linkgenerated text NOT NULL, confirmed boolean NOT NULL);")
c.execute("CREATE TABLE IF NOT EXISTS posts(Id integer NOT NULL PRIMARY KEY AUTOINCREMENT, username text NOT NULL, postdate date NOT NULL, title text NOT NULL,  imagename text NOT NULL, article text NOT NULL);")

conn.commit()
conn.close()

@app.route("/")
def home():
	if 'username' in session:
		print("Hello",session['username'])
		return render_template("index.html",login = True, username = session['username'])
	else:
		return render_template("index.html",login = False)

@app.route("/login", methods=['POST', 'GET'])
def login():
	if request.method=='POST':
		with sqlite3.connect("club_data.db") as con:
			cur = con.cursor()
			data = cur.execute('SELECT username, password, confirmed FROM members WHERE username=? OR email=?', (request.form["usr"],request.form["usr"])).fetchall()
			if data != []:
				check = False
				for item in data:
					if security.checkpwd(request.form['pw'],item[1]):
						finaldata = item
						check = True
						break
				if check == False:
					return render_template("login.html", failed = 2)

				if finaldata[2] == 0:
					return render_template("login.html", failed = 1)
				else:
					if "rme" in request.form:
						print("cookie set")
						session['username'] = finaldata[0]
					else:
						print("no cookies")
						session['username'] = finaldata[0]

					if 'target' not in session:
						return redirect(url_for('home'))
					else:
						target = session['target']
						session.pop('target',None)
						return redirect(url_for(target))
			else:
				return render_template("login.html", failed = 2)
	else:
		#get request nothing happen
		session.pop('username', None)
		return render_template("login.html", failed = 3)

@app.route("/logout", methods=['GET'])
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route("/signup", methods=['POST', 'GET'])
def signup():
	if request.method=='POST':
		name = request.form['usr']
		email = request.form['email']

		with sqlite3.connect("club_data.db") as con:
			cur = con.cursor()
			if cur.execute('SELECT username, email FROM members WHERE username=? OR email=?', (name,email)).fetchall() != []:
				return render_template("signup.html", failed = True)
			else:
				password = security.generatehash(request.form['pw'])
				link = security.linkgen()
				while cur.execute('SELECT linkgenerated FROM members WHERE linkgenerated=?', (link,)).fetchone() != None:
					link = security.linkgen()
				
				#status = mailing.send_email(email,name, mysiteurl + "/authemail/" + link)
				status = True

				if status == True:
					cur.execute('INSERT INTO members (username,password,email,linkgenerated,confirmed) VALUES (?,?,?,?,1)', (name,password, email,link))
					con.commit()
					#return "Your account has been created, a confirmation link has been sent to your email."
					return "Your account has been created."
				else:
					return "An error occured while sending the email"

	else:
		#get request nothing happen
		session.pop('username', None)
		return render_template("signup.html", failed = False)

"""
@app.route("/authemail/<code>", methods=['GET'])
def confirmemail(code):
	with sqlite3.connect("club_data.db") as con:
		cur = con.cursor()
		data = cur.execute('SELECT confirmed FROM members WHERE linkgenerated=?', (code,)).fetchone()
		if data == None:
			return "Error auth link"
		elif data[0] == 1:
			return "Email is already confirmed"
		else:
			cur.execute("UPDATE members SET confirmed=? WHERE linkgenerated=?",(1,code))
			con.commit()
			return "Email confirmed successfully"

"""

@app.route("/about")
def about():
	return "about"

@app.route("/members")
def members():
	return "members"

@app.route("/project")
def projectshowcase():
	return "project"

#temporary dashboard
@app.route("/dashboard", methods=['POST', 'GET'])
def controlcenter():
	if 'username' in session:
		if request.method == "GET":
			return "<h1>In development, to logout click <a href='/logout'>here</a></h1>"

		else:
			#verifyposter()
			return "In development"
	else:
		return redirect(url_for('login'))		


@app.route("/<somewhere>", methods=['GET'])
def give_error(somewhere):
	return render_template("404.html")

"""
### Login Protected pages ####

def verifyposter():
	pass

@app.route("/dashboard", methods=['POST', 'GET'])
def controlcenter():
	if request.method == "GET":
		if 'username' in session:
			return render_template('dashboard.html', username = session['username'])
		else:
			session['target'] = 'controlcenter'
			return redirect(url_for('login'))
	else:
		verifyposter()
		return "in development"
	
@app.route("/article/new", methods=['POST', 'GET'])
def contentadd():
	if request.method == "GET":
		if 'username' in session:
			return render_template('contentadd.html', username = session['username'])
		else:
			session['target'] = 'contentadd'
			return redirect(url_for('login'))
	else:
		verifyposter()
		return "in development"


### Experiement section
@app.route("/test", methods=['POST', 'GET'])
def testing(filename='clubimg.png'):
	return send_file(app.config['UPLOAD_FOLDER'] + filename, attachment_filename = filename)

@app.route("/clear")
def clearall():
	with sqlite3.connect("club_data.db") as con:
		cur = con.cursor()
		cur.execute("DELETE FROM members")
		con.commit()
	return "done"
"""

if __name__ == "__main__":
	app.run(debug=True)
