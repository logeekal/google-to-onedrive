#!usr/bin/python

import os
import httplib2
import pprint
import json

from apiclient.discovery import build
from apiclient.http import MediaFileUpload as uploader
from oauth2client.client import OAuth2WebServerFlow as oauth2
from oauth2client.client  import FlowExchangeError as flexerror

class GoogleSignIn:
	"""
	StandAlone class for handling google Sign In
	"""
	def __init__(self,scope):
		cwd = os.getcwd()

		with open(cwd + "/config/CLIENT_ID.json") as json_file:
			json_data = json.load(json_file)

		self.CLIENT_ID = json_data['web']['client_id']
		self.CLIENT_SECRET = json_data['web']['client_secret']
		
		self.SCOPE = json_data['scopes']['drive']
		
		self.RED_URI = json_data['web']['redirect_uris'][0]
		self.flow = oauth2(self.CLIENT_ID,self.CLIENT_SECRET,self.SCOPE,redirect_uri=self.RED_URI)

			
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

	def store_credentials(self, user_id, credentials):
		cwd = os.getcwd()
		cred_path = cwd + '/config/' + user_id + '.json'
		
		if os.path.exists(cred_path):
			return False
		else:
			file = open(cred_path, 'w')
			print credentials.to_json()
			file.write(credentials.to_json())
			return True

	def build_service(self):
		http = http2lib.Http()
		http = credentials.authorize(http)
		
		return build('drive','v2',http=http)
	
#goog = GoogleSignIn('drive')
#goog.get_auth_url()

		
