# coding=utf8
import os
import requests
import json
from flask import Flask, render_template
app = Flask(__name__)

with open('static/data.json', 'r') as fp:
    geist_data = json.load(fp)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title="Test", geist_data=geist_data)

'''
@app.route("/{}".format(hostname))
def test():
'''    

if __name__ == '__main__':
    app.run(debug=True)



