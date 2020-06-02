import ntpath
import os
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
		print(current_user)
	posts = Post.query.all()
	return render_template('home.html', posts=posts)

@app.route("/about")
def about():
	return render_template('about.html', title='About')

# @app.route("/admin")
# def admin():
# 	return render_template('adminsite/html/index.html')


# folder = 'pdf'
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
		#org_chk = User.query.filter_by(username=form.org_code.data).first()
		emp = User(username=form.username.data, email=form.email.data, password=hashed_password, parent_org=form.org_code.data)
		#if form.org_code.data = org_chk.username:
		empreq = empRequest(empname=form.username.data, orgname=form.org_code.data) 
		db.session.add(empreq)
		emp_role = Role.query.filter_by(name='emp').first()
		emp.roles = [emp_role]
		db.session.add(emp)
		db.session.commit()
		flash("You have been registered Successfully. Please wait until you are approved!", 'success')
		# else:
		# 	flash("There Is no Such Organization", 'warning')
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
		# admin = Role.query.filter_by(name='org').first()
		# user.roles = [admin]
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
		# usertype = form.userTpye.data
		# if usertype == 'employee':
		# 	emp = Employee.query.filter_by(email=form.email.data).first()
		# 	if emp and bcrypt.check_password_hash(emp.password, form.password.data):
		# 		print(emp)
		# 		login_user(emp, remember=form.remember.data)
		# 		next_page = request.args.get('next') #args is a dictionary we use get method so that if the next prameter dost not exits it gives none so dont use square brackets with the key
		# 		initUser()
		# 		flash("Login Successful " + current_user.username , "success")
		# 		return redirect(next_page) if next_page else redirect(url_for('home')) # this is done so that if login page is directed from a restricted page then after login it redirects to that page instead of home page
			
		# elif usertype == 'organization':
		# 	org = Organization.query.filter_by(email=form.email.data).first()
		# 	if org and bcrypt.check_password_hash(org.password, form.password.data):
		# 		login_user(org, remember=form.remember.data)
		# 		next_page = request.args.get('next') #args is a dictionary we use get method so that if the next prameter dost not exits it gives none so dont use square brackets with the key
		# 		initOrg()
		# 		flash("Login Successful" , "success")
		# 		return redirect(next_page) if next_page else redirect(url_for('home')) # this is done so that if login page is directed from a restricted page then after login it redirects to that page instead of home page
		# else:
		user = User.query.filter_by(email=form.email.data).first()
		
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			if str(user.parent_org) != 'None':
				print(user.parent_org)
				print(user.parent_org != 'None')
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
# @roles_required('org')
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
			# employee List 
			emplst = empList.query.filter_by(orgname=current_user.username).all()
			newEmpLst = []
			for rec in emplst:
				e = User.query.filter_by(username=rec.empname).first()
				newEmpLst.append(e)
			print(f'LIST : {newEmpLst}')
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
		print(current_user)
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
	# Organization me ye org_name hy
	# yahan pe check kro k current_user.role == 'employee' to phr
	# rootFolder =  current_user.parent . '/' . current_user.username;
	
	print(f'praent naem: {current_user.parent_org}')
	root_dir = dih.getRootDir(userName=current_user.username, parent=current_user.parent_org)	
	dirs = dih.getAllFoldersInAFolder(folder='.')	
	files = dih.getAllFilesInAFolder(folder='.')
	print(f'root_dir: {root_dir}')
	return [root_dir,dirs,files]
	# flash(dirs)
# def initOrg():
# 	# Organization me ye org_name hy
# 	root_dir = dih.getRootDir(userName=current_user.organization_name)	
# 	dirs = dih.getAllFoldersInAFolder(folder='.')	
# 	files = dih.getAllFilesInAFolder(folder='.')
# 	return [root_dir,dirs,files]

@app.route("/drive/")
@login_required
def drive():
	folder_icon = url_for('static', filename='driveIcons/folderIcon.png' )
	# file_icon = url_for('static', filename='driveIcons/document.png')
	
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
	# flash(dirs)

def getFolderIcon():
	# random_hex = secrets.token_hex(8)
	# _, f_ext = os.path.splitext(icon.filename)
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
	# name = name.replace('drive', '')

	folder_icon = url_for('static', filename='driveIcons/folderIcon.png' )
	file_icon = url_for('static', filename='driveIcons/document.png')
	# folder_icon = getFolderIcon(icon = folder_icon)
	# file_icon = getFolderIcon()	
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
	print(abspath)
	# root_dir,dirs,files = searchFolder(abspath)
	info = searchFolder(abspath)
	root_dir = info[0]
	files = info[2]
	dirs = info[1]
	print(f'userName:{root_dir}, dirs: {dirs}, files{files}')
	
	path = root_dir + '\\'+abspath
	filename = path_leaf(abspath)
	# filename = os.path.splitext(abspath)[0]
	# ext = os.path.splitext(abspath)[1]
	# path = "Users\\root_admin686\\textFiles\\README.TXT"
	# filename = path_leaf(name)
	path = path.replace('\\','/')
	
	print('path',path)
	print('filename',filename)
	return send_file(path, attachment_filename=filename, as_attachment=True)
	# return send_from_directory(directory=path, filename='README.TXT', as_attachment=True)

# @app.route("/upload_file")
# @login_required
# def upload():
# 	return render_template('uploadFile.html', title='upload file')


def getDest(file):
	print(current_user.parent_org)
	root_dir = dih.getRootDir(userName=current_user.username, parent=current_user.parent_org)	
	destPath = dih.getDestinationPath(file=file)	
	return destPath

@app.route("/drive/upload", methods=['POST'])
@login_required
def upload_file():
	for file in request.files.getlist("file"):
		print(file)
		filename = file.filename
		if dih.validateFile(filename):
			destination = getDest(file=filename) + '/'+ filename
			print(destination)
			# if os.path.isfile(destination):
			# 	flash('File already Exists!', 'success')
			# 	return redirect(url_for('drive'))
			file.save(destination)
			flash('File(s) Uploaded!', 'success')
		else:
			flash('Invalid File!', 'danger')

	return redirect(url_for('drive'))





#function on btn submit id base pe table list insert select req table del reqemp

# @roles_required('org')

	# for role in current_user.roles:
	# 	if role == adminRole or role == orgRole:
	# 		req1 = empRequest.query.filter_by(orgname=current_user.username)
	# 		newReq1 = []
	# 		for rec in req1:
	# 			e = User.query.filter_by(username=rec.empname).first()
	# 			newReq1.append(e)
	# 		print(newReq1)
	# 		empl = empList(empname = req1.empname, orgname=req1.orgname)
	# 		db.session.add(empl)
	# 		db.session.commit()
	# 		return render_template('org_dashboard.html', title='Dashboard',newReq = newReq1)

		
# 	abort(403)


		
