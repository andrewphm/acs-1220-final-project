from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flaskbook_app.models import User, Post, Interest, UserInterest, Follow, Comment
from flaskbook_app.extensions import db
from flaskbook_app.auth.forms import SignUpForm
from flaskbook_app.extensions import db, app, bcrypt
from flaskbook_app.main.forms import PostForm

main = Blueprint("main", __name__)

@main.route("/")
@login_required
def index():
    return render_template("home.html")


@main.route("/<username>/")
@login_required
def user_profile(username):
    form = PostForm()
    user = User.query.filter_by(username=username).first_or_404()
    # posts = Post.query.filter_by(user_id=user.id).all()
    interests = []

    print(user.avatar)
    for interest in user.user_interests:
        interests.append(interest.interest.name)

    return render_template("profile.html", user=user, current_user=current_user, interests=interests, form=form)


@main.route("/<username>/profile/edit")
def edit_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = SignUpForm(obj=user)

    default_interests = []
    for user_interest in user.user_interests:
        default_interests.append(user_interest.interest.id)

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(
            username=form.username.data,
            password=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        if user:
            db.session.add(user)
            db.session.commit()
            flash('Account Updated!', category='success')
        else:
            flash('Account updated failed.', category='danger')

    return render_template('edit_profile.html', form=form, default_interests=default_interests)
