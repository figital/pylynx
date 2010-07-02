import html

class Renderer(object):
	def __init__(self, topWindow):
		super(Renderer, self).__init__()
		self.topWindow = topWindow

	def render(self, dom):
		self.document = dom
		self.bodyNode = self.document.getElementsByTagName('body')[0]
		self.bodyDisplayNode = html.SpecialNode_body(self.bodyNode)
		self.topWindow.widget_list[2] = self.bodyDisplayNode
		#raise Exception(repr( [x for x in self.bodyDisplayNode.widget_list[2].render((80,)).content()] ))
		#self.topWindow.contentArea._invalidate()
		#self.topWindow._invalidate()
