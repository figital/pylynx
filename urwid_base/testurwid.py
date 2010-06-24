#!/usr/bin/python
import urwid
import TopWindow

palette = [('highlighted', 'default,standout', 'default', 'default'),]

root = TopWindow.TopWindow()
fill = urwid.Filler(root, 'top')
loop = urwid.MainLoop(fill, palette)
loop.run()


