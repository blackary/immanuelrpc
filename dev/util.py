
def toList(items):
    if not items:
        return []
    if not(isinstance(items, tuple) or isinstance(items, list)):
        items = [items]
    return items
    
    
def deCamel(name):
    s = ''
    for c in name:
        s += '-'+c if c.isupper() else c
    return s
    

DES_SALT = 'SC3dM0wT'
    
def rpcID(method):

    methodName = method.im_func.func_name
    className  = method.im_class.__name__
    moduleName = method.im_class.__module__
    
    methID = '%s.%s.%s' % (methodName, className, moduleName)
    
    from pyDes import des
    key = des(DES_SALT)
    rpcID = key.encrypt(methID, pad=' ')
    
    import base64
    rpcID64 = base64.b64encode(rpcID)
    
    return rpcID64
    
    
def rpcMethod(rpcID64):
    import base64
    rpcID = base64.b64decode(rpcID64)
    
    from pyDes import des
    key = des(DES_SALT)
    methID = key.decrypt(rpcID, pad=' ')
    
    moduleName, className, methodName = methID.split('.')
    
    return moduleName, className, methodName
