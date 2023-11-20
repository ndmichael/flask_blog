from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, BooleanField, EmailField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from fblog.models import User


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20) ])
    email = EmailField('Email', validators=[ DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50) ])
    confirm_password =  PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Now')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username has been taken.")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email has been taken.")


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[ DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50) ])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class CreatePost(FlaskForm):
    title = StringField('Your Title', validators=[DataRequired(), Length(min=5, max=100) ])
    content = TextAreaField('Content', render_kw={'rows':7})
    image = FileField('Post Image', validators=[FileAllowed(['jpg', 'png', 'svg'])])
    submit = SubmitField('SUBMIT POST')


class UpdatePost(FlaskForm):
    title = StringField('Your Title', validators=[DataRequired(), Length(min=5, max=100) ])
    content = TextAreaField('Content', render_kw={'rows':7})
    submit = SubmitField('UPDATE POST')