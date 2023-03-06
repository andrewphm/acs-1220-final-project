# from flaskbook_app import bcrypt
from flaskbook_app.models import User, Interest
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, ValidationError
from flaskbook_app.extensions import db, bcrypt

class SignUpForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(),Length(min=3, max=50)], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Last Name"})
    username = StringField('Username',
        validators=[DataRequired(), Length(min=3, max=50)], render_kw={"placeholder": "Username"})
    avatar = StringField('Avatar', render_kw={"placeholder": "Add an avatar url"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    interests = SelectMultipleField('Interests', choices=[(interest.id, interest.name) for interest in Interest.query.all()], widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput(), coerce=int)
    submit = SubmitField('Sign Up')

    def __str__(self):
        return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')
