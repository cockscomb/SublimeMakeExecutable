import sublime, sublime_plugin
import os, stat

s = sublime.load_settings('MakeExecutable.sublime-settings')

class Pref:
    def load(self):
        Pref.enabled_extensions = [x.lower() for x in s.get('enabled_extensions', [])]

Pref = Pref()
Pref.load();
s.add_on_change('reload', lambda:Pref.load())

class MakeExecutable(sublime_plugin.EventListener):

    def on_post_save(self, view):

        # get filename
        filename = view.file_name()

        # get file extension, make extension lower case, strip the .
        ext = os.path.splitext(filename)[1].lower()[1:]

        # if file extension is in list of enabled extensions
        if ext in Pref.enabled_extensions:

            # if file starts with shebang
            shebang = view.substr(sublime.Region(0, 2))
            if shebang == '#!':

                # make file executable
                mode = os.stat(filename)[stat.ST_MODE]
                mode = mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
                os.chmod(filename, mode)

                # output status of command
                self.name = os.path.split(filename)[1]
                sublime.set_timeout(
                    lambda: sublime.status_message(
                        "'{0}' is now executable.".format(self.name)
                    ),
                    4000)