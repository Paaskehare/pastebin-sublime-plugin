Metabox Sublime Plugin
======================

This is a simple plugin for Sublime Text 2 to allow for easily pasting code to a pastebin

It takes the current selection in a file, uploads it to [Metabox](http://dl.gs), and returns the URL to the clipboard.


Installation
------------
###Linux
 move **metabox.py** to `~/.config/sublime-text-2/Packages/User/`
  
  Bind a key to upload, like:
    `{ "keys": ["super+m"], "command": "metabox" }`

Select some text, and hit `Super + m` and afterwards `ctrl + v` - and you're good to go!

*Good luck!*
