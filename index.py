#coding=utf-8
import web
import urllib2, urllib
import json

web.config.debug = False
urls = (
	'/','default',
	'/login','login',
	'/reset','reset',
	'/download','download',
)

app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('userstatus'),
							  initializer={'account': None, 'passwd': None})
render = web.template.render('templates/')

class default:
	def GET(self):
		if session.account:
			return render.default(session.account)
		else:
			web.seeother('/login')
	
class login:
	def POST(self):
		account, passwd = web.input().account, web.input().passwd
		data = {'login_email':account,'login_password':passwd,
				'format':'json'}
		f = urllib2.urlopen(
			url = 'https://dnsapi.cn/User.Detail',
			data = urllib.urlencode(data)
		)
		jsondict = json.loads(f.read())
		if jsondict['status']['code'] == '1':
			session.account, session.passwd = account, passwd
			raise web.seeother('/')
		else:
			return render.login('账户名或密码错误。')
	def GET(self):
		if not session.account:
			return render.login()
		else:
			web.seeother('/')

class reset:
	def GET(self):
		session.kill()
		web.seeother('/login')
		
class download:
	def GET(self):
		if session.account:
			data = {'login_email':session.account,
					'login_password':session.passwd,
					'format':'json'}
			f = urllib2.urlopen(
				url = 'https://dnsapi.cn/Domain.List',
				data = urllib.urlencode(data)
			)
			f2 = urllib2.urlopen(
				url = 'https://dnsapi.cn/Record.List',
				data = urllib.urlencode(data)
			)

			web.header('Content-Type','application/octet-stream')
			web.header('Content-disposition','attachment; filename='+session.account+'.bak')
			return f.read()+'\n'+f2.read()

if __name__ == '__main__':
	app.run()
