#!usr/bin/python

import os
import httplib2
import pprint
import json
import requests

from apiclient.discovery import build
from apiclient.http import MediaFileUpload as uploader
from oauth2client.client import OAuth2WebServerFlow as oauth2
from oauth2client.client  import FlowExchangeError as flexerror

class GoogleSignIn:
	"""
	StandAlone class for handling google Sign In
	"""
	def __init__(self,scope):
		self.cwd = os.getcwd()

		with open(self.cwd + "/config/CLIENT_ID.json") as json_file:
			json_data = json.load(json_file)

		self.CLIENT_ID = json_data['web']['client_id']
		self.CLIENT_SECRET = json_data['web']['client_secret']
		
		self.SCOPE = json_data['scopes']['drive']
		
		self.RED_URI = json_data['web']['redirect_uris'][0]
		self.flow = oauth2(self.CLIENT_ID,self.CLIENT_SECRET,self.SCOPE,redirect_uri=self.RED_URI)
		self.config_dir = self.cwd + '/config/'
			
	def get_auth_url(self):
		self.authorize_url = self.flow.step1_get_authorize_url()
		print type(self.authorize_url) , self.authorize_url
		return self.authorize_url	
	
	def put_auth_code(self, auth_code):
		self.auth_code = auth_code

	
	def get_credentials(self, auth_code=1):
		if auth_code == 1:
			auth_code = self.auth_code
		try:
			self.credentials = self.flow.step2_exchange(auth_code)
			print self.credentials.access_token, dir(self.credentials)
			return self.credentials
		except flexerror, error:
			print 'Error  : ' + error 
	
	def get_user_info(self,credentials):
		'''
		Return User info as JSON with the help of credentials
		'''
		self.user_info_service =  build(serviceName = 'oauth2', version='v2', http=credentials.authorize(httplib2.Http()))	
		self.user_info = None
		
		user_info =  self.user_info_service.userinfo().get().execute()
		return user_info

	def store_user_info(self, user_info):
		'''
		Stores user_info in the local disk
		'''
		with open(self.config_dir+user_info['id']+'_profile.json', 'w') as user_file:
			user_file.write(json.dumps(user_info))

	def store_credentials(self, user_id, credentials):
		self.cwd = os.getcwd()
		cred_path = self.cwd + '/config/' + user_id + '.json'
		
	
		file = open(cred_path, 'w')
		print credentials.to_json()
		file.write(credentials.to_json())
		return True
	
	def get_stored_creds(self,user_id):
		'''
		This routine gets stored credentials from the system as a json file.
		'''
		with open(self.cwd+'/config/'+user_id+'.json') as cred_file:
			stored_creds = json.load(cred_file)
		return stored_creds


	def refresh_token(self, credentials,user_id):
		'''
		This routine checks if the token is expired or not.
		If token is expired, it asks for a new refresh token
		and otherwise it doesn't do anything.
		'''
	
		print type(credentials), credentials	
		token_host = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=' + credentials['access_token']
		refresh_token_uri = 'https://www.googleapis.com/oauth2/v3/token'	
		req =  requests.get(token_host)
		if 'error' in req.json():
			print 'Token needs to be refreshed'
			request_text = {
					"refresh_token" :  credentials['refresh_token'],
"client_id" : credentials['client_id'],
"client_secret" : credentials['client_secret'],
"grant_type" : 'refresh_token'
					}
			req = requests.post(refresh_token_uri,params=request_text)
			print 'JSON Response - ', req.json()	
		 
			credentials['access_token']=req.json()['access_token']
			for key in credentials['token_response'].keys():
				if key in req:
					credentials['token_response'][key] = req[key]
			with open(self.config_dir + user_id + '.json','w') as cred_file:
				cred_file.write(json.dumps(credentials))
			return True
		return 1		 
		
		
	def build_service(self):
		http = http2lib.Http()
		http = credentials.authorize(http)
		
		return build('drive','v2',http=http)
	
#goog = GoogleSignIn('drive')
#goog.get_auth_url()

'''
should be called like this in oauth2 call function
	qs = urlparse.parse_qs	(environ['QUERY_STRING'])
	auth_code =qs['code'][0]
	goog.put_auth_code(auth_code)
	creds = goog.get_credentials()
	user_info = goog.get_user_info(creds)
	user_id = user_info['id']
	
	if creds.refresh_token is not None:
		goog.store_credentials(user_id,creds)
	else:
		stored_creds =  goog.get_stored_creds(user_id)	
		print type(stored_creds)
		
		goog.refresh_token(stored_creds,user_id)
'''	
