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
    user = User.query.filter_by(username=current_user.username).first_or_404()
    followed_users = user.followed.all()
    posts = Post.query \
    .join(Follow, Follow.followed_id == Post.author_id) \
    .filter(Follow.follower_id == user.id) \
    .filter(Post.receiver_id == Post.author_id) \
    .order_by(Post.created_at.desc()) \
    .all()

    print(posts)
    return render_template("home.html", posts=posts, current_user=current_user)


@main.route("/<username>/")
@login_required
def user_profile(username):
    form = PostForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(receiver_id=user.id).order_by(Post.created_at.desc()).all()
    interests = []

    for interest in user.user_interests:
        interests.append(interest.interest.name)

    return render_template("profile.html", user=user, current_user=current_user, interests=interests, form=form, posts=posts)


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

@main.route('/post/create/<user_id>', methods=['GET', 'POST'])
@login_required
def create_post(user_id):
    form = PostForm()
    user = User.query.get(user_id)
    if form.validate_on_submit():
        post = Post(
            content=form.content.data,
            photo=form.image.data,
            author_id=current_user.id,
            receiver_id=user_id
        )
        print(post)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', category='success')
        return redirect(url_for('main.user_profile', username=user.username))
    return render_template('create_post.html', form=form)
