#!/usr/bin/python
import curses
import curses.textpad
import urllib2

class Pad(object):
	def __init__(self, height, width):
		super(Pad, self).__init__()
		self.pad = curses.newpad(height, width)
		self.setParams(0, 0, 0, 0, 0, 0)
	def refresh(self):
		self.pad.refresh(self.y_offset, self.x_offset, self.top, self.left, self.height, self.width)
	def setParams(self, y=None, x=None, t=None, l=None, h=None, w=None):
		if y is not None:
			self.y_offset = y
		if x is not None:
			self.x_offset = x
		if t is not None:
			self.top = t
		if l is not None:
			self.left = l
		if h is not None:
			self.height = h
		if w is not None:
			self.width = w

class NewUrl(Exception):
	def __init__(self, newurl):
		self.url = newurl
	def __str__(self):
		return "The browser was issued a request to load but did not respond.\nLocation: %s" % (self.url,)

class Urlbar(object):
	window = None	# Curses window
	location = ''	# Current location

	def __init__(self, location='about:pynks'):
		super(Urlbar, self).__init__()
		self.window = curses.newwin(1, 80, 1, 0)
		self.location = location
		self.redraw()

	def input(self):
		self.redraw()
		pad = curses.textpad.Textbox(self.window)
		self.window.move(0, 0)
		input_url = pad.edit()

		if input_url != self.location:
			self.location = input_url
			self.redraw()
			self.issueNewUrl()
		else:
			self.redraw()

	def redraw(self):
		self.window.clear()
		self.window.addstr(0, 0, self.location)
		self.window.refresh()

	def issueNewUrl(self):
		raise NewUrl(self.location)

class Browser(object):
	pad = None
	urlbar = None

	def __init__(self, location):
		self.pad = Pad(200, 200)

		self.urlbar = Urlbar(location)
		self.navigate(self.urlbar.location)

	def navigate(self, location=None):
		if location is None:
			try:
				self.urlbar.input()
			except NewUrl, m:
				location = m.url
			else:
				location = self.urlbar.location

		if location.lstrip().startswith('http:') is True:
			response = urllib2.urlopen(location)
			for shit in response.read():
				self.pad.pad.addstr(shit)
			self.pad.setParams(0, 0, 2, 0, 26, 80)
			self.pad.refresh()

def main(window):
	#curses.curs_set(2)
	browser = Browser('http://www.google.com')
	#browser.pad.pad.nodelay(1)
	browser.pad.pad.keypad(1)
	while True:
		key = browser.pad.pad.getch()
		(y, x) = browser.pad.pad.getyx()
		if key == 113:
			break
		if key == curses.KEY_DOWN:
			browser.pad.y_offset += 1
			browser.pad.refresh()
		if key == curses.KEY_UP:
			browser.pad.y_offset -= 1
			browser.pad.refresh()
		if key == curses.KEY_LEFT:
			browser.pad.x_offset -= 1
			browser.pad.refresh()
		if key == curses.KEY_RIGHT:
			browser.pad.x_offset += 1
			browser.pad.refresh()


if __name__ == '__main__':
	curses.wrapper(main)
