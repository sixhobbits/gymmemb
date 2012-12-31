import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import sqlite3
import index
import datetime


# Set up log for current session
fn = "logs\\" + str(datetime.datetime.now()).replace(":",".") + ".txt"
f = open(fn, 'w')


UPLOAD_FOLDER = os.getcwd() + '\\static'
print UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['jpg','jpeg','gif','png'])

# init database
conn = sqlite3.connect("members.db")
cursor = conn.cursor()
conn.text_factory = str


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
		   
		   
@app.route('/info', methods=['GET','POST'])
def info():
	try:
		if request.method == 'GET':
			return render_template("manage.html", d="none")
		else:
			mid = request.form['id']
			if mid == "":
				f.write("no info submitted\n")
				return render_template("manage.html",d="none")
			f.write("%s\n" % (mid))
			search_by_id = True
			try:
				mid = int(mid)
				search_by_id = True
			except:	
				f.write("couldn't convert to int. Surname search?\n")
				mid = str(mid)
				search_by_id = False
			if search_by_id:
				f.write("executing ID query\n")
				cursor.execute("SELECT * FROM members WHERE number=%s;" % mid)
				f.write("executed select\n")
				member = cursor.fetchone()
				if(member):
					f.write("member found in database\n")
					# Global member to pass to iframe
					global m
					m = {'num':member[0], 'fname':member[1] , 'sname':member[2], 'phone':member[4],'photo':"/static/" + member[3], 'account':member[5]}
					return render_template("manage.html",d="member_ok")
				else:
					return render_template("manage.html",d="not_found")
				return render_template("manage.html",d="none")
			# Searching by surname -- first three letters
			else:
				f.write("Query by Surname\n\n")
				cursor.execute("SELECT * FROM members WHERE last_name like '%s';" % (mid + '%'))
				f.write("Query successful\n\n")
				global matches
				matches = cursor.fetchall()
				if not matches:
					return render_template("manage.html",d="not_found")
				else:
					return render_template("manage.html", d="names")
	except: # Not getting paid enough to deal nicely with errors...
		return render_template('manage.html',err="focusandinform('none')")

@app.route('/namematches')
def namematches():
	global matches
	return render_template("namematches.html", members=matches, nummems=len(matches))

@app.route('/memberinvalid')
def memberinvalid():
	return render_template("memberinvalid.html")

@app.route('/memberfine')
def memberfine():
		global m
		return render_template("memberok.html",m=m)
		

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
	return render_template("authenticate.html", err="focusandinform('none')")

@app.route('/auth', methods=['GET','POST'])	
def auth():
	if request.form['pw'] == "gareth":
		return render_template("manage.html",err="focusandinform('none')")
	else:
		return render_template("authenticate.html", err="focusandinform('try_again')")
	

@app.route('/newmember',methods=['GET','POST'])
def newmember():
	try:
		print "checking member number"
		cursor.execute("SELECT * FROM members WHERE number=%s;" % (request.form['num']))
		exists = cursor.fetchone()
		if exists:
			print "duplicate member number"
			return render_template('manage.html',err="focusandinform('dup_num')")
		print "newmember"
		print "uploading file"
		print request.files
		file = request.files['pic']
		print "that worked"
		if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				print "saving..."
				print os.path.join(app.config["UPLOAD_FOLDER"])
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				print "saved"
		# Make sure member number is not already in use
		print "inserting into databse"
		sqlstring = "INSERT INTO members VALUES (%d,'%s','%s','%s','%s','%s')" % (int(request.form['num']),request.form['first'],request.form['last'],file.filename,request.form['phone'], True)
		print sqlstring
		cursor.execute(sqlstring)
		print ("executed")
		conn.commit()
		print "commited"
		return render_template('manage.html',err="focusandinform('added')")
	except: # Not getting paid enough to deal nicely with errors...
		return render_template('manage.html',err="focusandinform('none')")

	
@app.route('/removemember', methods=['GET','POST'])
def removemember():
	try:
		print("removing member")
		cursor.execute("DELETE FROM members WHERE number = %s;" % (int(request.form['dnum'])))
		conn.commit()
		print "successfully removed"
		return render_template('manage.html',err="focusandinform('deleted')")
	except: # Not getting paid enough to deal nicely with errors...
		return render_template('manage.html',err="focusandinform('none')")


@app.route('/toggleaccount', methods=['GET','POST'])
def toggleaccount():
	try:
		print "toggling account"
		mnum = int(request.form['tnum'])
		cursor.execute("SELECT account_paid FROM members WHERE number=%s" % (mnum))
		accountpaid = cursor.fetchone()[0]
		print accountpaid
		if accountpaid == "True":
			cursor.execute("UPDATE members SET account_paid='False' WHERE number=%s" %(mnum))
		else:
			cursor.execute("UPDATE members SET account_paid='True' WHERE number=%s" % (mnum))
		conn.commit()
		return render_template('manage.html',err="focusandinform('toggled')")
	except: # Not getting paid enough to deal nicely with errors...
		return render_template('manage.html',err="focusandinform('none')")
		
	

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)