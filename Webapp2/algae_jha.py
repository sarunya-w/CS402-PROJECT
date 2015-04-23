# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:08:08 2015

@author: Jha Yanin
"""

import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # J add code classifier here
            # then save the output_img to somewhere in /static
            # the classification report can be added in status            
            return render_template('index.html',
                                   status="%s is uploaded"%filename,
                                   input_img=os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                   output_img=os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('index.html',status='Please upload an image')
if __name__ == '__main__':
    app.run(debug=True)