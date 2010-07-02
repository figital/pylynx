import HTML

class Renderer(object):
	def __init__(self, topWindow):
		super(Renderer, self).__init__()
		self.topWindow = topWindow

	def render(self, dom):
		self.document = dom
		self.bodyNode = self.document.getElementsByTagName('body')[0]
		try:
			self.title = self.document.getElementsByTagName('title')[0].childNodes[0].nodeValue
		except IndexError, e:
			self.title = self.topWindow.urlbar.get_text()[0]

		self.bodyDisplayNode = HTML.SpecialNode_body(self.bodyNode)
		self.topWindow.titlebar.title.set_text('pylynx -- ' + self.title)
		self.topWindow.widget_list[2] = self.bodyDisplayNode
