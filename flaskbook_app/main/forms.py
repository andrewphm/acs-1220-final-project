from flaskbook_app.models import User, Interest
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, widgets, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from flaskbook_app.extensions import db, bcrypt

class PostForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()], render_kw={"placeholder": "Write a comment..."})
    image = StringField('Image', render_kw={"placeholder": "Image URL..."})
    submit = SubmitField('Share')
