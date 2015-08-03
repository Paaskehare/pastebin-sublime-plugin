import sublime, sublime_plugin

import string, random, os.path

# Python 2
try:
    import urllib2

# Python 3
except ImportError:
    import urllib.request as urllib2

HOSTNAME = 'https://upl.io'
POST_FILE_FIELD = 'file'

class FilePart:

    CONTENT_TYPE = 'application/text-plain;charset=utf-8;'
    CONTENT_TRANSFER_ENCODING = 'utf-8'

    def __init__(self, name, filename, body, boundary):

        self.name = name
        self.filename = filename
        self.body = body
        self.boundary = boundary

        self.headers = {
            'Content-Type':        self.CONTENT_TYPE,
            'Content-Disposition': 'form-data; name="{0}"; filename="{1}"'.format(
                    self.name, self.filename
                ),
            'Content-Transfer-Encoding': self.CONTENT_TRANSFER_ENCODING,
        }

    def get(self):
        lines = []
        lines.append('--' + self.boundary)

        for key, val in self.headers.items():
            lines.append('{0}: {1}'.format(key, val))

        lines.append('')
        lines.append(self.body)
        lines.append('--{0}--'.format(self.boundary))
        lines.append('')

        return lines

class FileForm:

    NEWLINE = '\r\n'

    # Generate a random boundary
    def _gen_boundary(self):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for x in range(40))

    def __init__(self):
        self.boundary = self._gen_boundary()
        self._file = None

    def file(self, filename, content):
        self._file = FilePart(POST_FILE_FIELD, filename, content, self.boundary)

    def get(self):
        # file returns an array
        content = self._file.get()

        content_type = 'multipart/form-data; boundary=' + self.boundary

        return content_type, self.NEWLINE.join(content).encode(FilePart.CONTENT_TRANSFER_ENCODING)

class PastebinCommand(sublime_plugin.TextCommand):

    def _get_file_name(self):
        name = "untitled"
        try:
            name = os.path.split(self.view.file_name())[-1]
        except AttributeError:
            pass
        except TypeError:
            pass
        return name

    def run(self, edit):

        # init an empty unicode string
        content = u''

        # loop over the selections in the view:
        for region in self.view.sel():

            if not region.empty():
                # be sure to insert a newline if we have multiple selections
                if content:
                    content += FileForm.NEWLINE
                content += self.view.substr(region)

        # if we havent gotten data from selected text,
        # we assume the entire file should be pasted:
        if not content:
            content += self.view.substr(sublime.Region(0, self.view.size()))

        filename = self._get_file_name()

        form = FileForm()

        # insert the "fake" file
        form.file(filename = filename, content = content)

        content_type, body = form.get()

        request = urllib2.Request(url=HOSTNAME, headers={'Content-Type': content_type}, data=body)
        reply = urllib2.urlopen(request).read().decode(FilePart.CONTENT_TRANSFER_ENCODING)

        sublime.set_clipboard(reply)
        sublime.status_message("Paste: " + reply)
