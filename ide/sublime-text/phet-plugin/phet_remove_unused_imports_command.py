import sublime, sublime_plugin

from . import phet

class PhetRemoveUnusedImportsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    phet.run_remove_unused_imports(self, self.view, edit)
