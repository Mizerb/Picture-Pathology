import os
import keys
import json
import sys
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
from clarifai_basic import ClarifaiCustomModel
from flask.ext.sqlalchemy import SQLAlchemy

clarifai_api = ClarifaiCustomModel(app_id=keys.clientId, app_secret=keys.clientSecret)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = 'static/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/about/', methods=['GET'])
def about():
	return render_template("about.html")

@app.route('/data/', methods=['GET'])
def data():
	return render_template("data.html")

# @app.route('/results/', methods=['GET'])
# def results():
# 	return render_template("results.html")


@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		print request.files
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			## Change first part if we change domain names
			filePath = "http://ec2-52-88-123-145.us-west-2.compute.amazonaws.com/" + os.path.join(app.config['UPLOAD_FOLDER'], filename)



			result = clarifai_api.predict(filePath, 'test4') ## melanoma

			# res = json.loads(json.dumps(result))

			# if str(res["status_code"]) == "OK":
			# 	tmp = res['results'][0]['result']['tag']
			return render_template("results.html", res=result['urls'][0]['score'] > .55, res1=result['urls'][0]['score'])
			# else:
			# 	return str(res["status_msg"])

	return render_template('index.html')


if __name__ == '__main__':

	if len(sys.argv) == 2:
		if sys.argv[1] == "recreate":
			db_recreate()
			sys.exit(0)
		if sys.argv[1] == "create":
			db_create()
			sys.exit(0)

	app.run(debug=True, host='0.0.0.0', port=80, threading=True)