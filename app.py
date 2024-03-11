#### ........................... dependencies importing .............................####
from flask import Flask, render_template as rt
from os import getenv 
from flask_login import login_required, current_user
from flask_mail import Mail
from db.db import db as d

#### ........................... App configuration .............................####
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv("SECRET_KEY")

##### .......................................... Mail Configuration .............................................#####
app.config.update(
    MAIL_SERVER = getenv('SMTP_SERVER'),
    MAIL_PORT = getenv('SMTP_PORT'),
    MAIL_USE_SSL = True,
    MAIL_USERNAME = getenv('SMTP_USERNAME'),
    MAIL_PASSWORD = getenv('SMTP_PASSWORD')
)
mail = Mail(app)

#### ........................... Static routes .............................####

@app.route('/')
def index():
    return rt("index.html")


@app.route('/landupload')
@login_required
def landupload():
    print(current_user.email)
    return rt("landupload.html")


@app.route('/aboutus')
def aboutus():
    return rt("aboutus.html")


#### ........................... import routes .............................####

from users.routes import *


#### ........................... error handling .............................####s

@app.errorhandler(404)
def badlink(e):
    return rt('404.html') , 404