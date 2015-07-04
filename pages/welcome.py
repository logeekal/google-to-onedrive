import urlparse
import os, json
import requests
import app_conf as GLOBALS

welcome_html = """
<html>
<head>
<title>Welcome %s</title>
<script type="text/javascript" src="/static/utilities.js"></script>
""" + GLOBALS.SCRIPT_TAG + """
</head>
<body>
	<pre>
		Welcome %s
	</pre>
	<div class="filebox">

	<!--	<form name=file_list>         -->
			%s
	<!--	</form>  -->
	</div>
</body>
</html>
"""

class welcome:
	def __init__(self, google):
		self.goog = google
		
	def run(self, environ, start_response):
		qs = urlparse.parse_qs(environ['QUERY_STRING'])
		user_id = qs['id'][0]
		if user_id is not None:
			with open(os.getcwd()+'/config/'+user_id+'_profile.json','r') as profile_file:
				profile = json.load(profile_file)
			print 'profile ' , profile
			name = str(profile['name'])
			
			#start service
			result =[]
			service = self.goog.build_service(user_id)
			params = {
					'maxResults' : 65,
					'q'	     : 'mimeType = \'application/vnd.google-apps.folder\''
				}
			results = service.files().list(**params).execute()
			files = """ """
			for items in results['items']:
				files  = files + """
						<input type=checkbox name=filelist>""" + """<a href=""" + str(items['alternateLink'])+ """>"""+str(items['title']) + """</a><br>
					 	 """
			resp_body = welcome_html %(name,name,files)
		else:
			resp_body = welcome_html % ('Error','Error')
		session = environ['beaker.session']
		if 'user' not in session:
			session['user'] = user_id
			session.save()			
		start_response('200 OK',[('Content-Type','text/html'),('Content-Length',str(len(resp_body)))])
		return [resp_body]
	

