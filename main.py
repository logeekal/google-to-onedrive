from wsgiref.simple_server import make_server as server
from beaker.middleware import SessionMiddleware as SM
import os,json
import app_conf as GLOBALS
from goog.signin import GoogleSignIn as google
from pages.main import main
from pages.welcome import welcome

import urlparse


def display_env(environ,start_response):
	env_list = ['%s : %s' % (key, value) for key, value in sorted(environ.items())]
	
	response_body =  '\n'.join(env_list) 
	
	status = '200 OK'
	
	response_headers = [
						('Content-Type','text/plain'),
						('Content-Length', str(len(response_body)))
						]
						
	start_response(status, response_headers)
	
	return [response_body]


def auth(environ, start_response, goog):
	auth_url = goog.get_auth_url()	
	start_response('302 Found',[('Location',auth_url)])
	return ['1']
	

def oauth2callback(environ, start_response,goog):
	qs = urlparse.parse_qs	(environ['QUERY_STRING'])
	auth_code =qs['code'][0]
	goog.put_auth_code(auth_code)
	creds = goog.get_credentials()
	user_info = goog.get_user_info(creds)
	print type(user_info), 'user_info : ', user_info
	user_id = user_info['id']

	
	if creds.refresh_token is not None:
		goog.store_credentials(user_id,creds)
		#Saving the user profile in a file.
		goog.store_user_info(user_info)	
	else:	
		stored_creds =  goog.get_stored_creds(user_id)	
		
		goog.refresh_token(stored_creds,user_id)
	red_url = '/welcome?id=' + user_id
	print 'Redirecting now to : ' + red_url
	start_response('302 Found',[('Location',str(red_url))])
	return ['1']

def read_static_files(environ, start_response):
	path = environ['PATH_INFO']
	path = path.replace(GLOBALS.STATIC_DIR, GLOBALS.STATIC_DIR_PREFIX)
	print path
	if os.path.exists(path) :
		ext = path[-3:]
		if ext in GLOBALS.MIME_TYPE:
			content_type = GLOBALS.MIME_TYPE[ext]
		else:
			content_type = 'text/plain'
		with open(path,'rb')as static_file:
			static_file = static_file.read()
			start_response('200 OK',[('Content-Type',content_type)] )
			return [static_file]
	else:
		print GLOBALS.MIME_TYPE['.html'] 
		start_response('404 Not Found',[('Content-Type',GLOBALS.MIME_TYPE['.html'])] )
		return ['1']
	 
def Application(environ, start_response):

	goog = google('drive')
	
	if environ['PATH_INFO'] == '/authenticate':
		return auth(environ, start_response, goog)
	if environ['PATH_INFO'] == '/':
		main_page = main()
		return main_page.run(environ, start_response)
	if environ['PATH_INFO'] == '/oauth2callback':
		return oauth2callback(environ, start_response, goog)
	if environ['PATH_INFO'] == '/welcome':
		welcome_page = welcome(goog)
		return welcome_page.run(environ, start_response)
	if environ['PATH_INFO'] == '/env':
		return display_env(environ, start_response)
	if environ['PATH_INFO'].startswith(GLOBALS.STATIC_DIR):
		return read_static_files(environ, start_response)	

Application = SM(Application)
httpd =  server('10.0.2.15',8051, Application)
print  "Serving start"
httpd.serve_forever()
	
