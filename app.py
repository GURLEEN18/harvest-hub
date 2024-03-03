from flask import Flask, request ,render_template as rt , redirect ,flash
from users.modal import User
from os import getenv 
from flask_login import LoginManager,login_required, logout_user


app = Flask(__name__)

app.config['SECRET_KEY'] = getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(email):
    data= User.userData(email)
    # add other attribute to the user object doinn this to test the user object
    user_object = User(data['name'],data['email'], data['password_hash'] )
    return user_object

@app.route('/')
def index():
    return rt("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("inside post")

        email = request.form.get('email')
        password = request.form.get('password')
        res , status =User.login(email, password)
        if status:
            flash(res)
            return redirect('/dashboard')
        else:
            flash(res)
            return redirect('/login')
    return rt('login.html' )
    
@app.route('/signup' , methods=['GET', 'POST'])
def signup():
    
    return rt('signup.html' )

@app.route('/verify')
def verify():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password') 
        confirm_password = request.form.get('Confirm_password')
        res , status =User.signup(name ,email, password , confirm_password)
        if status:
            flash(res)
            return redirect('/login')
        else:
            flash(res)
            return redirect('/signup')

    return rt('verify.html')

@app.route('/logout', methods=['GET'])
@login_required
def logout():
	logout_user()
	flash("You Have Been Logged Out!")
	return redirect(('/login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return rt("dashboard.html")

@app.route('/header')
def header():
    return rt("layout.html")
@app.route('/aboutus')
def aboutus():
    return rt("aboutus.html")





@app.errorhandler(404)
def badlink(e):
    return rt('404.html') , 404