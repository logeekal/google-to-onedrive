from wsgiref.simple_server import make_server as server

from goog.signin import GoogleSignIn as google
from pages.main import main

import urlparse

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
	user_id = user_info['id']

	print goog.store_credentials(user_id,creds)
	 
def Application(environ, start_response):

	goog = google('drive')
	
	if environ['PATH_INFO'] == '/authenticate':
		return auth(environ, start_response, goog)
	if environ['PATH_INFO'] == '/':
		main_page = main()
		return main_page.run(environ, start_response)
	if environ['PATH_INFO'] == '/oauth2callback':
		return oauth2callback(environ, start_response, goog)




httpd =  server('10.0.2.15',8051, Application)
print  "Serving start"
httpd.serve_forever()
	
