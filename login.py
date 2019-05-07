import flask 
import sqlite3
from flask import render_template

app = flask.Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

import flask_login

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# Our mock database for login.
users = {'admin': {'password': 'admin'}}

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

@app.route('/')
def home():
	return flask.redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
    	return render_template('login.html')
        # return '''
        #        <form action='login' method='POST'>
        #         <input type='text' name='email' id='email' placeholder='email'/>
        #         <input type='password' name='password' id='password' placeholder='password'/>
        #         <input type='submit' name='submit'/>
        #        </form>
        #        '''

    email = flask.request.form['email']
    if email not in users:
    	return render_template('error.html',message="wrong credentials")
    	
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return render_template('error.html',message="wrong credentials")


@app.route('/protected')
@flask_login.login_required
def protected():
    return flask.redirect('/dash')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('error.html',message="logged out")

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('error.html',message="unauthorized access")

# @app.route('/dashboard', methods=['GET', 'POST'])
# def dashboard():
# 	if flask.request.method == 'GET':
# 		conn = sqlite3.connect("med.db")
# 		c=conn.cursor()
# 		x1=c.execute("SELECT * from record where admitted='Y'")
		
# 		conn.commit()
# 		conn.close()
# 		return render_template('dash.html',x=x1)

@app.route('/dash', methods=['GET','POST'])
def dash():
	if flask.request.method =='GET':
		conn = sqlite3.connect("med.db")
		c=conn.cursor()
		x=c.execute("SELECT * from record where admitted='Y'")
		return render_template('dash.html',x=x)

	
	id=flask.request.form['id']
	return flask.redirect('/patient/'+id)	

@app.route('/create')
def create():

	conn = sqlite3.connect("med.db")
	c=conn.cursor()
	x=c.execute("SELECT * from record ORDER BY patientid")
	for row in x:
		y=row[0]
	y=y+1
	x=c.execute("INSERT into record values("+str(y)+",'','','M','','','','','','','','','','')")
	conn.commit()
	conn.close()
	return flask.redirect('/edit/'+str(y))


@app.route('/patient/<id>')
def profile(id):
    
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
@flask_login.login_required
def edit(id):
	if flask.request.method == 'GET':
		
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
	
	conn = sqlite3.connect("med.db")
	c=conn.cursor()
	x = c.execute("update record set name='"+name+"', age ='"+age+"' ,gender ='"+gender+"', location = '"+loc+"' ,history ='"+his+"', allergies='"+alle+"' ,symptoms ='"+sym+"', bloodgroup='"+bg+"', haemoglobin="+hb+" ,insurance='"+ins+"' ,admitted ='"+adm+"' ,danger ='"+dan+"', medication ='"+med+"' where patientid='"+id+"'" )
	x=c.execute("UPDATE record set danger='Y' where haemoglobin<'10.0'");
	conn.commit()
	conn.close()
	return flask.redirect('/patient/'+id)	

