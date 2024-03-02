from flask import Flask, request ,render_template as rt
from os import getenv 

app = Flask(__name__)

app.config['SECRET_KEY'] = getenv("SECRET_KEY")

@app.route('/')
def index():
    return rt("index.html")

@app.route('/header')
def header():
    return rt("layout.html")
@app.route('/aboutus')
def aboutus():
    return rt("aboutus.html")





@app.errorhandler(404)
def badlink(e):
    return rt('404.html') , 404