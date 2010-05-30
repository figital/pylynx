#!/usr/bin/python
import curses
import scrollpad
from sys import argv

def dummy(charcode):
	return True

def main(stdscr):
	stdscr.refresh()
	if len(argv) == 2:
		arr=stdscr.getmaxyx()
		scrolly = scrollpad.ScrollPad(buffersize=[400, 100], screensize=stdscr.getmaxyx())
		#scrolly.draw("Hello World?")
		scrolly.draw(open(argv[1], 'r').read())
		scrolly.interact(dummy)

curses.wrapper(main)
