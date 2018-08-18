# coding=utf8
import os
import json
from flask import Flask, render_template
app = Flask(__name__)

# with open('data.json', 'w') as fp:
#     json.dump(geist_data, fp)


with open('static/data.json', 'r') as fp:
    geist_data = json.load(fp)

print(geist_data)



posts = [
    {
        'author': 'Spencer Caldwell',
        'title': 'Blog post #1',
        'content': 'This is my first post.',
        'date_posted': "April 20, 2018"
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog post #2',
        'content': 'Hi this is Jane. Take a look at my blog',
        'date_posted': "April 23, 2018"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts, geist_data=geist_data)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/test")
def test():
    return render_template('test.html', title="Test", geist_data=geist_data, posts=posts)

if __name__ == '__main__':
    app.run(debug=True)