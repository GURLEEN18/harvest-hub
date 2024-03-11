from db.db import db
from flask_login import UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from os import getenv
from flask_mail import Message
from app import mail
from flask import render_template as rt






user = db["users"]

class User(UserMixin):
    def __init__(self,userData):
        self.name = userData['name']
        self.email = userData['email']
        self.password_hash = userData['password_hash']
        self.plots = userData['plots']
        self.seeds = userData['seeds']
        self.activated = userData['activated']
        self.otp = userData['otp']


    def get_id(self):
        return self.email


    def add_user(self):
            user_data = dict( name = self.name, email = self.email, password_hash = self.password_hash , plots = self.plots, seeds = self.seeds)
            result = user.insert_one(user_data)

    def alreadyExists(email):
        data = user.find_one({ "email": email })
        if data:
            return True
        else:
            return False
      
    def userData(email):
        data = user.find_one({ "email": email})
        return data
    
    def get_all_emails():
        cursor = user.find({}, {"email": 1, "_id": 0})
        emailList = []
        for document in cursor:
            if 'email' in document:
                emailList.append(document['email'])
        return emailList
        
    def update_activation_status(email):
        myquery = { "email": email }
        newvalues = { "$set": { "activated": True } }
        user.update_one(myquery, newvalues)
      
    def signup(form):
        email = form.email.data
        password = form.password.data
        name = form.name.data
        if (User.alreadyExists(email)):
            return "This email is already in use", False    
        else:
            hash_pass =  generate_password_hash(password, method='scrypt')
            otp = randint(1000,9999)
            new_user = dict( name = name, email = email, password_hash = hash_pass , plots=[] ,seeds = []   , activated = False , otp = otp)
            result = user.insert_one(new_user)
            print("User added with id: ", result.inserted_id)
            msg = Message(subject="OTP for Sign up",sender= getenv('SMTP_USERNAME'), recipients=[email])
            msg.html = rt('mail.html', name = name , otp = otp)
            mail.send(msg)
            login_user(User(new_user))
            return "email sent to "+ email + " please check your inbox " , True

    def login(form):
        if (User.alreadyExists(form.email.data)):
                    userData = User.userData(form.email.data)
                    if (check_password_hash(userData['password_hash'],form.password.data)):
                        print(str(userData['email'])+": Logged in")
                        userObject = User(userData)
                        login_user(userObject)
                        responce = "Login Succesfull!!"
                        status = True
                    else:
                        responce = 'Incorrect login credentials'
                        status = False
        else:
            responce = 'User doest exist!! try again'
            status = False

        return responce , status
    