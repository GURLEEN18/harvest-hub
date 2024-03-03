from db.db import db
from flask_login import UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash

user = db["users"]

class User(UserMixin):
    def __init__(self, name, email, password_hash , plots=[],seeds=[]):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.plots = plots
        self.seeds = seeds


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
    
    def signup(name ,email, password , confirm_password):
        if (password != confirm_password):
            return "Passwords do not match", False
        if (User.alreadyExists(email)):
            return "This email is already in use", False    
        else:
            hash_pass =  generate_password_hash(password, method='scrypt')
            new_user = User(name, email, hash_pass , plots=[],seeds=[])
            new_user.add_user()
            login_user(new_user)
            return "Account created Successfully", True 

    def login(email, password):

        if (User.alreadyExists(email)):
                    data = User.userData(email)
                    if (check_password_hash(data['password_hash'],password)):
                        user_object = User( data['name'],data['email'], data['password_hash'], data['plots'], data['seeds'])
                        login_user(user_object)
                        responce = "Login Succesfull!!"
                        status = True
                    else:
                        responce = 'Incorrect login credentials'
                        status = False
        else:
            responce = 'User doest exist!! try again'
            status = False

        return responce , status
                








        

    

    
    

    

    