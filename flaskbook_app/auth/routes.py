from flaskbook_app.models import User, UserInterest, Interest, Post, Follow
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flaskbook_app.auth.forms import SignUpForm, LoginForm
from flaskbook_app.extensions import db, app, bcrypt

auth = Blueprint("auth", __name__)

interests = ['Music','Movies', 'Books', 'Sports',
             'Food', 'Travel', 'Fashion', 'Gaming',
             'Art', 'Technology', 'Fitness', 'Science',]

@auth.route('/signup', methods=['GET', 'POST'])
def signup():


    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        if form.avatar.data:
            user = User(
                username=form.username.data,
                password=hashed_password,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                avatar=form.avatar.data
            )
        else:
            user = User(
                username=form.username.data,
                password=hashed_password,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )

        if user:
            db.session.add(user)
            db.session.commit()

            for interest_id in form.interests.data:
                user_interest = UserInterest(user_id=user.id, interest_id=interest_id)
                db.session.add(user_interest)
            db.session.commit()
            flash('Account Created!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('main.index'))

        else:
            flash('Account creation failed.', category='danger')

    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()


    # User.__table__.drop(db.engine)
    # UserInterest.__table__.drop(db.engine)
    # Post.__table__.drop(db.engine)
    # print(Post.query.all())

    # for interest in interests:
    #     new_interest = Interest(name=interest)
    #     db.session.add(new_interest)
    # db.session.commit()

    # posts = Post.query.filter_by(receiver_id=1).all()
    # print(posts)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.index'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
