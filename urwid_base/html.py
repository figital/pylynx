import urwid

"""
Throughout this module I will draw a distinction between the display tree and the DOM tree.

The DOM tree is handled by the xml.dom module and strictly [as interpreted by BeautifulSoup]
represents the structure defined in the HTML source.

The display tree, on the other hand, represents the way each node is presented to urwid and
rendered. For example, I *cannot* render block element within an inline element, even though
this happens in real-world [shitty] HTML all the time. To remedy this, I render the block
element up one or more element in the tree. As far as the display tree is concerned,
"<inline>dogshit<block>bullshit</block>catshit</inline>" is reprented as
"<inline>dogshit</inline><inline>catshit</inline><block>bullshit</block>", which would then
be displayed as
<pile>
	<row><inline>dogshit</inline><inline>catshit</inline></row>
	<row><block>bullshit</block></row>
</pile>
Provided that the amount of content inside the block element is small, this should not
radically distort the layout, although it will be out of order. This behavior may be
amended in later versions, when it is seen how large the impact will be on everyday use.

This does not, however, affect the DOM tree.
"""


class DisplayNode:
	domNode = None
	displayParent = None

	def init(self, domNode):
		domNode.displayNode = self
		self.domNode = domNode
		self.prepareNodes() # Initialize all child elements.
		self.prepareTree() # Assemble display tree.

	def prepareNodes(self):
		"""
		Visit each child in the DOM tree, initializing a node object for each.
		Every node object will run through its constructor as well, meaning
		that the entire tree will be initialized after calling this method on
		the root display node, usually <body.>
		"""
		for childNode in self.domNode.childNodes:
			try:
				classFinder[childNode.nodeName](childNode)
			except KeyError, e:
				continue # Unsupported node.

	def prepareTree(self):
		"""	Assemble nodes into correct hierarchy, taking into account any special cases."""
		for childNode in self.domNode.childNodes:
			try:
				childNode.displayNode.prepareTree()
			except AttributeError, e:
				pass # Special non-display node

		self.requestAdoption()

	def requestAdoption(self):
		"""Request adoption from DOM parent."""
		self.domNode.parentNode.displayNode.adopt(self)

	def adopt(self, childNode):
		"""
		Add childNode to displayChildren if it is reasonable to do so.
		Alternatives are to toss the node up a level to see if the DOM
		grandparent [ad nauseum] can handle it, or just drop it on its
		fucking head if it's one of those bastard crossbreed <script>
		tags or similar. There will be no mandatory child support, dammit!
		"""
		pass



class BlockNode(DisplayNode, urwid.Pile):
	"""
	Every BlockNode will have a Pile-like interface.
	In the event of an empty block node, the pile will have a single Text node
	containing "" as its only displayChild.
	"""

	displayMode = 'block'
	widget_list = []

	def __init__(self, domNode):
		if self.widget_list == []:
			self.widget_list.append(urwid.Text(''))
		super(BlockNode, self).__init__(self.widget_list)
		self.init(domNode)

	def adopt(self, childNode):
		if childNode in self.widget_list:
			return
		if childNode.displayMode not in ('block', 'inline'): # Probably a special node, toss it into the fire.
			return
		self.widget_list.append(childNode)
		childNode.displayParent = self


class InlineNode(DisplayNode, urwid.Text):
	"""Every InlineNode *must* implement a get_text() method similar to urwid.Text.get_text()."""

	displayMode = 'inline'

	def __init__(self, domNode):
		self.init(domNode)
		super(InlineNode, self).__init__('') # Empty for now.

	def adopt(self, childNode):
		if childNode in self.displayChildren:
			return
		if childNode.displayMode == 'inline':
			self.displayChildren.append(childNode)
			childNode.displayParent = self
		elif childNode.displayMode == 'block': # Fucking Dreamweaver Whores.
			self.domNode.parentNode.displayNode.adopt(childNode)
		else:
			pass # Likely a special node. It's still referenced from the DOM.

	def get_text(self):
		out_text = ''
		out_attributes = []
		for w in self.displayChildren:
			text, attributes = w.get_text()
			out_text += text
			for attr in attributes:
				out_attributes.append(attr)
		return out_text, out_attributes

	def render(self, size, focus=False):
		self.set_text(self.get_text())
		return super(InlineDisplay, self).render(size, focus)


# Block Nodes
class SpecialNode_body(BlockNode):
	def requestAdoption(self):
		pass # This is the root of the display, so there's nobody to ask!

class Node_p(BlockNode):
	pass # TODO: Add indention

class Node_h1(BlockNode):
	pass
class Node_h2(BlockNode):
	pass
class Node_h3(BlockNode):
	pass
class Node_h4(BlockNode):
	pass
class Node_h5(BlockNode):
	pass
class Node_h6(BlockNode):
	pass
class Node_div(BlockNode):
	pass

class Node_ol(BlockNode):
	pass
class Node_ul(BlockNode):
	pass
class Node_li(BlockNode):
	pass

class Node_hr(BlockNode):
	def __init__(self, domNode):
		super(Node_hr, self).__init__(domNode)
		self.widget_list.append(urwid.Divider('-'))
		self.widget_list[0:len(self.widget_list)-2] = []

class Node_pre(BlockNode):
	pass # Is this even possible after BeautifulSoup and xml.dom? Research!


# Inline Nodes
class SpecialNode_text(urwid.Text):
	displayMode = 'inline'
	def __init__(self, textNode):
		assert textNode.nodeName == '#text'
		if textNode.nodeValue == "\n":
			return
		self.domNode = textNode
		textNode.displayNode = self
		self.domNode.parentNode.displayNode.adopt(self)
		super(SpecialNode_text, self).__init__(textNode.nodeValue)
#		if textNode.nodeValue != "\n":
#			raise Exception(self.displayParent)

class Node_a(InlineNode):
	pass

class Node_i(InlineNode):
	pass

class Node_b(InlineNode):
	pass

class Node_u(InlineNode):
	pass

class Node_span(InlineNode):
	pass

class Node_br(urwid.Text):
	def __init__(self, domNode):
		assert domNode.nodeName == 'br'
		self.domNode = domNode
		domNode.displayNode = self
		super(Node_br, self).__init__("\n")

class Node_font(InlineNode):
	pass

class Node_tt(InlineNode):
	pass

class Node_code(InlineNode):
	pass

class Node_samp(InlineNode):
	pass

class Node_kbd(InlineNode):
	pass

class Node_ins(InlineNode):
	pass

class Node_del(InlineNode):
	pass

class Node_strike(InlineNode):
	pass

class Node_q(InlineNode):
	pass

# Special non-display Nodes
class SpecialNode_script:
	pass


# Aliases
Node_em = Node_i
Node_strong = Node_b


classFinder = {
		'p': Node_p,
		'h1': Node_h1,
		'h2': Node_h2,
		'h3': Node_h3,
		'h4': Node_h4,
		'h5': Node_h5,
		'h6': Node_h6,
		'div': Node_div,
		'ol': Node_ol,
		'ul': Node_ul,
		'li': Node_li,
		'hr': Node_hr,
		'pre': Node_pre,
		'a': Node_a,
		'em': Node_em,
		'strong': Node_strong,
		'i': Node_i,
		'b': Node_b,
		'u': Node_u,
		'span': Node_span,
		'br': Node_br,
		#'img': Node_img,
		'font': Node_font,
		'tt': Node_tt,
		'code': Node_code,
		'samp': Node_samp,
		'kbd': Node_kbd,
		'ins': Node_ins,
		'del': Node_del,
		'strike': Node_strike,
		'q': Node_q,
		'#text': SpecialNode_text,
		'script': SpecialNode_script,
		'body': SpecialNode_body,
}
