#!/usr/bin/python
import curses
from BeautifulSoup import BeautifulSoup
import scrollpad
from sys import argv

#file = 'testpage.htm'
#fh = open(file)
#dom = BeautifulSoup(fh)

def dummy(charcode):
	return True
def main(stdscr):
	stdscr.refresh()
	if len(argv) == 2:
		scrolly = scrollpad.ScrollPad(buffersize=[500, stdscr.getmaxyx()[1]], screensize=stdscr.getmaxyx())

		dom = BeautifulSoup(open(argv[1]))
		for tag in dom:
			scrolly.addTag(tag)

		#scrolly.draw(open(argv[1], 'r').read())
		scrolly.interact(dummy)

curses.wrapper(main)
