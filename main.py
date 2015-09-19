from flask import Flask, request, redirect, url_for
import os
import keys
from werkzeug import secure_filename
from clarifai.client import ClarifaiApi

app = Flask(__name__)

clarifai_api = ClarifaiApi(app_id=keys.clientId, app_secret=keys.clientSecret)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

UPLOAD_FOLDER = './'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            
            result = clarifai_api.tag_images(file)

            return str(result)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':



    app.run()