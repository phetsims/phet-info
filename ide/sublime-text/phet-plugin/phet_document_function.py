import sublime, sublime_plugin

from . import phet

class PhetDocumentFunction(sublime_plugin.TextCommand):
  def run(self, edit):
    phet.run_document_function(self, self.view, edit)
