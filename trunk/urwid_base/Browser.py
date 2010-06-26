import urllib2
import urwid
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

def fetchSource(location):
	if location[0:8] == 'file:///':
		return open(location[6:]).read()
	elif location[0:7] == 'http://':
		return urllib2.urlopen(location).read()
	elif location[0:7] == 'https://':
		raise NotImplementedError()
	else: # Bad
		return urllib2.urlopen('http://'+location).read()

