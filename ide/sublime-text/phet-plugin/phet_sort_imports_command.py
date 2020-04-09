import sublime, sublime_plugin

from . import phet

class PhetSortImportsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    phet.run_sort_imports(self, self.view, edit)
