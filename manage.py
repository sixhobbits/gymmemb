import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from member import Member
import sqlite3



UPLOAD_FOLDER = 'C:/Users/Gareth/Desktop/gymmemb/static'
ALLOWED_EXTENSIONS = set(['jpg','jpeg','gif','png'])

# init database
conn = sqlite3.connect("members.db")
cursor = conn.cursor()


# Request dashboard
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
	return render_template("manage.html")

@app.route('/newmember',methods=['GET','POST'])
def newmember():
	print "newmember"
	print "uploading file"
	print request.files
	file = request.files['pic']
	print "that worked"
        if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print "saving..."
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print "saved"
	print "inserting into databse"
	print request.form['num']
	print request.form['first']
	print request.form['last']
	print request.form['phone']
	print file.filename
	sqlstring = "INSERT INTO members VALUES (%d,'%s','%s','%s','%s')" % (int(request.form['num']),request.form['first'],request.form['last'],file.filename,request.form['phone'])
	print sqlstring
	cursor.execute(sqlstring)
	print ("executed")
	conn.commit()
	print "commited"
	return render_template('manage.html')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)