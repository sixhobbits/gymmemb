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

# init database
print "connecting to database..."
conn = sqlite3.connect("members.db")
print "done"
print "getting cursor"
cursor = conn.cursor()
print "done"
print "init flask."
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	print "index"
	if request.method == 'GET':
		print "rendering index"
		return render_template("index.html", d="none")
	else:
		global m
		try:
			mid = request.form['id']
			if mid == "":
				print "no info submitted"
				return render_template("index.html",d="none")
			mid = int(mid)
			print mid
			cursor.execute("SELECT * FROM members WHERE number=%d;" % mid)
			print "executed select"
			member = cursor.fetchone()
			if(member):
				print ("member found in database")
				# Global member to pass to iframe
				print "photo: %s" % member[3]
				m = {'num':member[0], 'fname':member[1] , 'sname':member[2], 'phone':member[4],'photo':"/static/" + member[3] }
				return render_template("index.html",d="member_ok")
			else:
				return render_template("index.html",d="not_found")
		except:	
			print "exception: probably non-integer id entered"
			return render_template("index.html",d="none")

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
