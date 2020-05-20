from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app  = Flask(__name__)
app.config['SECRET_KEY'] = '0e4cc2d780d7f2b9a1be03e1a42e84c9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['SERVER_NAME'] = '*:5000'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' #same as login function name this will be used in url_for()
login_manager.login_message_category = 'info' #the class name which we are using in html [now we are using bootstrap]

##############################################################################
# Do not move this import because it will create errors on importing modules
from project import routes
##############################################################################
