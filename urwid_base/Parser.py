import BeautifulSoup
# These are always block mode unless CSS or malformed HTML dictates otherwise.
blockTags = ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'ol', 'ul', 'li', 'hr', 'pre',)
# These are always inline, except perhaps the list tags.
inlineTags = ('a', 'em', 'strong', 'i', 'b', 'u', 'span', 'br', 'img', 'font', 'tt', 'code', 'samp', 'kdb', 'del', 'ins', 'strike', 'q',)
# Never render anything below these.
noRenderTags = ('hr', 'br', 'img', 'script')

class DomNode(object):
	def __init__(self, soup_node):
		super(DomNode, self).__init__()
		self.soup_node = soup_node
		self.soup_node.dom_node = self

def getEffectiveLayout(soupTag):
	if type(soupTag) != type(soupTag.parent):
		return ''
	if hasAttr(soupTag, 'effectiveLayout'):
		return soupTag.effectiveLayout
	if soupTag.name in blockTags:
		return 'block'
	if soupTag.name in inlineTags:
		return 'inline'
	throw Exception("Invalid tag type")

def setEffectiveLayout(soupTag, layout):
	effectiveLayout = getEffectiveLayout(soupTag)
	if effectiveLayout == layout:
		return
	else:
		soupTag.effectiveLayout = layout


class DisplayDom(object): # Transform HTML DOM into tree of widgets, not necessarily same structure
	def __init__(self, source):
		super(DisplayDom, self).__init__()
		self.source = source
		self.soup = BeautifulSoup.BeautifulSoup(self.source)
		self.initializeTags()

	def initializeTags(self):
		currentNode = self.soup.html
		while currentNode.next is not None:
			DomNode(currentNode)
			currentNode = currentNode.next

	def prepareTag(soupTag): # Fix stupid shit happening in parse tree.
		assert soupTag.name not in blockTags or soupTag.name not in inlineTags
		if !hasattr(soupTag, 'string') and type(soupTag) == type(soupTag.parent): # Contains tags, not just text.
			if getEffectiveLayout(soupTag) == 'inline':
				for child in soupTag.contents:
					if getEffectiveLayout(child) == 'block':
						setEffectiveLayout(child, 'inline') # Force blocks within inlines to render inline for great justice.


