from project import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.png')
	password = db.Column(db.String(60), nullable=False)
	parent_org = db.Column(db.String(20), nullable=True)
	roles = db.relationship('Role', secondary='user_roles')
	posts = db.relationship('Post', backref='author', lazy=True)

# get FullName
	def FullDir(self):
		if not self.parent_org:
			return f"/{self.username}"	
		else:
			return f"/{self.parent_org}/{self.username}"
	
	def get_urole(self):
		return self.roles

# print method
	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.roles}', '{self.parent_org}')"
		
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# print method
	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}' )"

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), unique=True)
# print method
	def __repr__(self):
		return self.name

# Define the UserRoles association table
class UserRoles(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
# print method
	def __repr__(self):
		return f"UserRoles('{self.user_id}', '{self.role_id}')"

class empRequest(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	empname = db.Column(db.String(20), nullable=False)
	orgname = db.Column(db.String(20), nullable=False)
# print method
	def __repr__(self):
		return f"empRequest('{self.empname}', '{self.orgname}')"



class empList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	empname = db.Column(db.String(20), nullable=False)
	orgname = db.Column(db.String(20), nullable=False)
# print method
	def __repr__(self):
		return f"empRequest('{self.empname}', '{self.orgname}')"

class Announcement(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	message = db.Column(db.String(20), unique=True, nullable=False)
	orgname = db.Column(db.String(20), unique=True, nullable=False)
# print method
	def __repr__(self):
		return f"empRequest('{self.empname}', '{self.orgname}')"

# class Folder(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	title = db.Column(db.String(100), nullable=False)
# 	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# 	location = db.Column(db.String(200), nullable=False)
# 	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	

# class Organization(db.Model, UserMixin):
	
# 	id = db.Column(db.Integer, primary_key=True)
# 	organization_name = db.Column(db.String(20), unique=True, nullable=False)
# 	email = db.Column(db.String(120), unique=True, nullable=False)
# 	logo = db.Column(db.String(20), nullable=False, default='default.png')
# 	password = db.Column(db.String(60), nullable=False)
# 	roles = db.Column(db.String(20), nullable=False, default='organization')
# 	emps = db.relationship('Employee', backref='org', lazy=True)

# # print method
# 	def __repr__(self):
# 		return f"Organization('{self.organization_name}', '{self.email}, '{self.logo} )"


# class Employee(db.Model, UserMixin):
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(20), unique=True, nullable=False)
# 	email = db.Column(db.String(120), unique=True, nullable=False)
# 	image_file = db.Column(db.String(20), nullable=False, default='default.png')
# 	password = db.Column(db.String(60), nullable=False)
# 	role = db.Column(db.String(20), nullable=False, default='employee')
# 	org_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

# # print method
# 	def __repr__(self):
# 		return f"Employee('{self.username}', '{self.email}, '{self.org_id}', ' {self.image_file}' )"

