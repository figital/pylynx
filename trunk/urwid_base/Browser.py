import urllib2
import xml.dom.minidom
import urwid
import BeautifulSoup
import TopWindow

class Browser(object):
	def __init__(self):
		super(Browser, self).__init__()
		self.display = TopWindow.TopWindow(self)
		fill = urwid.Filler(self.display, 'top')
		palette = [('highlighted', 'default,standout', 'default', 'default'),]
		loop = urwid.MainLoop(fill, palette)
		loop.run()

	def urlbar_navigate(self):
		self.navigate(self.display.urlbar.get_edit_text())

	def navigate(self, location):
		self.display.titlebar.status.clear_flags()
		self.display.titlebar.status['Downloading'] = True
		source = fetchSource(location)
		self.display.titlebar.status['Downloading'] = False
		self.display.titlebar.status['Parsing'] = True
		soup = BeautifulSoup.BeautifulSoup(source, convertEntities=BeautifulSoup.BeautifulSoup.ALL_ENTITIES)
		
		for script in soup.findAll(name='script'):
			script.replaceWith(BeautifulSoup.CData(str(script.string)))

		dom = xml.dom.minidom.parseString(str(soup.html))
		self.display.titlebar.status['Parsing'] = False

def fetchSource(location):
	if location[0:8] == 'file:///':
		return open(location[6:]).read()
	elif location[0:7] == 'http://':
		return urllib2.urlopen(location).read()
	elif location[0:7] == 'https://':
		raise NotImplementedError()
	else: # Bad
		return urllib2.urlopen('http://'+location).read()

