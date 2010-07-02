import urllib2
import xml.dom.minidom
import urwid
import BeautifulSoup
import TopWindow
import Renderer

class Browser(object):
	def __init__(self):
		super(Browser, self).__init__()
		self.display = TopWindow.TopWindow(self)
		self.renderer = Renderer.Renderer(self.display)
		fill = urwid.Filler(self.display, 'top')
		palette = [('highlighted', 'default,standout', 'default', 'default'),]
		loop = urwid.MainLoop(fill, palette)
		loop.run()

	def urlbar_navigate(self):
		self.navigate(self.display.urlbar.get_edit_text())

	def navigate(self, location):
		self.display.titlebar.status.clear_flags()
		self.display.titlebar.status['Downloading'] = True
		source = self.fetchSource(location)
		self.display.titlebar.status['Downloading'] = False

		self.display.titlebar.status['Parsing'] = True
		soup = BeautifulSoup.BeautifulSoup(source, convertEntities=BeautifulSoup.BeautifulSoup.ALL_ENTITIES)

		for script in soup.findAll(name='script'):
			script.replaceWith(BeautifulSoup.CData(str(script.string)))

		dom = xml.dom.minidom.parseString(str(soup.html))
		self.display.titlebar.status['Parsing'] = False
		

		self.display.titlebar.status['Rendering'] = True
		self.renderer.render(dom)
		self.display.titlebar.status['Rendering'] = False

		self.display.titlebar.status['UserInputNeeded'] = True

	# The whole resource grabbing architecture will change as I find myself
	# needing to send POST requests, include cookies, handle HTTP codes, etc.
	# Therefore, don't put much effort into this yet.
	def fetchSource(self, location):
		colonIndex = location.find(':')
		if colonIndex >= 0: # Use given protocol.
			protocol = location[:colonIndex]
			if protocol == 'http':
				return urllib2.urlopen(location).read()

			elif protocol == 'https':
				# Later. This will involve root CAs and all sorts of crazy shit.
				raise NotImplementedError('SSL not yet supported!')
		
			elif protocol == 'file':
				fileName = location[7:]
				return open(fileName).read()

		else: # Need to guess protocol.
			raise NotImplementedError('Protocol guessing not done yet!')
