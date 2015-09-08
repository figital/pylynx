# More than you ever wanted to know about pylynx #

## Why? (The reasons for pylynx) ##
Why would anyone want another console web browser? Aren't links et al bad enough as it is?

Yes, and that's the problem. Text browsers are boring and painful because they're outdated and lack support for any web technology debuted after at least 1980. Also people like to see their ~~hardcore porn~~ pictures of loved ones, but that's another issue.

## What? (The expectations of pylynx) ##
Pylynx has one goal: To bring the text browsing experience as close as possible to the level of graphical web browsers.

### What's so different about pylynx compared to (for example) lynx? ###
Similarities:
  * They're all rendered in text.
  * They were all written by humans in a programming language.
  * They were all designed to view HTML.

Differences:
  * Pylynx is written in Python, not C.
  * Pylynx is written in Urwid, not Curses.
  * Pylynx will (maybe) use caret browsing as the main interface. If you want tabular browsing, however, you can still use the tab key.
  * Pylynx does a good job with messy HTML, dammit! This is a consequence of using BeautifulSoup for SGML parsing.
  * Pylynx has a single notification area. Little boxes and shit won't be constantly popping up everywhere.
    * Pylynx will have a real URL bar, so there will be none of this pussyfooted "here's a text box, now tell me **exactly** where you want to go" business.
    * Pylynx tells you **exactly** what it's doing. Always. Are we waiting for user input, resolving, downloading, parsing, DOMifying, rendering, or doing nothing? You're going to know, and it won't annoy the hell out you, either.
  * Pylynx makes console web browsing cool again.
  * Pylynx will dramatically improve your sex life.
  * Pylynx will also do much, much, more.

## Huh? (The politics of pylynx) ##
All code distributed in a "release" of pylynx is licensed under the [WTFPL.](http://sam.zoy.org/wtfpl)

All code hosted under the pylynx repository is free software as defined by the [FSF.](http://fsf.org/)

The pylynx source code is intended for mature audiences only. You may find graphic and disturbing comments and docstrings within. You view the source at great personal risk, as I shall not be held liable for offending you or others.

This is intended to be a ridiculously ambitious project.
I am well aware of it, so either shut up or lend a keyboard.