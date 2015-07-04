main_html = """
<html>
<head>
<title> Main Page </title>




</head>
	<form method='post' action='/authenticate'>
		<input type='Submit' value = 'Google SignIn' onClick="return popup('/authenticate')">
	</form>
</html>
"""

'''
def main1(environ, start_response):

	resp_body = main_html
	resp_status = '200 OK'
	response_header = [
				('Content-Type','text/html'),
				('Content-Length', str(len(resp_body)))
			  ]
	start_response(resp_status, response_header)
	return [resp_body]
'''


class main():
	def __init__(self):
		pass
	def run(self, environ, start_response):
		session = environ['beaker.session']
		if 'user' in session:
			red_url = '/welcome?id=' + str(session['user'])
			start_response('302 Found', [('Location',red_url)])
			return ['1']
		else:
			resp_body = main_html
			resp_status = '200 OK'
			response_header = [
					('Content-Type','text/html'),
					('Content-Length', str(len(resp_body)))
			 		 ]	
			start_response(resp_status, response_header)
			return [resp_body]
	

