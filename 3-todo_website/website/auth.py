from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user


auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in sucessfully!',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Try again!!',category='error')
        else:
            flash('Email does not exists.',category='error')
    return render_template("login.html",user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exits.",category='error')
        elif len(email) < 4:
            flash("Email must be > 4",category='error')
        elif len(username) < 2:
            flash("Username must be > 2",category='error')
        elif password1 != password2:
            flash("Password does not match ",category='error')
        else:
            new_user = User(email=email,username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Successfully signed up!!",category='success')
            login_user(new_user)
            return redirect(url_for('views.home'))
             
    return render_template("sign_up.html",user=current_user)