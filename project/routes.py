import ntpath
import os
import shutil
import secrets
from DirectoryHandling import DirectoryHandling as dh
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort,send_file, send_from_directory
from project import app, db, bcrypt, login_manager
from project.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, Emp_RegistrationForm, Org_RegistrationForm
from project.models import User, Post, Role, empRequest, empList
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps
# from flask_user import roles_required, UserManager


files = []
dirs = []
root_dir = ''
dih = dh.dirHandling()



@app.route("/")
@app.route("/home")
def home():
	if current_user.is_authenticated:
		return redirect(url_for('account'))
	posts = Post.query.all()
	return render_template('home.html', posts=posts)

@app.route("/about")
def about():
	return render_template('about.html', title='About')

@app.route("/OrgRegister", methods=['GET', 'POST'])
def OrginizationRegister():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = Org_RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		org = User(username=form.org_name.data, email=form.email.data, password=hashed_password)
		org_role = Role.query.filter_by(name='org').first()
		org.roles = [org_role]
		db.session.add(org)
		db.session.commit()
		flash("Your Organization Account has been created! You are now able to log in", 'success')
		return redirect(url_for('login'))
	return render_template('org_registration.html', title='Register', form=form)

@app.route("/EmpRegister", methods=['GET', 'POST'])
def EmpRegister():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = Emp_RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		emp = User(username=form.username.data, email=form.email.data, password=hashed_password, parent_org=form.org_code.data)
		empreq = empRequest(empname=form.username.data, orgname=form.org_code.data) 
		db.session.add(empreq)
		emp_role = Role.query.filter_by(name='emp').first()
		emp.roles = [emp_role]
		db.session.add(emp)
		db.session.commit()
		flash("You have been registered Successfully. Please wait until you are approved!", 'success')
		return redirect(url_for('login'))
	return render_template('emp_registration.html', title='Register', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash("Your account has been created! You are now able to log in", 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		initUser()
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			if str(user.parent_org) != 'None':
				emp = empList.query.filter_by(empname= user.username).first()
				if not emp:
					flash("Login Unsuccessful, Your Organization request has not been approved yet." , "warning")					
					return render_template('login.html', title='Login', form=form)				
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next') #args is a dictionary we use get method so that if the next prameter dost not exits it gives none so dont use square brackets with the key
			initUser()
			flash("Login Successful" , "success")
			return redirect(next_page) if next_page else redirect(url_for('home')) # this is done so that if login page is directed from a restricted page then after login it redirects to that page instead of home page
		else:
			flash("Login Unsuccessful, Please check your email and password" , "danger")
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/Dashboard")
@login_required
def Dashboard():
	adminRole = Role.query.filter_by(name='Admin').first() #selection
	orgRole = Role.query.filter_by(name='org').first()
	for role in current_user.roles:
		if role == adminRole or role == orgRole:
			req = empRequest.query.filter_by(orgname=current_user.username).all()
			newReq = []
			for rec in req:
				e = User.query.filter_by(username=rec.empname).first()
				newReq.append(e)
			emplst = empList.query.filter_by(orgname=current_user.username).all()
			newEmpLst = []
			for rec in emplst:
				e = User.query.filter_by(username=rec.empname).first()
				newEmpLst.append(e)
			return render_template('org_dashboard.html', title='Dashboard',req = newReq, emplst = newEmpLst) 
		
	abort(403)
@app.route("/Dashboard/<string:empname>/<string:orgname>")
@login_required
def req_emp(empname,orgname):
	emp  = empRequest.query.filter_by(empname=empname,orgname=orgname).first()
	empAdd = empList(empname = emp.empname, orgname=emp.orgname)
	db.session.add(empAdd)
	db.session.delete(emp)
	db.session.commit()
	return redirect(url_for('Dashboard'))

@app.route("/deleteEmployee/<string:en>/<string:on>")
@login_required
def del_emplist(en,on):
	emp  = empList.query.filter_by(empname=en,orgname=on).first()
	user = User.query.filter_by(username=en).first()
	empReg  = User.query.filter_by(username=en,parent_org=on).first()
	db.session.delete(user)
	db.session.delete(emp)
	db.session.delete(empReg)
	db.session.commit()
	# delete_directory('root_'+en,1) # uncomment this line to also remove the directory of the employee
	return redirect(url_for('Dashboard'))

@app.route("/requestdelete/<string:e>/<string:o>")
@login_required
def del_empreq(e,o):
	emp  = empRequest.query.filter_by(empname=e,orgname=o).first()
	empReg  = User.query.filter_by(username=e,parent_org=o).first()
	user = User.query.filter_by(username = e).first()
	db.session.delete(user)
	db.session.delete(empReg)
	db.session.delete(emp)
	db.session.commit()
	return redirect(url_for('Dashboard'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	
	outputsize = (125,125)
	pic = Image.open(form_picture)
	pic.thumbnail(outputsize)
	pic.save(picture_path)
	return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your Account has been Successfully Updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form = form)



@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title = form.title.data, content = form.content.data, author = current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your Post has been created!', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title='New Post', form = form , legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Post Successfully Updated', 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':	
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', form = form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your Post has been deleted!', 'success')
	return redirect(url_for('home'))


def initUser():
	root_dir = dih.getRootDir(userName=current_user.username, parent=current_user.parent_org)	
	dirs = dih.getAllFoldersInAFolder(folder='.')	
	files = dih.getAllFilesInAFolder(folder='.')
	return [root_dir,dirs,files]

@app.route("/drive/")
@login_required
def drive():
	folder_icon = url_for('static', filename='driveIcons/folderIcon.png' )
	
	file_icon = getFolderIcon()
	info = initUser()
	dirs = info[1]
	folder = 'drive'
	return render_template('drive.html', title='Drive', image_file = file_icon, 
							image_folder = folder_icon, dirs= dirs, files = files, 
							cur_folder = folder, prev_folder = "")

def searchFolder(folder):
	root_dir = dih.getRootDir(userName=current_user.username, parent=current_user.parent_org)	
	dirs = dih.getAllFoldersInAFolder(folder='./' + folder)	
	files = dih.getAllFilesInAFolder(folder='./' + folder)
	return [root_dir,dirs,files]

def getFolderIcon():
	path = url_for('static', filename='driveIcons/document.png')
	picture_path =  os.getcwd() + '/project' + path	
	outputsize = (100,100)
	pic = Image.open(picture_path)
	pic.thumbnail(outputsize)
	pic.save(picture_path)
	return pic




@app.route("/drive/url=<path:name>")
@login_required
def subFolder(name):
	if name == 'drive':
		name = '.'
	else:
		name = name.replace('drive/', '')
	folder_icon = url_for('static', filename='driveIcons/folderIcon.png' )
	file_icon = url_for('static', filename='driveIcons/document.png')
	info = searchFolder(name)
	files = info[2]
	dirs = info[1]
	folder = name
	return render_template('drive.html', title='Drive', image_file = file_icon, image_folder = folder_icon,
							 dirs= dirs, files = files, cur_folder = folder, prev_folder = 'drive')

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

@app.route("/downloadFile/<path:abspath>", methods=['GET'])
@login_required
def downloadFile(abspath):
	info = searchFolder(abspath)
	root_dir = info[0]
	path = root_dir + '\\'+abspath
	filename = path_leaf(abspath)
	path = path.replace('\\','/')
	
	return send_file(path, attachment_filename=filename, as_attachment=True)

def getDest(file):
	root_dir = dih.getRootDir(userName=current_user.username, parent=current_user.parent_org)	
	destPath = dih.getDestinationPath(file=file)	
	return destPath

@app.route("/drive/upload", methods=['POST'])
@login_required
def upload_file():
	for file in request.files.getlist("file"):
		filename = file.filename
		if dih.validateFile(filename):
			destination = getDest(file=filename) + '/'+ filename
			print(destination)
			file.save(destination)
			flash('File(s) Uploaded!', 'success')
		else:
			flash('Invalid File!', 'danger')

	return redirect(url_for('drive'))



@app.route("/drive/deleteFile/<path:abspath>", methods=['GET'])
@login_required
def delete_file(abspath):
	info = searchFolder(abspath)
	root_dir = info[0]
	files = info[2]
	dirs = info[1]
	path = root_dir + '\\'+abspath
	filename = path_leaf(abspath)
	path = path.replace('\\','/')
	print('path',path)
	print('filename',filename)
	if os.path.exists(path):
		os.remove(path)
		flash(f'{filename} Deleted!', 'success')
	else:
		flash('Invalid File!', 'danger')
	return redirect(url_for('drive'))


@app.route("/drive/deleteDir/<path:abspath>/<int:delt>", methods=['GET'])
@login_required
def delete_directory(abspath,delt):
	info = searchFolder(abspath)
	root_dir = info[0]
	path = root_dir + '\\'+abspath
	path = path.replace('\\','/')
	dname = os.path.basename(os.path.dirname(path))
	print('path',path)
	print('dname',dname)
	if os.path.isdir(path):
		if(delt == 1):
			try:
				shutil.rmtree(path)
			except OSError as e:
				flash("Error: %s : %s" % (dname, e.strerror), 'danger')
		else:
			try:
				os.rmdir(path)
			except OSError  as e:
				flash("Error: %s : %s" % (dname, e.strerror) ,'warning')
				return redirect(url_for('drive'))
		flash(f'{dname} Deleted!', 'success')
	else:
		flash('Invalid Directory or Directory does not exists!', 'danger')
	return redirect(url_for('drive'))
