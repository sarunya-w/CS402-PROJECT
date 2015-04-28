# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 11:15:23 2015

@author: Sarunya
"""

from flask import Flask
app = Flask(__name__)

@app.route('/index')
def index():
    return "Hello World!"
if __name__ == '__main__':
    app.run(debug=True)
