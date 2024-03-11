from app import app
from users.userforms  import signupForm, loginForm, otpForm
from users.modal import User
from flask import render_template as rt, flash, redirect , url_for
from flask_login import current_user , LoginManager , logout_user , login_required 


##### .......................................... User Login Configurations .............................................#####


# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(email):
    data= User.userData(email)
    return User(data)

##### .......................................... User Routes .............................................#####


# login
@app.route('/user/login', methods=['GET', 'POST'])
def login():
    form=loginForm()
    if form.validate_on_submit():
        res , status = User.login(form)
        if status:
            flash(res)
            return redirect('/dashboard')
        else:
            flash(res)
            return redirect('/login')
    return rt('login.html' , form = form )


# Signup
@app.route('/user/signup', methods=['GET', 'POST'])
def signup():
    form = signupForm()
    if form.validate_on_submit():
        response, status = User.signup(form)
        flash(response)
        if (status):
             return redirect(url_for('otp'))
        else:
            return redirect(url_for('signup'))
    return rt('signup.html' , form=form)

@app.route('/user/verify-otp', methods=['GET', 'POST'])
def otp():
    form = otpForm()
    if form.validate_on_submit():
        otp = int(form.otp.data)
        if current_user.otp == otp:
            User.update_activation_status(current_user.email)
            print("hello")
            print(current_user.email)
            flash('Email confirmed!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid OTP!', 'danger')
            return redirect(url_for('otp'))
   
    return rt('otp.html', form = form)



# Logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
	logout_user()
	flash("You Have Been Logged Out!")
	return redirect((url_for('login')))


@app.route('/dashboard')
@login_required
def dashboard():
    return rt('dashboard.html')




# @app.route('/check-email')
# def check_email():
#     email = session.get('email', None)
#     if not email:
#         return redirect('/signup')
#     return rt('check-mail.html', email=email)



# @app.route('/confirm_email/<token>')
# def confirm_email(token):
#     try:
#         s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#         email = s.loads(token, salt='email-confirm', max_age=3600)
#     except:
#         flash('The confirmation link is invalid or has expired.', 'danger')
#         return redirect(url_for('login'))

#     user = User.userData(email)
    
#     if user:
#         if user['activated']:
#             flash('Email already confirmed. Please log in.', 'info')
#             return redirect('/login')
#         User.updateuser(email)
#         # send_welcome_email(email)
#         # print("Welcome Email sent")
#         flash('Thank you for confirming your email! Please log in.', 'success')
#         # return redirect('/dashboard')

#     else:
#         flash('Error! User not found.', 'danger')
#     return redirect('/login')
