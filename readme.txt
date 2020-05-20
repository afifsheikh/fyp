database video:
https://www.youtube.com/watch?v=cYWiDiIUxQc


admin_role = Role(name='Admin')

PATH:
"D:\SAM\GIT_dir\Python-Flask-\FYP_UI_1"

to change your database you just need to pass a different URL to the sqlalchemy.


from project import db

from project.models import User, Post, Role
to create database type this in command line (don't forget to import db):
db.create_all

to drop database type this in command line (don't forget to import db):
db.drop_all()


>>>pip install flask

>>>pyhton -m flask --version

>>>set FLASK_APP=flaskBlog.py

>>>flask run 
>>>python -m flask run

>>>python flaskBlog.py 
(after add the following code in the file
if __name__ == '__main__':
	app.run(debug=True)
)
-------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------
(for web registration validation) flask WTForms
>>>pip install flask-wtf 

------------------------------------------------------------------------------------------------------------------
(database) sql-alchemy
>>>pip install flask-sqlalchemy


// ADD USER
>>> from flaskBlog import db
>>> db.create_all()
>>> from flaskBlog import User, Post
>>> user_1 = User(username='Muneeb', email='m@demo.com', password='password')
>>> db.session.add(user_1)
>>> db.session.commit()

>>> User.query.all()	-->> select * from [tableName]
>>>user = User.query.get([id])
>>> user = User.query.filter_by(email='sk@demo.com').first()

>>> User.query.filter_by(email='sk@demo.com').first()
User('Sheikh', 'sk@demo.com', 'default.jepg') --> no List
>>> User.query.filter_by(email='sk@demo.com').all()
[User('Sheikh', 'sk@demo.com', 'default.jepg')] -->> LIST
>>> user.id


// DELETE USER
>>> User.query.filter_by(email='muneeb@flaskblog.com').delete()
1


>>> user.posts
[]

>>> for post in user.posts:
...     print(post.title)
...
Blog 1
Blog 2
>>> post_1 = Post(title='Blog 1', content='First Post Content!', user_id=user.id)
>>> post_2 = Post(title='Blog 2', content='Second Post Content!', user_id=user.id)
>>> db.session.add(post_1)
>>> db.session.add(post_2)
>>> db.session.commit()

>>> user.posts
[Post('Blog 1', '2019-09-03 12:08:02.125635' ), Post('Blog 2', '2019-09-03 12:08:02.130573' )]

>>> post = Post.query.first()
>>> post
Post('Blog 1', '2019-09-03 12:08:02.125635' )
>>> post.user_id
1

/**
author is not a column in Post table but because it was defined in the relationship in User as a 'backref'
that's why we can call all the user information from the author attribute.
**/
>>> post.author
User('Muneeb', 'm@demo.com', 'default.jepg')
>>> post.author.username
'Muneeb'
>>> db.drop_all()
>>> db.create_all()
>>> User.query.all()
[]
>>> Post.query.all()
[]
>>>

#################################################
database tutorial in part 5
https://www.youtube.com/watch?v=44PvX0Yv368
#################################################
--------------------------------------------------------------------------------------------------------------
>>> pip install flask_bcrypt
>>>python
>>> from flask_bcrypt import Bcrypt
>>> bcrypt = Bcrypt()

>>> bcrypt.generate_password_hash('testing')
b'$2b$12$0rWLTrchk982VId0OQEQ8uREW8vmCUcBSas5h1IyctHdoCvy2.hyq'

>>> bcrypt.generate_password_hash('testing').decode('utf-8')
'$2b$12$eYl2LgHALYQ7F1VoIIyQRe12AP28WgQA6FJLl77OnBbzawfV9TBIq'
>>> bcrypt.generate_password_hash('testing').decode('utf-8')
'$2b$12$1/jyqTsrMs9Vuf286h9MyeuN9SxMqyDYb26xeOuLD5kFjtv7oowwm'

>>> hashed_pw = bcrypt.generate_password_hash('testing').decode('utf-8')
>>> bcrypt.check_password_hash(hashed_pw, 'password')
False
>>> bcrypt.check_password_hash(hashed_pw, 'testing')
True

 >>>pip install flask-login


installed Pillow to compress images to smaller size
>>>pip install Pillow

from PIL import Image 


----------------------------------------------------------------------------
----------------------------------------------------------------------------
static scripts
----------------------------------------------------------------------------
----------------------------------------------------------------------------
to run the application execute the following script:
--> go to the application directory in cmd
>>> python run.py

to login use following credentials
email: admin@admin.com
password: admin





``````````````````````````````````````````````````````````````````````````````
``````````````````````````````````````````````````````````````````````````````
CURRENT 
``````````````````````````````````````````````````````````````````````````````
``````````````````````````````````````````````````````````````````````````````

15/12/2019
user can create post, but cannot add to db

17/12/2019
post added to database and also displayed on home page with some formating


flask Blog part 8
https://www.youtube.com/watch?v=u0oDDZrDz9U
@: 17:53

	<a href="{{ url_for('subFolder_drive', folder=d) }}"><li> {{ d }} </li></a> 

<ul>
	<li>Files</li>
	{% for f in files %}
	<li> {{ f }} </li>
	{% endfor %}
</ul>

{% if cur_folder == 'drive' %}
				<a href="{{ url_for('subFolder', name=d) }}">
			{% endif %}