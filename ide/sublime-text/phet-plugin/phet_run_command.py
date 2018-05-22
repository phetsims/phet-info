import os
import sublime
import sublime_plugin
import subprocess

#  class generally copied from http://mreq.eu/2014/10/running-custom-command/
class PhetRunCommand(sublime_plugin.WindowCommand):
  def run(self, cmd):

    # Save the file first so you don't look working copy changes
    window = self.window
    view = window.active_view()
    view.run_command('save')

    if "$file_name" in cmd:
      view = self.window.active_view()
      cmd = cmd.replace("$file_name",view.file_name())
    if "$file_dir" in cmd:
      view = self.window.active_view()
      cmd = cmd.replace("$file_dir",os.path.split(view.file_name())[0])

    if "$selectedText" in cmd:

      # code section copied from https://stackoverflow.com/questions/19707727/api-how-to-get-selected-text-from-object-sublime-selection
      sel = view.sel()
      region1 = sel[0]
      selectionText = view.substr(region1)

      cmd = cmd.replace("$selectedText", selectionText)


    print ('Running custom command:', cmd)

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.path.split(view.file_name())[0])
    while proc.poll() is None:
      line = proc.stdout.readline()
      if( len(line) > 0):
        print (line.decode("utf-8")) # give output from your execution/your own message
    self.commandResult = proc.wait() # catch return code