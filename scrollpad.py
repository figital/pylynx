import curses
import logging

_logfile = 'scrollpad.log'
logging.basicConfig(filename=_logfile, level=logging.DEBUG)

'''When the pad is resized due to overflow, _resize_margin is the (height, width)
tuple by which the pad will expand. I could just look at the input to determine
this but that's a small bit of work I don't want to do [now].'''
_resize_margin = (0, 10)

'''When polling for input, how long should each iteration block? Zero blocking
time is Just Fucking Stupid in an infinite loop, so don't do that. If I ever
get my head far enough out my ass I'll probably move [most] all input in the
whole app to another thread with full blocking so as to avoid the whole polling
issue, but let's start small, yes?'''
_blocking_time = 100


class ScrollPad(object):

	def __init__(self, buffersize, screensize, position=[0,0]):
		super(ScrollPad, self).__init__()
		self.pad = curses.newpad(buffersize[0], buffersize[1])
		self.pad.scrollok(1)
		self.pad.idlok(1)
		self.pad.keypad(1)
		self.offset = [0, 0]
		self.size = [screensize[0]-1, screensize[1]-1]	
		self.position = position

	def draw(self, data):
		cursor_pos = self.pad.getyx()
		self.pad.erase()
		self.pad.move(0, 0)

		self.write(data)

		self.pad.move(cursor_pos[0], cursor_pos[1])
		self.refresh()

	def write(self, string):
		for char in string:
			self.pad.addch(ord(char))
			if self.pad.getyx()[1] == self.pad.getmaxyx()[1]:
				self.pad.move(self.getyx()[0]+1, 0)
			if self.pad.getyx()[0] == self.pad.getmaxyx()[0]:
				self.resize(self.pad.getmaxyx()[0] + _resize_margin[0], self.pad.getmaxyx()[1] + _resize_margin[1])
				break


	def addTag(self, tag):
		self.tagAttrOn(tag)

		try:
			logging.debug(repr(tag.contents))
			for child in tag.contents:
				self.addTag(child)
				self.tagAttrOn(tag) # In case it decided to remove an attribute

		except TypeError, e: # No tag.contents
			self.write(tag.string)
		except AttributeError, e: # No tag.contents
			self.write(tag.string)

		self.tagAttrOff(tag)

	def tagAttrOn(self, tag):
		try:
			if tag.name in ('b', 'strong'):
				self.pad.attron(curses.A_BOLD)
			if tag.name in ('a', 'u'):
				self.pad.attron(curses.A_UNDERLINE)
		except AttributeError, e: # Text node
			pass

	def tagAttrOff(self, tag):
		try:
			if tag.name in ('b', 'strong'):
				self.pad.attroff(curses.A_BOLD)
			if tag.name in ('a', 'u'):
				self.pad.attroff(curses.A_UNDERLINE)
		except AttributeError, e: # Text Node
			pass

	def refresh(self):
			self.pad.refresh(self.offset[0], self.offset[1], self.position[0], self.position[1], self.size[0], self.size[1])


	'''callback is a callable taking a charcode argument which returns a boolean
	instructing [False] the loop to continue or [True] the loop to exit. This
	argument will be called for any input which ScrollPad cannot handle.'''
	def interact(self, callback):
		self.pad.timeout(_blocking_time)
		curses.noecho()
		while True:
			logging.debug(repr(curses.getsyx()))
			charcode = self.pad.getch()
			if charcode == -1:
				continue

			elif charcode in (curses.KEY_UP, ord('k')):
				if self.pad.getyx()[0] > 0:
					self.pad.move(self.pad.getyx()[0]-1, self.pad.getyx()[1])
					self.refresh()

			elif charcode in(curses.KEY_DOWN, ord('j')):
				if self.pad.getyx()[0] < self.pad.getmaxyx()[0]:
					self.pad.move(self.pad.getyx()[0]+1, self.pad.getyx()[1])
					self.refresh()

			elif charcode in(curses.KEY_LEFT, ord('h')):
				if self.pad.getyx()[1] > 0:
					self.pad.move(self.pad.getyx()[0], self.pad.getyx()[1]-1)
					self.refresh()

			elif charcode in (curses.KEY_RIGHT, ord('l')):
				if self.pad.getyx()[1] < self.pad.getmaxyx()[1]:
					self.pad.move(self.pad.getyx()[0], self.pad.getyx()[1]+1)
					self.refresh()

			elif charcode == curses.KEY_NPAGE:
				for i in xrange(self.size[0]):
					if self.offset[0] + self.size[0] + 1 >= self.pad.getmaxyx()[0]:
						break
					self.offset[0] += 1
				self.refresh()

			elif charcode == curses.KEY_PPAGE:
				if self.offset[0] - self.size[0] <= 0:
					self.offset[0] = 0
				else:
					for i in xrange(self.size[0]):
						self.offset[0] -= 1
				self.refresh()




			elif callback(charcode):
				break











