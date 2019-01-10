from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from webapp.backend.data_storage import UserStorage

LOCATIONS = [('London', 'London'), ('Madrid', 'Madrid')]


class NewSearchForm(FlaskForm):
    submit = SubmitField('New Search')


class SearchActionForm(FlaskForm):
    def __init__(self, term, loc, *args, **kwargs):
        super(SearchActionForm, self).__init__(*args, **kwargs)
        self.term = term
        self.loc = loc

    remove = SubmitField("Remove")
    search = SubmitField("Search")


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class SearchForm(FlaskForm):
    term = StringField('Search Term', validators=[DataRequired()])
    geo = SelectField('Location', choices=LOCATIONS)
    submit = SubmitField('Search')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    location = SelectField('Location', choices=LOCATIONS, validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = UserStorage
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
