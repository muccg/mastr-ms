# -*- coding: UTF-8 -*-
try: import json as simplejson
except ImportError: import simplejson

st = u'Е乂αmp١ȅ'

a = {}
#a[u'hello'] = 'world'
a[u'Е乂αmp١ȅ'] = 'bar'

print 'A unicode string looks like: ', st.encode('utf-8')
print 'Dict is: ', a
print 'Dump of dict json is: ', simplejson.dumps(a)
print 'Reconstituted dict is: ', simplejson.loads(simplejson.dumps(a))

if a.keys()[0].encode('utf-8') == st.encode('utf-8'):
    match = True
else:
    match = False
print 'Check if string matches reconst dict key: ', match
