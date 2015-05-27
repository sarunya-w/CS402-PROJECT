# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:08:08 2015

@author: Jha Yanin
"""

import os
#import json
from flask import Flask, request, redirect, url_for, render_template,Markup
from werkzeug import secure_filename
from web_classification import *

#from pprint import pprint

UPLOAD_FOLDER = 'static/uploads'
TOTAL_FOLDER = 'static/out/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TOTAL_FOLDER'] = TOTAL_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                   
            #with open('data.json') as data_file:
                #data = json.load(data_file)
            #pprint(data)
   
            rrects = ''
            out_rrects = ''           
            coordinate = master(filename)
            #print coordinate
            count = [0,0,0,0,0,0,0,0,0,0]
            classname = ["Anabaena sp.","Coelomoron sp.","Oscillatoria sp.","Actinastrum sp.","Closteriopsis sp.","Pediasprum sp. ","Scenedesnus sp.","Triplastrum sp.","Lepocinclis sp.","Cyclotella sp."]
            xcolor = ["#FF0000","#0e7fff","#b4772c","#2ca02c","#FC6C85","#800080","#FFA500","#22bdbc","#7f7f7f","#cfbe17"]
            for j in xrange(len(coordinate)):
            	if coordinate[j][2] == 0 :
            		count[0] += 1
            		color = xcolor[0]
            	elif coordinate[j][2] == 1 :
            		count[1] += 1
            		color = xcolor[1]
            	elif coordinate[j][2] == 2 :
            		count[2] += 1
            		color = xcolor[2]
            	elif coordinate[j][2] == 3 :
            		count[3] += 1
            		color = xcolor[3]
            	elif coordinate[j][2] == 4 :
            		count[4] += 1
            		color = xcolor[4]
            	elif coordinate[j][2] == 5 :
            		count[5] += 1
            		color = xcolor[5]
            	elif coordinate[j][2] == 6 :
            		count[6] += 1
            		color = xcolor[6]
            	elif coordinate[j][2] == 7 :
            		count[7] += 1
            		color = xcolor[7]
            	elif coordinate[j][2] == 8 :
            		count[8] += 1
            		color = xcolor[8]
            	elif coordinate[j][2] == 9 :
            		count[9] += 1
            		color = xcolor[9]

            	rrects += Markup('''<rect x="''' + "%d"%coordinate[j][0] + '''" y="''' + "%d"%coordinate[j][1] + '''" 
            		width="200" height="200" style="stroke:''' + "%s"%color + ''';
            		stroke-width:2;fill-opacity:0.0;stroke-opacity:1.0"/>''')


            for k in xrange(len(count)):
            	if count[k] !=0:
            		out_rrects += Markup('''<div style="display: block;height="50"><svg width="110" height="50"><rect x="50" y="20" width="30" height="30"
            			style="fill:''' + "%s"%xcolor[k] + ''';fill-opacity:1.0"></svg>'''+ "%s "%classname[k] + 
            			 '{:.2%}'.format((float(count[k])/float(len(coordinate)))) +''' </div>''')

            return render_template('index.html',
                                   status="%s is uploaded"%filename ,
                                   input_img=os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                   output_img=out_rrects,rect=rrects)
                                    
                                    
    return render_template('index.html',status='Please upload an image')
if __name__ == '__main__':
    app.run(debug=True)