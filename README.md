Metabox Sublime Plugin
======================

This is a simple plugin for [Sublime Text 2](http://www.sublimetext.com/2) to allow for easily pasting code to a pastebin

It takes the current selection in a file, uploads it to [Metabox](http://dl.gs), and returns the URL to the clipboard.


Installation
------------

* copy **metabox.py** to Your `Packages/User` directory on e.g. linux it will most likely be in `~/.config/sublime-text-2/Packages/User/`


* Bind a key to upload, like:
  `{ "keys": ["super+m"], "command": "metabox" }`

Select some text, and hit `Super + m` and afterwards `ctrl + v` - and you're good to go!

*Good luck!*
