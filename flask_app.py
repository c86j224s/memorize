#!/usr/bin/env python
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask! (20130929)' 

@app.route('/about')
def about ():
	return render_template ('about.html',
		globalNavigation=(
			('http://www.google.com', 'Google!'), 
			('http://www.naver.com', 'Naver!'),
			('http://www.daum.net', 'Daum!')))

@app.route('/posts')
def posts ():
	# @todo get multiple posts from db
	return render_template('post.html')

@app.route('/post/<int:post_id>')
def post (post_id):
	# @todo get one post from db
	return render_template('post.html')

if __name__ == '__main__':
	app.debug = True
	app.run ()
