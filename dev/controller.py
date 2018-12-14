import util
from view import *


class Controller(object):
	def __init__(self, request):
		self.request = request
	
	def head(self):
		head = Head(title='Default Title') 
		return head        
	
	def body(self):
		body = Body()
		body(self.content(), 
		self.scripts())
		return body
	
	def page(self):        
		page = HTMLPage()
		page(self.head(),
		self.body())
		return page
	
	def content(self):
		return "Default Content"
	
	def scripts(self):
		script = Script()
		for s in self.registeredScripts:
			script(s)
			return script
	
	def setup(self):
		self.registeredScripts = []
		return self
	
	def get(self):
		self.setup()
		page = self.page()
		return str(page)
	
	def registerScript(self, script):
		self.registeredScripts.append(script)
	
	def connectRPC(self, jsfunction, method):
		rpcID = util.rpcID(method)
		rpc = RPCCall(jsfunction, rpcID)
		self.registerScript(rpc)


