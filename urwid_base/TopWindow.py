import urwid
import TitleBar, UrlBar

class TopWindow(urwid.Pile):
	def __init__(self):
		self.titlebar = TitleBar.TitleBar()
		#self.text = urwid.Text("Title")
		self.urlbar = UrlBar.UrlBar()
		#super(TopWindow, self).__init__((self.text, self.urlbar), self.urlbar)
		super(TopWindow, self).__init__((self.titlebar, self.urlbar), self.urlbar)

	def keypress(self, size, key):
		if key not in ('up', 'down'):
			try:
				super(TopWindow, self).keypress(size, key)
			except UrlBar.UrlChange:
				url = self.urlbar.get_edit_text()
				#self.text.set_text("Loading %s..." % url,)

	def set_focus(self, item):
		if item is self.urlbar:
			item.set_edit_text('crap')
			item.begin_focus()

		super(TopWindow, self).set_focus(item)

