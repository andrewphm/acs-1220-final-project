from flaskbook_app.models import User
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flaskbook_app.auth.forms import SignUpForm, LoginForm
from flaskbook_app.extensions import db, app, bcrypt

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print(form.__str__)

        user = User(
            username=form.username.data,
            password=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        if user:
            # print('user: ', user.__dict__)
            # db.session.add(user)
            # db.session.commit()
            flash('Account Created!', category='success')

    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
