import requests, os

with open(os.getcwd()+'/config/goog_conf.json') as config:
	config = json.loads(config)



class gdriveOps:
	def __init__(self, GoogleSignin):
		req_url = config['DRIVE_REQUEST_URL']
	def get_files(self, params):
		

