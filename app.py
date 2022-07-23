import os
from flask import Flask, after_this_request, render_template, flash, request, redirect
import pandas as pd
from pandas_profiling import ProfileReport
from werkzeug.utils import secure_filename
import matplotlib
matplotlib.use('Agg')
from flask_cors import CORS
from pathlib import Path

UPLOAD_FOLDER = './Store/'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD']= True

@app.route("/quality")
def data_quality():
    my_file = Path('./templates/Entube.html')
    if my_file.is_file():
        return render_template('Entube.html')
    return None
    


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = pd.read_csv(f'./Store/{file.filename}')
            profile = ProfileReport(df, title="Profiling Report", explorative=True)
            profile.to_file("templates/Entube.html")
            os.remove(f'./Store/{file.filename}')
            return redirect(request.url)
