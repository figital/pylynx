import urwid

class UrlChange(Exception):
	'''Simple exception to trigger a request for URL change'''
	pass

class UrlBar(urwid.Edit):
	'''Implements UI functionality for entering URLs'''
	select_all = False

	def __init__(self, location=""):
		super(UrlBar, self).__init__(location)

	def keypress(self, size, key):
		if self.select_all:
			if key == 'esc':
				self.select_all = False
				self.redraw()
				return
			elif key == 'enter':
				self.preserve_url()
				self.select_all = False
				self.redraw()
				raise UrlChange()
			elif key in ('left', 'home'):
				self.select_all = False
				self.set_edit_pos(0)
			elif key in ('right', 'end'):
				self.select_all = False
				self.set_edit_pos(len(self.edit_text))
			else:
				self.select_all = False
				self.set_edit_text('')

		else:
			if key == 'esc':
				self.cancel_edit()
				return
			elif key == 'enter':
				self.preserve_url()
				raise UrlChange()
				
		super(UrlBar, self).keypress(size, key)

	def get_text(self):
		text, attributes = super(UrlBar, self).get_text()
		if self.select_all:
			attributes = [('highlighted', len(text)),]
		return text, attributes

	def preserve_url(self):
		self.preserved_url = self.get_edit_text()

	def cancel_edit(self):
		self.select_all = False
		self.set_edit_text(self.preserved_url)

	def begin_focus(self):
		self.select_all = True
		self.preserve_url()
		self.redraw()

	def redraw(self):
		self.set_edit_text(self.get_edit_text()) # Really bad, I don't know how to trigger a redraw yet.

