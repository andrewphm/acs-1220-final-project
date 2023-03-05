from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flaskbook_app.models import User, Post, Interest, UserInterest, Follow
from flaskbook_app.auth.forms import SignUpForm
from flaskbook_app.extensions import db, app, bcrypt
from flaskbook_app.main.forms import PostForm

main = Blueprint("main", __name__)

@main.route("/")
@login_required
def index():
    # Post.__table__.drop(db.engine)
    # UserInterest.__table__.drop(db.engine)
    # Follow.__table__.drop(db.engine)
    print("finished dropping table")
    return render_template("home.html")


@main.route("/<username>/")
@login_required
def user_profile(username):
    form = PostForm()
    user = User.query.filter_by(username=username).first_or_404()

    interests = []

    for interest in user.user_interests:
        interests.append(interest.interest.name)

    return render_template("profile.html", user=user, current_user=current_user, interests=interests, form=form)


@main.route('/follow/<user_id>', methods=['POST'])
@login_required
def follow(user_id):
    print('firing')
    user_to_follow = User.query.get(user_id)
    if user_to_follow is None:
        flash('User not found.', category='danger')
        return redirect(url_for('main.index'))
    if current_user.is_following(user_to_follow):
        flash('You are already following this user.', category='danger')
        return redirect(url_for('main.user_profile', username=user_to_follow.username))
    current_user.follow(user_to_follow)
    db.session.commit()
    flash(f'You are now following {user_to_follow.first_name}', category='success')
    return redirect(url_for('main.user_profile', username=user_to_follow.username))

@main.route('/unfollow/<user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    user_to_unfollow = User.query.get(user_id)
    if user_to_unfollow is None:
        flash('User not found.', category='danger')
        return redirect(url_for('main.index'))
    if not current_user.is_following(user_to_unfollow):
        flash('You are not following this user.', category='danger')
        return redirect(url_for('main.user_profile', username=user_to_unfollow.username))
    current_user.unfollow(user_to_unfollow)
    db.session.commit()
    flash(f'You are no longer following {user_to_unfollow.first_name}', category='success')
    return redirect(url_for('main.user_profile', username=user_to_unfollow.username))

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
