import sublime, sublime_plugin

from . import phet

class PhetImportCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    phet.run_import(self, self.view, edit)
