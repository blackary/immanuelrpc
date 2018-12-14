import util

class HTML(object):
    def __init__(self, content=None, tag=None, **attributes):
        self.content = util.toList(content)
        self.attributes = self.defaults()
        self.attributes.update(attributes)

    def defaults(self):
        return {}

    def i(self, content):
        'insert content'
        self.content += util.toList(content)
        return self
        
    def __call__(self, *args): 
        self.content += args
        return self
        
    def __setitem__(self, key, value):
        self.attributes[key] = value
        
    def __getitem__(self, key):
        return self.attributes[key]

    def __mul__(self, num): return str(self)*num        
    def __add__(self, element): return str(self)+str(element)
    def __radd__(self, element): return str(element)+str(self)

    def __str__(self): return str(self._build())
    def __repr__(self): return str(self._build())
    
    def _build(self):
        
        params = { 'tag':self.tag,
                    'content':self._buildContent(),
                    'attributes':self._buildAttributes(),
                 }
        
        return '''<%(tag)s %(attributes)s> 
                   %(content)s
                  </%(tag)s>''' % params

    def _buildContent(self):
        strContent = ''
        for c in self.content:
            strContent += str(c)
    
        return strContent

    def _buildAttributes(self):
        # handle special klass case
        if 'klass' in self.attributes:            
            self.attributes['class'] = self.attributes.pop('klass')
        
        strAttributes = ''
        for key, value in self.attributes.items():
            strAttributes += "%s='%s' " % (util.deCamel(key), value)

        return strAttributes

class HTMLPage(HTML): tag = 'html'
class Body(HTML): tag = 'body'
class Head(HTML): tag = 'head'
class Div(HTML): tag = 'div'
class Span(HTML): tag = 'span'
class Anchor(HTML): tag = 'a'
class Script(HTML): 
    tag = 'script'
    def defaults(self): return { 'type':'text/javascript'}
    
class Link(HTML): 
    tag = 'link'
    def defaults(self): return {'rel':'stylesheet', 'type':'text/css'}

class SCHTML(HTML):
    'self closing html'
    def _build(self):
        return '<%(tag)s %(attributes)s />' % {
            'tag':self.tag,
            'attributes':self._buildAttributes(),
            }
            
class Table(HTML):
    tag = 'table'
    def __init__(self, content=None, **attributes):
        tableContent = [c if isinstance(c, TR) else TR(c) for c in util.toList(content)]
        HTML.__init__(self, content=tableContent, **attributes)
        
    def defaults(self): return {'cellspacing':'0', 'cellpadding':'0'}

class TR(HTML): 
    tag = 'tr'
    def __init__(self, content=None, **attributes):
        rowContent = [c if isinstance(c, TD) else TD(c) for c in util.toList(content)]
        HTML.__init__(self, content=rowContent, **attributes)

class TD(HTML): tag = 'td'

class TextArea(HTML): tag = 'textarea'
class Option(HTML): tag = 'option'
class Select(HTML):
    tag = 'select'
    def __init__(self, content=None, **attributes):
        selectContent = [Option(c) for c in util.toList(content)]
        HTML.__init__(self, content=selectContent, **attributes)


class Image(SCHTML): tag = 'img'
class BR(SCHTML): tag = 'br'
class Input(SCHTML):
    tag = 'input'

    def _buildAttributes(self):
        return "type='%s' %s" % (self.inputType, HTML._buildAttributes(self))

class TextInput(Input): inputType = 'text'
class PasswordInput(Input): inputType = 'password'
class RadioInput(Input): inputType = 'radio'
class CheckBoxInput(Input): inputType = 'checkbox'
   
class JS(HTML):
    def _build(self):
        return 'function(){%s}'%self._buildContent()

class RPCCall(HTML):
    def __init__(self, name=None, rpcID=None):
        HTML.__init__(self)
        self.name = name
        self.rpcID = rpcID        

    def _build(self):
        script = '''
            var params = {"rpcID":"%s"};
            var argc = 0;
            $A(arguments).each(function(arg){
                params["arg"+(argc++)] = arg;
            }.bind(this));
            params['argc'] = argc;
            new Ajax.Request("/rpc/",
            {
                method:"post",
                onSuccess: function(transport) {                    
                    var scripts = transport.responseText;
                    eval(scripts);
                },
                parameters: params,
                onFailure: function(){ /*pass*/ }
            });

        ''' % self.rpcID
        return 'function %s(){%s;}'%(self.name, script)
        