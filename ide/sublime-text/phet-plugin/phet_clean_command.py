import sublime, sublime_plugin

from . import phet

class PhetCleanCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    phet.run_clean(self, self.view, edit)
