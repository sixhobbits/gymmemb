# index.py
# python 2.7
# Flask webapp, designed to be run locally
# Author Gareth Dwyer, garethdwyer@gmail.com
# December 2012
# Basic membership authentication system.
# 	Uses Sqlite3 to keep a database of members
#   Then uses html webforms to check member number
#   against database.
#=========================================================

from flask import Flask
from flask import render_template
from flask import request
import os
import sqlite3
import jinja2.ext # This is not included by cxfreeze
import datetime


# Set up log for current session
fn = "logs\\" + str(datetime.datetime.now()).replace(":",".") + ".txt"
f = open(fn, 'w')


# init database
f.write("connecting to database...\n")
conn = sqlite3.connect("members.db")
cursor = conn.cursor() 
f.write("init flask.\n")
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template("index.html", d="none")
	else:
		mid = request.form['id']
		if mid == "":
			f.write("no info submitted\n")
			return render_template("index.html",d="none")
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
				return render_template("index.html",d="member_ok")
			else:
				return render_template("index.html",d="not_found")
			return render_template("index.html",d="none")
		# Searching by surname -- first three letters
		else:
			f.write("Query by Surname\n\n")
			cursor.execute("SELECT * FROM members WHERE last_name like '%s';" % (mid + '%'))
			f.write("Query successful\n\n")
			global matches
			matches = cursor.fetchall()
			if not matches:
				return render_template("index.html",d="not_found")
			else:
				return render_template("index.html", d="names")

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
		
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
