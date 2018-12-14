import os

from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from controller import Controller
import util

class RPCHandler(Controller):
    def post(self):
        args = self.getArgs()
        scripts = self.runRPCHandler(args)        
        self.response.headers['Content-Type'] = 'text/json'
        self.response.out.write(';'.join(scripts).replace('\n',' ').replace('\r',' '))
        self.response.out.flush()

    def getArgs(self):
        args = []
        numArgs = int(self.request.get('argc'))
        for i in range(numArgs):
            args.append(str(self.request.get('arg%d'%i)))
            
        return args
    
    def runRPCHandler(self, args):        
        rpcID = self.request.get('rpcID')        

        methodName, className, moduleName = util.rpcMethod(rpcID)
        
        try:
            module = __import__(moduleName)
            _class = module.__getattribute__(className)
            controllerObj = _class().setup()
            method = controllerObj.__getattribute__(methodName)
        except:
            self.error(403)

#        try:
#            method(*args)
#        except:
#            self.registerScript()
            
        method(*args)
        
        return controllerObj.registeredScripts
