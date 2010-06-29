import urwid
import TitleBar, UrlBar

class TopWindow(urwid.Pile):
	def __init__(self, browser):
		self.browser = browser
		self.titlebar = TitleBar.TitleBar()
		self.contentArea = urwid.Pile((urwid.Text(''),))
		self.urlbar = UrlBar.UrlBar()
		super(TopWindow, self).__init__((self.titlebar, self.urlbar, self.contentArea), self.urlbar)

	def keypress(self, size, key):
		if key not in ('up', 'down'): # Stop Pile from changing focus
			try:
				super(TopWindow, self).keypress(size, key)
			except UrlBar.UrlChange:
				self.browser.urlbar_navigate()

	def set_focus(self, item):
		if item is self.urlbar:
			item.set_edit_text('crap')
			item.begin_focus()

		super(TopWindow, self).set_focus(item)

