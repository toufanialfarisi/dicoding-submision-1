from flask import redirect, url_for, render_template, Blueprint, flash, request, Flask
from forms import Post
import os
import uuid
import sys
from azure.storage.blob import BlockBlobService, PublicAccess
from forms import UploadImage
import numpy as np
import pyodbc
from werkzeug.utils import secure_filename
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# Get endpoint and key from environment variables
# import os
endpoint = 'https://southeastasia.api.cognitive.microsoft.com/'
key = 'd4b8cbabf63c4220afe95a25b956b975'

# Set credentials
credentials = CognitiveServicesCredentials(key)

# Create client
client = ComputerVisionClient(endpoint, credentials)

# server = 'toufani-ra-server.database.windows.net'
# database = 'toufani-ra-db'
# username = 'toufani1515'
# password = '#serigala95'
# cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
#                       server+';DATABASE='+database+';UID='+username+';PWD=' + password)
# cursor = cnxn.cursor()

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
app.config['SECRET_KEY'] = 'mysecretkey'


UPLOAD_FOLDER = os.getcwd() + '/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/vision', methods=['POST', 'GET'])
def vision():
    form = UploadImage()
    if request.method == 'POST':
        # data = str(form.image.data)
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join(
                os.getcwd() + '/static/uploads', filename)
            file.save(image_path)

        image_analysis = client.analyze_image(
            image_path, visual_features=[VisualFeatureTypes.tags])

        for tag in image_analysis.tags:
            print(tag)

        models = client.list_models()

        for x in models.models_property:
            print(x)

        # type of prediction
        domain = "landmarks"

        # Public domain image of Eiffel tower
        url = "https://images.pexels.com/photos/338515/pexels-photo-338515.jpeg"

        # English language response
        language = "en"

        analysis = client.analyze_image_by_domain(domain, image_path, language)

        for landmark in analysis.result["landmarks"]:
            print(landmark["name"])
            print(landmark["confidence"])

        flash('sukses tersimpan', 'success')

        return render_template('cognitive.html', form=form)
    return render_template('cognitive.html', form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5005)
