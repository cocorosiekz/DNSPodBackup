import urllib2, urllib
import json

data = {'login_email':'cocorosiekz@gmail.com',
		'login_password':'alakb3kk',
		'format':'json'}
f = urllib2.urlopen(
	url = 'https://dnsapi.cn/User.Detail',
	data = urllib.urlencode(data)
)
text = f.read()
print type(text)
print type(json.loads(text))
print type(json.dumps(json.loads(text),indent=4))
print json.loads(text)['status']['code']
