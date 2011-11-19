# encoding: utf-8
import urllib2
import sublime, sublime_plugin

HOSTNAME = 'http://i.ole.im'
POST_FILE_FIELD = 'file'

class Part:

    BOUNDARY = '----------AaB03x'
    NEWLINE = '\r\n'

    CONTENT_TYPE = 'Content-Type'
    CONTENT_DISPOSITION = 'Content-Disposition'
    CONTENT_TRANSFER_ENCODING = 'Content-Transfer-Encoding'

    DEFAULT_CONTENT_TYPE = 'application/text-plain;charset=utf-8;'
    DEFAULT_ENCODING = 'utf-8'

    def __init__(self, name, filename, body, headers):
        self._headers = headers.copy()
        self._name = name
        self._filename = filename
        self._body = body

        self._headers[Part.CONTENT_DISPOSITION] = \
            ('form-data; name="%s"; filename="%s"' %
            (self._name, self._filename))
        self._headers[Part.CONTENT_TRANSFER_ENCODING] = \
            (Part.DEFAULT_ENCODING)

    def get(self):
        lines = []
        lines.append('--' + Part.BOUNDARY)
        for (key, val) in self._headers.items():
            lines.append('%s: %s' % (key, val))
        lines.append('')
        lines.append(self._body)
        return lines

class Multipart:

    def __init__(self):
        self.parts = []

    def file(self, name, filename, value, headers={'Content-Type': Part.DEFAULT_CONTENT_TYPE}):
        self.parts.append(Part(name, filename, value, headers))

    def get(self):
        all = []
        for part in self.parts:
            all += part.get()
        all.append('--' + Part.BOUNDARY + '--')
        all.append('')
        content_type = 'multipart/form-data; boundary=%s' % Part.BOUNDARY
        return content_type, Part.NEWLINE.join(all).encode(Part.DEFAULT_ENCODING)

class PastebinCommand(sublime_plugin.TextCommand):

    def get_file_name(self):
        name = "untitled"
        try: name = self.view.file_name().split('/')[-1]
        except AttributeError: pass
        return name

    def run(self, view):
    	global HOSTNAME, POST_FILE_FIELD

        for region in self.view.sel():

            if not region.empty():
                content = self.view.substr(region)
            else:
                content = self.view.substr(sublime.Region(0, self.view.size()))
            form = Multipart()
            file_name = self.get_file_name()
            form.file(POST_FILE_FIELD, file_name, content)
            content_type, body = form.get()

            print(body)
            request = urllib2.Request(url=HOSTNAME, headers={'Content-Type': content_type}, data=body)
            reply = urllib2.urlopen(request).read()
            sublime.set_clipboard(reply)
            sublime.status_message("Paste: " + reply)
