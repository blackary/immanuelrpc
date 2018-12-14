import sys, os
sys.path.append('/var/www/immanuelrpc.com/trunk/dev')

from controller import *


def application(environ, start_response):
	status = '200 OK'
	output = 'Hello World!'

	response_headers = [('Content-type', 'text/plain'),
											('Content-Length', str(len(output)))]
	start_response(status, response_headers)

	controller = ImmanuelRPCController(environ)
	response = controller.get()

	try:
		pass
	except:
		response = str(sys.exc_info()[0])
	return [response]


class ImmanuelRPCController(Controller):
	def head(self):
		head = Head(title='ImmanuelRPC Dev')
		return head

