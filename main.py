import os
import keys
import json
import sys
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
from clarifai.client import ClarifaiApi
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

clarifai_api = ClarifaiApi(app_id=keys.clientId, app_secret=keys.clientSecret)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['SQLALCHEMY_DATABASE_URI'] = keys.DB_LOCATION
db = SQLAlchemy(app)


class ImageClass(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.String(128))
	image_data_id = db.Column(db.Integer, db.ForeignKey('image_data.id'))
	def __init__(self, val):
		self.value = val

class ImageProb(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.String(127))
	image_data_id = db.Column(db.Integer, db.ForeignKey('image_data.id'))
	def __init__(self, val):
		self.value = val
		
class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    classes =  db.relationship('ImageClass', backref='image_data',
                                lazy='dynamic')
    probs =  db.relationship('ImageProb', backref='image_data',
                                lazy='dynamic')    
    docIdStr = db.Column(db.String(128))

    def __init__(self, docIdStr):
        self.docIdStr = docIdStr

    def __repr__(self):
        return '<ImageData classes=' + ' '.join([item.value for item in self.classes]) + ' probs=' + ' '.join([item.value for item in self.probs]) + ' docIdStr=' + self.docIdStr + '>' 

def db_create():
    ## Create database from models
    print "Creating database"
    db.create_all()

def db_recreate():
    ## Drop all tables and then recreate.
    print "Recreating database"
    db.reflect()
    db.drop_all()
    db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def guess_disease(result):
	'''Given the result from Clarifai, scan the results for possible matches.'''
	## Data will be from res['results'][0]['result']['tag'], so we can just do result['classes'] and result['probs']
	possibleDiseases = ['melanoma'] ## Can be extended later

	## List of tuples containing name and probability of disease.
	diseaseProbability = []
	
	for disease in possibleDiseases:
		if disease in result['classes']:
			index = result['classes'].index(disease)
			currentProbability = result['probs'][index]
			diseaseProbability.append((disease, float(currentProbability)))

	diseaseProbability = sorted(diseaseProbability, key=lambda x: x[1], reverse=True)
	return diseaseProbability



@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		print ":("
		print request.files
		file = request.files['file']
		if file and allowed_file(file.filename):

			result = clarifai_api.tag_images(file)

			res = json.loads(json.dumps(result))

			if str(res["status_code"]) == "OK":
				tmp = res['results'][0]['result']['tag']
				imageData = ImageData(res['results'][0]['docid_str'])

				db.session.add(imageData)
				db.session.commit()

				for item in map(str, tmp['classes']):
					x = ImageClass(item)
					imageData.classes.append(x)

				for item in tmp['probs']:
					x = ImageProb(str(item))
					imageData.probs.append(x)

				db.session.add(imageData)
				db.session.commit()

				print tmp
				print guess_disease(tmp)

				return json.dumps(result)
			else:
				return str(res["status_msg"])

	return render_template('index.html')


if __name__ == '__main__':

	if len(sys.argv) == 2:
		if sys.argv[1] == "recreate":
			db_recreate()
			sys.exit(0)
		if sys.argv[1] == "create":
			db_create()
			sys.exit(0)

	app.run(debug=True)