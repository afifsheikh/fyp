from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from project.models import User

class Org_RegistrationForm(FlaskForm):
	org_name = StringField('Orginization Name', validators=[DataRequired(), Length(min=2, max=50)])
	address = TextAreaField('Address', validators=[DataRequired(), Length(min=2, max=50)])
	email = StringField('Email', validators=[DataRequired(),Email()])
	contact = StringField('Contact No', validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')
	
	def validate_username(self, org_name):
		user = User.query.filter_by(username=org_name.data).first()
		if user:
			raise ValidationError('Username is already taken. Please choose different one.')
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is already taken. Please choose different one.')
	
class Emp_RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	org_code = StringField('Orginization Code', validators=[DataRequired(), Length(min=1, max=10)])
	email = StringField('Email', validators=[DataRequired(),Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username is already taken. Please choose different one.')
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is already taken. Please choose different one.')
	

class RegistrationForm(FlaskForm):
	# DataRequired is for cumplusary fields
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(),Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username is already taken. Please choose different one.')
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is already taken. Please choose different one.')
		

class LoginForm(FlaskForm):
	# DataRequired is for cumplusary fields
	email = StringField('Email', validators=[DataRequired(),Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	userTpye = RadioField('User', choices=[('employee','Employee'),('organization','Organization')],default='employee', validators=[DataRequired()])
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	# DataRequired is for cumplusary fields
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(),Email()])
	picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username is already taken. Please choose different one.')
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email is already taken. Please choose different one.')

class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])	
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')

class AnnouncementForm(FlaskForm):
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Announce!')

# class UploadFileForm(FlaskForm):
# 	file_name = StringField('File Name', validators=[DataRequired()])	
# 	file_type = TextAreaField('File Type', validators=[DataRequired()])
# 	file = FileField('Upload File')
# 	submit = SubmitField('Upload')
