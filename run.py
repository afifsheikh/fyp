
from project import app

if __name__ == '__main__':
	website_url = '127.0.0.1:5001'
	# website_url = '192.168.0.107:4996'
	# website_url = 'localhost:4996'
	# website_url = '10.133.128.149:5000'
	#app.config['SERVER_NAME'] = website_url
	app.run(host ='0.0.0.0', port = 5000, debug = True) 
	#app.run(debug=True)