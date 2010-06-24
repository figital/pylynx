import urwid

class Status(urwid.WidgetWrap):
	display_template = "[%s]"
	inactive_icon = "-"
	flags = {'Downloading': False,
			'Parsing': False,
			'UiWait': True}

	def __init__(self):
		self.status_text = urwid.Text('', "right")
		self.update_flags()
		super(Status, self).__init__(self.status_text)

	def update_flags(self):
		text = ''
		for key, default in self.flags.iteritems():
			if default:
				text += key[0]
			else:
				text += self.inactive_icon
		self.status_text.set_text(self.display_template % (text,))

	def get_text(self):
		self.update_flags()
		return self.status_text.get_text()

	def __getitem__(self, key):
		return self.flags[key]

	def __setitem__(self, key, value):
		self.flags[key] = value
		self.update_flags()

class TitleBar(urwid.WidgetWrap):
	def __init__(self):
		self.title = urwid.Text("Title")
		self.status = Status()
		self.columns = urwid.Columns((self.title, self.status))
		super(TitleBar, self).__init__(self.columns)
		self.status['Downloading'] = True
