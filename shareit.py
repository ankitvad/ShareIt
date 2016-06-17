from flask import Flask, request, g, redirect, url_for, abort, render_template, send_from_directory, flash
from werkzeug import secure_filename
from hashlib import md5
from PIL import Image
import sqlite3
import os
import time
import cleanComment
from adultscanner import get_skin_ratio as gsr
from PornPicDetector import detector as ppd
from trending import confidence as conf

DEBUG              = True
BASE_DIR           = open("dirLocation.txt").read().rstrip("\n")
UPLOAD_DIR         = BASE_DIR + '/pics'
DATABASE           = BASE_DIR + '/flaskgur.db'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config.from_object(__name__)


# Make sure extension is in the ALLOWD_EXTENSIONS set
def check_extension(extension):
	return extension in ALLOWED_EXTENSIONS

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

# Return a list of the last 25 uploaded images	
def get_last_pics():
	cur = g.db.execute('select filename from pics order by id desc limit 25')
	filenames = [row[0] for row in cur.fetchall()]
	return filenames

#Get Like and Dislike rating from the SQLite database.
def get_ratings(imageName):
	cur = g.db.execute('select likes,dislikes from pics where filename="'+imageName+'"')
	rating = cur.fetchall()
	return rating[0]# like = rating[0][0], dislike = rating[0][1]

#Update Ratings:
def updateRatings(filename,ratingType):
	if (ratingType == "l"):
		query = 'update pics set likes=likes+1 where filename="'+filename+'"'
	else:
		query = 'update pics set dislikes=dislikes+1 where filename="'+filename+'"'
	g.db.execute(query)
	g.db.commit()

#Get all Ratings:
def getRatings():
	cur = g.db.execute("select filename,likes,dislikes from pics")
	result = cur.fetchall()
	return result

#Get caption from database:
def get_caption(filename):
	cur = g.db.execute('select tags from caption where filename="'+filename+'"')
	result = cur.fetchall()
	return result

def searchImage(searchQuery):
	images = []
	query = "select filename,tags from caption"
	cur = g.db.execute(query)
	result = cur.fetchall()
	for stuff in result:
		if all(q in stuff[1] for q in searchQuery):
			images.append(str(stuff[0]))
	if images:
		return images
	else:
		return 0

#Get all comments on the specified image.
def get_comments(imageName):
	cur = g.db.execute('select comment from comments where filename="'+imageName+'"')
	tmp = cur.fetchall()
	comments = [str(row[0]) for row in tmp]
	return comments

#Post comment to sqlite:
def postComment(comment,url):
	query='insert into comments values("'+url+'","'+comment+'")'
	g.db.execute(query)
	g.db.commit()

# Insert filename into database
def add_pic(filename):
	g.db.execute('insert into pics (filename) values (?)', [filename])
	g.db.commit()

# Generate thumbnail image
def gen_thumbnail(filename):
	height = width = 200
	original = Image.open(os.path.join(app.config['UPLOAD_DIR'], filename))
	thumbnail = original.resize((width, height), Image.ANTIALIAS)
	thumbnail.save(os.path.join(app.config['UPLOAD_DIR'], 'thumb_'+filename))
	
# Taken from flask example app
@app.before_request
def before_request():
    g.db = connect_db()
    
# Taken from flask example app
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=['GET','POST'])
def upload_pic():
	if request.method == 'POST':
		file = request.files['file']
		try:
			extension = file.filename.rsplit('.', 1)[1].lower()
		except IndexError, e:
			print("1")
			abort(404)
		if file and check_extension(extension):
			# Salt and hash the file contents
			filename = md5(file.read() + str(round(time.time() * 1000))).hexdigest() + '.' + extension
			file.seek(0) # Move cursor back to beginning so we can write to disk
			file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
			test1 = gsr(UPLOAD_DIR+"/"+filename)
			test2 = ppd(UPLOAD_DIR+"/"+filename)
			if(test1 >= 0.30 or test2 == "adult"):
				x=[]
				x.append("Sorry the Image was considered as offensive.")
				x.append("http://localhost:5000/")
				return render_template('test.html', x=x)
			add_pic(filename)
			gen_thumbnail(filename)
			os.system("python /home/ankitvad/Research/Projects/check/webUI/CaptionGen/chainer_caption_generation-master/codes/submit_captions.py")
			return redirect(url_for('show_pic', filename=filename))
		else: # Bad file extension
			print("2")
			abort(404)
	else:
		return render_template('upload.html', pics=get_last_pics())

# Include support for ratings.
@app.route('/trending')
def trend_pics():
	allRanking = getRatings()
	ratings = []
	for item in allRanking:
		ratings.append([str(item[0]),item[1],item[2]])
	allRanking = []
	for item2 in ratings:
		allRanking.append([item2[0],conf(item2[1],item2[2])])
	allRanking.sort(key=lambda row: row[1],reverse=True)
	filenames = [x[0] for x in allRanking]
	return render_template('upload.html', pics=filenames)

#Get the image in API.
@app.route('/search')
def get_image():
	query = str(request.args.get('query', ''))
	query = query.split(" ")
	result = searchImage(query)
	if result:
		return render_template('upload.html', pics=result)
	else:
		x=[]
		x.append("Sorry no image found.")
		x.append("http://localhost:5000/")
		return render_template('search.html', x=x)


#SHow all images.
@app.route('/show')
def show_pic():
	filename = request.args.get('filename', '')
	rating = get_ratings(filename)
	comments = get_comments(filename)
	caption = get_caption(filename)
	if caption:
		caption = str(caption[0][0])
	else:
		caption = "No Captions for This Image."
	return render_template('upload.html', caption=caption, filename=filename, rating=rating, comments=comments)

@app.route('/hello',methods=['GET'])
def hello():
	Filename = request.args.get('filename')
	commentValue = request.args.get('comment')
	x=[]
	if not cleanComment.mainFunction(commentValue):
		x.append("Sorry, your comment could not be loaded as it was considered offensive.")
	else:
		postComment(commentValue,Filename)
		x.append("Your comment was successfully loaded.")
	x.append("http://localhost:5000/show?filename="+Filename)
	return render_template('test2.html', x=x)

@app.route('/rating',methods=['GET'])
def accountRatings():
	rating = request.args.get('r')
	filename = request.args.get('filename')
	if (rating == "l"):
		ratingType = "l"
	else:
		ratingType = "d"
	updateRatings(filename,ratingType)
	x= []
	x.append("Your ratings were added.")
	x.append("http://localhost:5000/show?filename="+filename)
	return render_template('test2.html', x=x)

@app.route('/pics/<filename>')
def return_pic(filename):
	return send_from_directory(app.config['UPLOAD_DIR'], secure_filename(filename))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
