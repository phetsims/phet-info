# Copyright 2020, University of Colorado Boulder
#
# @author Jonathan Olson <jonathan.olson@colorado.edu>

import sublime, sublime_plugin, os, re, subprocess, webbrowser, json, threading

from functools import reduce

### Summary of sublime plugin documentation and API

# location: a tuple of (str, str, (int, int)) that contains information about a location of a symbol. The first string
#   is the absolute file path, the second is the file path relative to the project, the third element is a two-element
#   tuple of the row and column.
# point: an int that represents the offset from the beginning of the editor buffer. The View methods text_point() and
#   rowcol() allow converting to and from this format.
# value: any of the Python data types bool, int, float, str, list or dict.
# dip: a float that represents a device-independent pixel.
# vector: a tuple of (dip, dip) representing x and y coordinates.
# CommandInputHandler: a subclass of either TextInputHandler or ListInputHandler.

# Selection - set of Regions, not overlapping - can be modified or queried
# Region - Region(a, b), a==b valid, they are int

# Window
# window.new_file() => View
# window.open_file(file_name, <flags>) => View
# window.folders() => [str] -------- hmmm?
# window.project_file_name() => str
# window.project_data() => dict ---- same format as .sublime-project
# window.show_quick_panel(items, on_done, <flags>, <selected_index>, <on_highlighted>) None
#   Shows a quick panel, to select an item in a list. on_done will be called once, with the index of the selected item.
#     If the quick panel was cancelled, on_done will be called with an argument of -1.
#   items may be a list of strings, or a list of string lists. In the latter case, each entry in the quick panel will show multiple rows.
#   flags is a bitwise OR of sublime.MONOSPACE_FONT and sublime.KEEP_OPEN_ON_FOCUS_LOST
#   on_highlighted, if given, will be called every time the highlighted item in the quick panel is changed.

# textCommand.is_enabled/is_visible/description

# View
# view.file_name()
# view.name()
# view.window() -- Window
# view.is_loading() - Returns True if the buffer is still loading from disk, and not ready for use.
# view.is_dirty() - Returns True if there are any unsaved modifications to the buffer.
# view.is_read_only()

# view.substr(region) => str
# view.insert(edit, point, string)
# view.erase(edit, region)
# view.replace(edit, region, string)
# view.sel() => Selection
# view.find(pattern, start_point, <flags>) => Region
# view.find_all(pattern, <flags>, <format>, <extractions>) => [Region]
# view.rowcol(point) => (int,int)
# view.text_point(row, col) => int
# view.show(location, <show_surrounds>)

# view.show_popup_menu(items, on_done, <flags>)

# lambda x: x
# (lambda x, y: x + y)
# map(func,iterable)

# test on Windows

# [func for func in dir(sublime.View) if callable(getattr(sublime.View, func))]
#
# ['__bool__', '__class__', '__delattr__', '__dir__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__',
# '__init__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
# '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'add_phantom', 'add_regions', 'assign_syntax',
# 'begin_edit', 'buffer_id', 'change_count', 'classify', 'close', 'command_history', 'em_width', 'encoding', 'end_edit',
# 'erase', 'erase_phantom_by_id', 'erase_phantoms', 'erase_regions', 'erase_status', 'expand_by_class',
# 'extract_completions', 'extract_scope', 'extract_tokens_with_scopes', 'file_name', 'find', 'find_all',
# 'find_all_results', 'find_all_results_with_text', 'find_by_class', 'find_by_selector', 'fold', 'folded_regions',
# 'full_line', 'get_regions', 'get_status', 'get_symbols', 'has_non_empty_selection_region', 'hide_popup', 'id',
# 'indentation_level', 'indented_region', 'indexed_references', 'indexed_symbols', 'insert', 'is_auto_complete_visible',
# 'is_dirty', 'is_folded', 'is_in_edit', 'is_loading', 'is_popup_visible', 'is_primary', 'is_read_only', 'is_scratch',
# 'is_valid', 'layout_extent', 'layout_to_text', 'layout_to_window', 'line', 'line_endings', 'line_height', 'lines',
# 'match_selector', 'meta_info', 'name', 'overwrite_status', 'query_phantom', 'query_phantoms', 'replace',
# 'reset_reference_document', 'retarget', 'rowcol', 'run_command', 'scope_name', 'score_selector', 'sel',
# 'set_encoding', 'set_line_endings', 'set_name', 'set_overwrite_status', 'set_read_only', 'set_reference_document',
# 'set_scratch', 'set_status', 'set_syntax_file', 'set_viewport_position', 'settings', 'show', 'show_at_center',
# 'show_popup', 'show_popup_menu', 'size', 'split_by_newlines', 'style', 'style_for_scope', 'substr', 'symbols',
# 'text_point', 'text_to_layout', 'text_to_window', 'unfold', 'update_popup', 'viewport_extent', 'viewport_position',
# 'visible_region', 'window', 'window_to_layout', 'window_to_text', 'word']

# [func for func in dir(sublime.Window) if callable(getattr(sublime.Window, func))]
#
# ['__bool__', '__class__', '__delattr__', '__dir__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__',
# '__init__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
# '__sizeof__', '__str__', '__subclasshook__', 'active_group', 'active_panel', 'active_sheet', 'active_sheet_in_group',
# 'active_view', 'active_view_in_group', 'create_output_panel', 'destroy_output_panel', 'extract_variables',
# 'find_open_file', 'find_output_panel', 'focus_group', 'focus_sheet', 'focus_view', 'folders', 'get_layout',
# 'get_output_panel', 'get_sheet_index', 'get_tabs_visible', 'get_view_index', 'hwnd', 'id', 'is_menu_visible',
# 'is_minimap_visible', 'is_sidebar_visible', 'is_status_bar_visible', 'is_valid', 'layout',
# 'lookup_references_in_index', 'lookup_references_in_open_files', 'lookup_symbol_in_index',
# 'lookup_symbol_in_open_files', 'new_file', 'num_groups', 'open_file', 'panels', 'project_data', 'project_file_name',
# 'run_command', 'set_layout', 'set_menu_visible', 'set_minimap_visible', 'set_project_data', 'set_sheet_index',
# 'set_sidebar_visible', 'set_status_bar_visible', 'set_tabs_visible', 'set_view_index', 'settings', 'sheets',
# 'sheets_in_group', 'show_input_panel', 'show_quick_panel', 'status_message', 'template_settings',
# 'transient_sheet_in_group', 'transient_view_in_group', 'views', 'views_in_group']

# >>> [func for func in dir(sublime) if callable(getattr(sublime, func))]
# ['Edit', 'Html', 'Phantom', 'PhantomSet', 'Region', 'Selection', 'Settings', 'Sheet', 'View', 'Window', '_LogWriter',
# 'active_window', 'arch', 'cache_path', 'channel', 'decode_value', 'encode_value', 'error_message', 'executable_hash',
# 'executable_path', 'expand_variables', 'find_resources', 'get_clipboard', 'get_macro', 'installed_packages_path',
# 'load_binary_resource', 'load_resource', 'load_settings', 'log_build_systems', 'log_commands', 'log_indexing',
# 'log_input', 'log_result_regex', 'message_dialog', 'ok_cancel_dialog', 'packages_path', 'platform', 'run_command',
# 'save_settings', 'score_selector', 'set_clipboard', 'set_timeout', 'set_timeout_async', 'status_message', 'version',
# 'windows', 'yes_no_cancel_dialog']

# >>> view.extract_tokens_with_scopes( view.sel()[0] )
# [((2648, 2669), 'source.js meta.class.js meta.block.js meta.function.declaration.js entity.name.function.js ')]

# >>> view.extract_completions( 'updateS' )
# ['updateSize', 'updateStepInformation']

# >>> view.indentation_level( view.sel()[0].begin() )
# 2

# view.substr(view.indented_region( view.sel()[0].begin() ))

# >>> view.indexed_references()
# [((798, 803), 'merge'), ((826, 844), 'createFromVertices'), ((856, 876), 'getEllipsoidVertices'), ((937, 954), 'getEllipsoidShape'), ((1007, 1016), 'getVolume'), ((1100, 1106), 'assert'), ((1339, 1349), 'updateSize'), ((1500, 1518), 'updateFromVertices'), ((1541, 1561), 'getEllipsoidVertices'), ((1676, 1693), 'getEllipsoidShape'), ((1764, 1773), 'getVolume'), ((2571, 2581), 'updateSize'), ((2593, 2610), 'getSizeFromRatios'), ((2690, 2716), 'bodyGetStepMatrixTransform'), ((2785, 2788), 'm02'), ((2828, 2831), 'm12'), ((3767, 3781), 'getTranslation'), ((3784, 3793), 'toVector3'), ((3881, 3889), 'minusXYZ'), ((4703, 4726), 'solveQuadraticRootsReal'), ((4738, 4744), 'filter'), ((6232, 6237), 'reset'), ((6250, 6260), 'updateSize'), ((6300, 6305), 'reset'), ((6516, 6523), 'ellipse'), ((6926, 6930), 'push'), ((6950, 6953), 'cos'), ((6981, 6984), 'sin'), ((7329, 7337), 'register')]

# >>> view.indexed_symbols()
# [((625, 634), 'Ellipsoid'), ((747, 758), 'constructor'), ((1463, 1473), 'updateSize'), ((2161, 2178), 'getSizeFromRatios'), ((2523, 2532), 'setRatios'), ((2648, 2669), 'updateStepInformation'), ((3703, 3712), 'intersect'), ((5097, 5113), 'getDisplacedArea'), ((5706, 5724), 'getDisplacedVolume'), ((6200, 6205), 'reset'), ((6462, 6479), 'getEllipsoidShape'), ((6729, 6749), 'getEllipsoidVertices'), ((7216, 7225), 'getVolume')]

number_names = [ 'i', 'j', 'n', 'x', 'y', 'z', 'width', 'height', 'index', 'dt' ]
node_names = [ 'node', 'content', 'listParent' ]

def detect_type(name):
  """Returns a guess on the type of a given name"""
  if name in number_names:
    return 'number'
  if name.endswith('Node') or name in node_names:
    return 'Node'
  if name.endswith('Bounds') or name == 'bounds':
    return 'Bounds2'
  if name.endswith('Point') or name == 'point':
    return 'Vector2'
  if name.endswith('Position') or name == 'position':
    return 'Vector2'
  if name.endswith('Property') or name == 'property':
    return 'Property.<*>'
  if name == 'options':
    return '[Object]'
  if name == 'config':
    return 'Object'
  if name == 'tandem':
    return 'Tandem'
  return '*'

def execute(cmd, cmd_args, cwd, callback):
  def thread_target(cmd, cmd_args, cwd, callback):
    proc = subprocess.Popen([ cmd ] + cmd_args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # proc.wait()
    callback(proc.communicate()[0].decode())
  thread = threading.Thread(target=thread_target, args=(cmd, cmd_args, cwd, callback))
  thread.start()
  # returns immediately after the thread starts
  return thread

def execute_and_show(view, cmd, cmd_args, cwd):
  execute(cmd, cmd_args, cwd, lambda output: show_output(view.window(), output))

def open_link(url):
  webbrowser.get('chrome').open(url, autoraise=True)

def show_output(window, str):
  view = window.create_output_panel('phet')
  view.set_read_only(False)
  view.run_command('append', {"characters": str})
  view.set_read_only(True)
  window.run_command('show_panel', {"panel": "output.phet"})

def get_git_root(view):
  """Returns the absolute path of the git root"""
  return view.window().folders()[0]

def get_relative_to_root(view, path):
  return os.path.relpath(path, get_git_root(view))

def get_repo(view):
  relative_path = get_relative_to_root(view, view.file_name())
  if relative_path[0] == '.':
    return None
  else:
    return relative_path.split('/')[0]

def count_up_directory(path):
  """Returns a count of ../, for determining what the best path is to import"""
  return path.count('../')

def union_regions(regions):
  """Returns the union of sublime.Region instances (using their term 'cover')"""
  return reduce((lambda maybe,region: region if maybe == None else maybe.cover(region)),regions,None)

def is_node_js(view):
  """Whether we're handling things in a node.js or module context"""
  return (not view.find('\n\'use strict\';\n', 0).empty()) and (not view.find(' = require\\( \'', 0).empty())

def load_file(path):
  """Loads a file as a string"""
  with open(path, 'r') as content_file:
    content = content_file.read()
  return content

def get_build_local():
  return json.loads(load_file(os.path.expanduser('~') + '/.phet/build-local.json'))

def get_local_testing_url():
  return get_build_local()[ 'localTestingURL' ]

def handle_windows_relative_path(path):
  return path.replace('\\', '/')

def ensure_dot_slash(path):
  if path[0] != '.':
    return './' + path
  return path

def get_perennial_list(view, name):
  """Ability to load things like active-repos with e.g. get_perennial_list(view, 'active-repos')"""
  return list(filter(lambda line: len(line) > 0, load_file(os.path.join(get_git_root(view),'perennial/data/' + name)).splitlines()))

def get_active_repos(view):
  return get_perennial_list(view, 'active-repos')

def scan_for_relative_js_files(view, js_type_name):
  """Walks our filesystem of repo/js/** looking for something matching ${js_type_name}.js, returned as relative paths"""
  results = []
  current_path = os.path.dirname(view.file_name())
  for repo in get_active_repos(view):
    repo_path = os.path.join(get_git_root(view), repo + '/js')
    for root, dirs, files in os.walk(repo_path):
      for name in files:
        if name == js_type_name + '.js':
          results.append(os.path.join(root, name))
  return list(map(handle_windows_relative_path, map(lambda x: os.path.relpath(x, current_path), results)))

def lookup_import_paths(view, str):
  """Returns a list of relative paths for modules detected to str"""
  current_path = os.path.dirname(view.file_name())
  locations = list(filter(lambda x: (str + '.js') in x[0] and not ('blue-rain' in x[0]), view.window().lookup_symbol_in_index(str)))
  return list(map(handle_windows_relative_path, map(lambda x: os.path.relpath(x[0], current_path), locations)))

def filter_preferred_paths(paths):
  """Returns all paths with the same minimum count of ../ in them"""
  min_directory_up_count = min(map(count_up_directory,paths))
  return filter(lambda path: count_up_directory(path) == min_directory_up_count, paths)

def contains_import(view, str):
  if is_node_js(view):
    return not view.find('const ' + str + ' = require\\(', 0).empty()
  else:
    return not view.find('import ' + str, 0).empty()

def find_import_regions(view):
  if is_node_js(view):
    return view.find_all(r'^const .+ = require\(.+;.*$');
  else:
    return view.find_all(r'^import .+;$');

def sort_imports(view, edit):
  import_regions = find_import_regions(view)
  start_index = union_regions(import_regions).begin()
  import_strings = []

  for region in reversed(import_regions):
    import_strings.append(view.substr(region))
    view.erase(edit,view.full_line(region))

  # It should work to sort imports after the first apostrophe for both node.js and modules
  for import_string in sorted(import_strings,key=(lambda str: str.split('\'')[1]), reverse=True):
    view.insert(edit, start_index, import_string + '\n')

def remove_unused_imports(view, edit):
  """Removes imports where their declared string isn't in the file (not 100% accurate, but helpful)"""
  candidate_regions = find_import_regions(view)
  regions_to_remove = []
  after_imports_point = union_regions(candidate_regions).end()
  for region in candidate_regions:
    import_string = view.substr(region)
    if import_string.startswith('const '):
      name = import_string.split(' ')[1]
    elif import_string.startswith('import '):
      match = re.search('import (.+) from', import_string)
      if match:
        name = match.group(1)
      else:
        break
    else:
      break
    if view.find(name, after_imports_point).empty():
      regions_to_remove.append(region)
  # iterate backward so we don't have to recompute regions here
  for region in reversed(regions_to_remove):
    print('removing: ' + view.substr(region))
    view.erase(edit,view.full_line(region))

def insert_import_in_front(view, edit, import_text):
  start_index = union_regions(find_import_regions(view)).begin()
  view.insert(edit, start_index, import_text + '\n')

def insert_import_and_sort(view, edit, name, path):
  if is_node_js(view):
    # strip off .js suffix
    if path.endswith( '.js' ):
      path = path[:-3]
    insert_import_in_front(view, edit, 'const ' + name + ' = require( \'' + path +'\' );')
  else:
    insert_import_in_front(view, edit, 'import ' + name + ' from \'' + path +'\';')

  sort_imports(view, edit)

def try_import_name(name, view, edit):
  if not contains_import(view, name):
    # scan for symbols in a fast way (with known files in the Sublime index)
    paths = lookup_import_paths(view, name)

    # fall back to scanning all JS files we have, use their names
    if not paths:
      paths = scan_for_relative_js_files(view, name)

    paths = list(map(ensure_dot_slash, paths))

    # if we're in node.js mode, we want to be able to import built-ins or top-level things like 'fs', which probably
    # will not be found
    if is_node_js(view) and not paths:
      paths = [name + '.js'] # the suffix will get stripped off later

    if paths:
      # find preferred paths (smallest amounts of ../)
      paths = list(filter_preferred_paths(paths))

      # we'll need to show a popup if there are still multiple choices
      if len(paths) == 1:
        insert_import_and_sort(view, edit, name, paths[0])
      else:
        # if we hit escape, don't error out or try to import something
        def on_done(index):
          if index >= 0:
            view.run_command('phet_internal_import', {"name": name, "path": paths[index]})
        view.window().show_quick_panel(paths, on_done)
    else:
      view.window().status_message('could not find: ' + name)
  else:
    view.window().status_message('contains import for: ' + name)




class PhetInternalImportCommand(sublime_plugin.TextCommand):
  def run(self, edit, name, path):
    view = self.view
    insert_import_and_sort(self.view, edit, name, path)

class PhetInternalGoToRepoCommand(sublime_plugin.TextCommand):
  def run(self, edit, repo):
    view = self.view
    view.window().open_file(get_git_root(view) + '/' + repo + '/README.md', sublime.TRANSIENT)





class PhetDevCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    print('test')

class PhetLintCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    repo = get_repo(view)
    if repo:
      execute_and_show(view, 'grunt', ['lint', '--no-color'], get_git_root(view) + '/' + repo)

class PhetUpdateCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    repo = get_repo(view)
    if repo:
      execute_and_show(view, 'grunt', ['update', '--no-color'], get_git_root(view) + '/' + repo)

class PhetGruntCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    repo = get_repo(view)
    if repo:
      execute_and_show(view, 'grunt', ['--no-color'], get_git_root(view) + '/' + repo)

class PhetImportCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    for region in view.sel():
      # get the name we're trying to import
      name = view.substr(view.word(region))

      try_import_name(name, view, edit)

class PhetCleanCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    remove_unused_imports(view, edit)
    sort_imports(view, edit)

class PhetSortImportsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    sort_imports(view, edit)

class PhetRemoveUnusedImportsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    remove_unused_imports(view, edit)

class PhetDocumentFunction(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    for region in view.sel():
      start_point = region.begin()
      name_region = view.word(region)
      name = view.substr(name_region)
      previous_line_point = view.full_line(name_region).begin() - 1
      name_scope_region = view.extract_scope(start_point)
      name_and_parameters = view.substr(view.extract_scope(name_scope_region.end()))
      function_scope_region = view.extract_scope(view.full_line(name_scope_region).end() + 1)
      indentation = view.indentation_level( start_point )

      hasReturn = 'return' in view.substr(function_scope_region)

      parameters = []
      paren_start = name_and_parameters.find('( ')
      paren_end = name_and_parameters.find(' )')
      if paren_start >= 0 and paren_end >= 0:
        # todo: handle defaults?
        parameters = name_and_parameters[paren_start + 2 : paren_end].split( ', ' )

      whitespace = indentation * '  '
      comment = '\n' + whitespace + '/**\n' + whitespace + ' * '
      if name == 'dispose':
        comment = comment + 'Releases references\n' + whitespace + ' * @public'
      if name == 'step':
        comment = comment + 'Steps forward in time\n' + whitespace + ' * @public'
      comment = comment + '\n'
      if parameters:
        comment = comment + whitespace + ' *\n'
        for parameter in parameters:
          # todo: guess type
          comment = comment + whitespace + ' * @param {' + detect_type(parameter) + '} ' + parameter + '\n'
      if hasReturn:
        comment = comment + whitespace + ' * @returns {*}\n'
      comment = comment + whitespace + ' */'

      view.insert(edit, previous_line_point, comment)

class PhetOpenPhetmarksCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    open_link(get_local_testing_url() + 'phetmarks')

class PhetOpenGithubCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    repo = get_repo(view)
    if repo:
      open_link('https://github.com/phetsims/' + repo)

class PhetOpenIssuesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    repo = get_repo(view)
    if repo:
      open_link('https://github.com/phetsims/' + repo + '/issues')

class PhetOpenSimCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    repo = get_repo(view)
    if repo:
      open_link(get_local_testing_url() + repo + '/' + repo + '_en.html?ea&brand=phet')

class PhetOpenBuiltSimCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    repo = get_repo(view)
    if repo:
      open_link(get_local_testing_url() + repo + '/build/phet/' + repo + '_en_phet.html')

class PhetGoToRepoCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    active_repos = get_active_repos(view)

    # if we hit escape, don't error out or try to import something
    def on_done(index):
      if index >= 0:
        view.run_command('phet_internal_go_to_repo', {"repo": active_repos[index]})
    view.window().show_quick_panel(active_repos, on_done)
