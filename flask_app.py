#!/usr/bin/env python
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/about')
def about ():
	return render_template ('about.html',
		globalNavigation=(
			('http://www.google.com', 'Google!'), 
			('http://www.naver.com', 'Naver!'),
			('http://www.daum.net', 'Daum!')))
