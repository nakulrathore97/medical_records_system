import flask
from flask import render_template

app = flask.Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

import flask_login

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# Our mock database for login.
users = {'foo@bar.tld': {'password': 'secret'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/dashboard')
def dashboard():
    import sqlite3
    conn = sqlite3.connect("med.db")
    c=conn.cursor()
    x=c.execute("SELECT * from record where admitted='Y'")
    conn.commit()
    conn.close()
    return render_template('dash.html',x=x)



# @app.route('/create')
# def create():
	
@app.route('/patient/<id>')
@flask_login.login_required
def profile(id):
    import sqlite3
    conn = sqlite3.connect("med.db")
    c=conn.cursor()
    flag=False
    x = c.execute("SELECT * FROM record where patientid="+id)
    for row in x:
        id=row[0]  
        name=row[1]
        age=row[2]
        gender=row[3]
        loc=row[4]
        his=row[5]
        alle=row[6]
        sym=row[7]
        bg=row[8]
        hb=row[9]
        ins=row[10]
        adm=row[11]
        dan=row[12]
        med=row[13]
        flag=True
    conn.commit()
    conn.close()
    if flag:  
        return render_template('profile.html',id=id,name=name,age=age,gender=gender,loc=loc,his=his,alle=alle,sym=sym,bg=bg,hb=hb,ins=ins,adm=adm,dan=dan,med=med)
    else:
        return "patient id not in database"

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
	if flask.request.method == 'GET':
		import sqlite3
		conn = sqlite3.connect("med.db")
		c=conn.cursor()
		flag=False
		x = c.execute("SELECT * FROM record where patientid="+id)
		for row in x:
			id=row[0]
			name=row[1]
			age=row[2]
			gender=row[3]
			loc=row[4]
			his=row[5]
			alle=row[6]
			sym=row[7]
			bg=row[8]
			hb=row[9]
			ins=row[10]
			adm=row[11]
			dan=row[12]
			med=row[13]
			flag=True
		conn.commit()
		conn.close()
		if flag:
			return render_template('edit.html',id=id,name=name,age=age,gender=gender,loc=loc,his=his,alle=alle,sym=sym,bg=bg,hb=hb,ins=ins,adm=adm,dan=dan,med=med)
		else:
			return "id not found"

	id=flask.request.form['id']
	name=flask.request.form['name']
	age=flask.request.form['age']
	gender=flask.request.form['gender']
	loc=flask.request.form['loc']
	his=flask.request.form['his']
	alle=flask.request.form['alle']
	sym=flask.request.form['sym']
	bg=flask.request.form['bg']
	hb=flask.request.form['hb']
	ins=flask.request.form['ins']
	adm=flask.request.form['adm']
	dan=flask.request.form['dan']
	med=flask.request.form['med']
	import sqlite3
	conn = sqlite3.connect("med.db")
	c=conn.cursor()
	x = c.execute("update record set name='"+name+"', age ='"+age+"' ,gender ='"+gender+"', location = '"+loc+"' ,history ='"+his+"', allergies='"+alle+"' ,symptoms ='"+sym+"', bloodgroup='"+bg+"', haemoglobin="+hb+" ,insurance='"+ins+"' ,admitted ='"+adm+"' ,danger ='"+dan+"', medication ='"+med+"' where patientid='"+id+"'" )
	conn.commit()
	conn.close()
	return flask.redirect('/patient/'+id)	
