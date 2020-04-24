# Copyright 2020, University of Colorado Boulder
#
# @author Jonathan Olson <jonathan.olson@colorado.edu>

import sublime, sublime_plugin, os, re, subprocess, webbrowser, json, threading

from functools import reduce

# Useful URLs:
# https://www.sublimetext.com/docs/3/api_reference.html
# http://www.sublimetext.com/docs/commands
# https://github.com/Binocular222/Sublime-Text-3-Full-Documentation
# https://github.com/Binocular222/Sublime-Text-3-Full-Documentation/blob/master/Command.txt
# https://www.sublimetext.com/docs/3/scope_naming.html
# https://sublime-text-unofficial-documentation.readthedocs.io/en/latest/reference/api.html

# undocumented APIs?:
# [func for func in dir(sublime.View) if callable(getattr(sublime.View, func))]
# [func for func in dir(sublime.Window) if callable(getattr(sublime.View, func))]
# lookup_references_in_index / lookup_references_in_open_files / lookup_symbol_in_index / lookup_symbol_in_open_files
# [func for func in dir(sublime) if callable(getattr(sublime.View, func))]

# potential commands?
# auto_complete build clear_fields close_file copy cut decrease_font_size delete_word duplicate_line exec
# expand_selection find_all_under find_next find_prev find_under find_under_expand find_under_prev focus_group
# hide_auto_complete hide_overlay hide_panel increase_font_size indent insert insert_snippet join_lines left_delete move
# move_to move_to_group new_file new_window next_field next_result next_view next_view_in_stack paste paste_and_indent
# prev_field prev_result prev_view prev_view_in_stack prompt_open_file prompt_save_as prompt_select_project redo
# redo_or_repeat reindent right_delete run_macro run_macro_file save scroll_lines select_all select_lines set_layout
# show_overlay show_panel show_scope_name single_selection slurp_find_string slurp_replace_string soft_redo soft_undo
# sort_lines split_selection_into_lines swap_line_down swap_line_up switch_file toggle_comment toggle_full_screen
# toggle_overwrite toggle_record_macro toggle_side_bar transpose undo unindent

# >>> view.extract_completions( 'updateS' )
# ['updateSize', 'updateStepInformation']

# >>> view.indentation_level( view.sel()[0].begin() )
# 2

# view.substr(view.indented_region( view.sel()[0].begin() ))

# >>> view.indexed_references()
# [((798, 803), 'merge'), ((826, 844), 'createFromVertices'), ((856, 876), 'getEllipsoidVertices'), ((937, 954), 'getEllipsoidShape'), ((1007, 1016), 'getVolume'), ((1100, 1106), 'assert'), ((1339, 1349), 'updateSize'), ((1500, 1518), 'updateFromVertices'), ((1541, 1561), 'getEllipsoidVertices'), ((1676, 1693), 'getEllipsoidShape'), ((1764, 1773), 'getVolume'), ((2571, 2581), 'updateSize'), ((2593, 2610), 'getSizeFromRatios'), ((2690, 2716), 'bodyGetStepMatrixTransform'), ((2785, 2788), 'm02'), ((2828, 2831), 'm12'), ((3767, 3781), 'getTranslation'), ((3784, 3793), 'toVector3'), ((3881, 3889), 'minusXYZ'), ((4703, 4726), 'solveQuadraticRootsReal'), ((4738, 4744), 'filter'), ((6232, 6237), 'reset'), ((6250, 6260), 'updateSize'), ((6300, 6305), 'reset'), ((6516, 6523), 'ellipse'), ((6926, 6930), 'push'), ((6950, 6953), 'cos'), ((6981, 6984), 'sin'), ((7329, 7337), 'register')]

# >>> view.indexed_symbols()
# [((625, 634), 'Ellipsoid'), ((747, 758), 'constructor'), ((1463, 1473), 'updateSize'), ((2161, 2178), 'getSizeFromRatios'), ((2523, 2532), 'setRatios'), ((2648, 2669), 'updateStepInformation'), ((3703, 3712), 'intersect'), ((5097, 5113), 'getDisplacedArea'), ((5706, 5724), 'getDisplacedVolume'), ((6200, 6205), 'reset'), ((6462, 6479), 'getEllipsoidShape'), ((6729, 6749), 'getEllipsoidVertices'), ((7216, 7225), 'getVolume')]

# for temp files:
# def get_cache_directory():
#   path = os.path.join(sublime.cache_path(), 'phet')
#   if not os.path.exists(path):
#     os.mkdir(path)
#   return path

# sublime.log_commands(True)
# sublime.log_commands(False)

linesep = os.linesep
pathsep = os.path.sep

goto_region_dict = {}

def clear_goto_region(id):
  goto_region_dict[id] = []

def push_goto_region(id, from_region, to_file, to):
  if id not in goto_region_dict:
    clear_goto_region(id)
  goto_region_dict[id].append({'from_region': from_region, 'to_file': to_file, 'to': to})

def lookup_goto_region(id, point):
  if id not in goto_region_dict:
    return None
  for entry in goto_region_dict[id]:
    from_region = entry['from_region']
    if point > from_region.begin() and point < from_region.end():
      return entry

load_actions = {}



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

def path_split(path):
  splits = os.path.split(path)
  if splits[0]:
    return path_split(splits[0]) + [splits[1]]
  else:
    return [splits[1]]

def get_repo(view):
  relative_path = get_relative_to_root(view, view.file_name())
  if relative_path[0] == '.':
    return None
  else:
    return path_split(relative_path)[0]

def count_up_directory(path):
  """Returns a count of ../, for determining what the best path is to import"""
  return path.count('../')

def union_regions(regions):
  """Returns the union of sublime.Region instances (using their term 'cover')"""
  return reduce((lambda maybe,region: region if maybe == None else maybe.cover(region)),regions,None)

def expand_region(region, str, num_lines):
  begin = region.begin()
  end = region.end()

  # TODO: Windows?

  # expand to the line
  begin = str.rfind('\n', 0, begin) + 1
  end = str.find('\n', end, len(str))

  for x in range(num_lines):
    if begin > 1:
      begin = str.rfind('\n', 0, begin - 2 ) + 1
    if end < len(str) - 1 and end != -1:
      end = str.find('\n', end + 1, len(str))

  if begin == -1:
    begin = 0
  if end == -1:
    end = len(str)

  return sublime.Region(begin, end)

def collapse_expanded_regions(regions, str, num_lines):
  current = None
  result = []

  for region in regions:
    expanded_region = expand_region(region, str, num_lines)
    if current:
      if current['expanded_region'].intersects(expanded_region):
        current['expanded_region'] = current['expanded_region'].cover(expanded_region)
        current['regions'].append(region)
      else:
        result.append(current)
        current = {'expanded_region': expanded_region, 'regions': [region]}
    else:
      current = {'expanded_region': expanded_region, 'regions': [region]}

  if current:
    result.append(current)
  return result

def is_node_js(view):
  """Whether we're handling things in a node.js or module context"""
  return (not view.find('\n\'use strict\';\n', 0).empty()) and (not view.find(' = require\\( \'', 0).empty())

def load_file(path):
  """Loads a file as a string"""
  with open(path, 'r', encoding='utf8') as content_file:
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

def show_lint_output(output):
  lines = output.splitlines()
  output_view = sublime.active_window().create_output_panel('phetlint')
  clear_goto_region(output_view.id())

  current_file = None
  for line in lines:
    match = re.search('^ +([0-9]+):([0-9]+)', line )
    if len(line) > 0 and line[0] == '/':
      current_file = line
      output_view.run_command('phet_internal_append_result', {'str': line + '\n'})
    elif match:
      row = int(match.group(1)) - 1
      col = int(match.group(2)) - 1
      output_view.run_command('phet_internal_append_search_result_row_col', {'str': line, 'to_file': current_file, 'row': row, 'col': col})
      output_view.run_command('phet_internal_append_result', {'str': '\n'})
    else:
      output_view.run_command('phet_internal_append_result', {'str': line + '\n'})

  sublime.active_window().run_command('show_panel', {"panel": "output.phetlint"})

abort_search = False

def threaded_for_js_files(repos, git_root, on_path, on_done):
  def thread_target(repos, git_root, on_path, on_done):
    global abort_search
    for repo in repos:
      # TODO: git root should be a setting? or get from the active window instead
      repo_path = os.path.join(git_root, repo + '/js')
      for root, dirs, files in os.walk(repo_path):
        is_phet_io_dir = 'js/phet-io' in root
        for name in files:
          if '-baseline.js' in name or '-overrides.js' in name or '-types.js' in name:
            continue
          path = os.path.join(root, name)
          if abort_search:
            abort_search = True
            return
          on_path(path)
    on_done()
  thread = threading.Thread(target=thread_target, args=(repos, git_root, on_path, on_done))
  thread.start()
  # returns immediately after the thread starts
  return thread


class PhetInternalImportCommand(sublime_plugin.TextCommand):
  def run(self, edit, name, path):
    view = self.view
    insert_import_and_sort(self.view, edit, name, path)

class PhetInternalGoToRepoCommand(sublime_plugin.TextCommand):
  def run(self, edit, repo):
    view = self.view
    view.window().open_file(get_git_root(view) + '/' + repo + '/README.md', sublime.TRANSIENT)

class PhetInternalAppendResult(sublime_plugin.TextCommand):
  def run(self, edit, str):
    view = self.view
    view.set_read_only(False)
    view.insert(edit, view.size(), str)
    view.set_read_only(True)

class PhetInternalAppendSearchResultRegion(sublime_plugin.TextCommand):
  def run(self, edit, str, to_file, start_index, end_index):
    view = self.view
    view.set_read_only(False)
    start = view.size()
    view.insert(edit, start, str)
    end = view.size()
    find_region = sublime.Region(start, end)

    view.add_regions('phet_find_result', view.get_regions('phet_find_result') + [find_region], 'string')

    view.set_read_only(True)
    push_goto_region(view.id(), find_region, to_file, sublime.Region(start_index, end_index))

class PhetInternalAppendSearchResultRowCol(sublime_plugin.TextCommand):
  def run(self, edit, str, to_file, row, col):
    view = self.view
    view.set_read_only(False)
    start = view.size()
    view.insert(edit, start, str)
    end = view.size()
    find_region = sublime.Region(start, end)

    # TODO: set our own sytax and colors, but for now just borrow this
    # view.add_regions('phet_find_result', view.get_regions('phet_find_result') + [find_region], 'string', flags=(sublime.DRAW_NO_FILL))
    view.add_regions('phet_find_result', view.get_regions('phet_find_result') + [find_region], 'string')
    # view.add_regions('phet_find_result', view.get_regions('phet_find_result') + [find_region], 'constant')
    # view.add_regions('phet_find_result', view.get_regions('phet_find_result') + [find_region], 'keyword')
    view.set_read_only(True)
    push_goto_region(view.id(), find_region, to_file, (row, col))

class PhetInternalSearch(sublime_plugin.TextCommand):
  def run(self, edit, pattern):
    view = self.view

    output_view = sublime.active_window().create_output_panel('phetfind')
    output_view.set_syntax_file('Packages/phet-plugin/phet-find-results.tmLanguage')
    clear_goto_region(output_view.id())

    output_view.run_command('phet_internal_append_result', {'str': 'Searching...\n\n'})
    sublime.active_window().run_command('show_panel', {"panel": "output.phetfind"})

    expr = re.compile(pattern)

    def regions_from_string(str):
      regions = []
      for match in expr.finditer(str):
        regions.append(sublime.Region(match.start(), match.end()))
      return regions

    def on_path(path):
      file_string = load_file(path)
      regions = regions_from_string(file_string)
      if regions:
        # TODO windows
        display_name = path[path.rfind('/')+1:]
        if '.js' in display_name:
          display_name = display_name[:display_name.find('.js')]

        output_view.run_command('phet_internal_append_result', {'str': display_name + ' ' + path + ':\n\n'})

        expanded_region_data = collapse_expanded_regions(regions, file_string, 2)

        for entry in expanded_region_data:
          expanded_region = entry['expanded_region']
          sub_regions = entry['regions']

          if sub_regions[0].begin() > expanded_region.begin():
            output_view.run_command('phet_internal_append_result', {'str': file_string[expanded_region.begin():sub_regions[0].begin()]})
          for i in range(len(sub_regions)):
            sub_region = sub_regions[i]
            output_view.run_command('phet_internal_append_search_result_region', {'str': file_string[sub_region.begin():sub_region.end()], 'to_file': path, 'start_index': sub_region.begin(), 'end_index': sub_region.end()})
            if i + 1 < len(sub_regions):
              next_sub_region = sub_regions[i + 1]
              if sub_region.end() < next_sub_region.begin():
                output_view.run_command('phet_internal_append_result', {'str': file_string[sub_region.end():next_sub_region.begin()]})
          last_sub_region = sub_regions[len(sub_regions) - 1]
          if last_sub_region.end() < expanded_region.end():
            output_view.run_command('phet_internal_append_result', {'str': file_string[last_sub_region.end():expanded_region.end()]})

          output_view.run_command('phet_internal_append_result', {'str': '\n\n'})

    def on_done():
      output_view.run_command('phet_internal_append_result', {'str': 'Done\n'})

    repos = get_active_repos(view)
    preferred_repo = get_repo(view)
    repos.remove(preferred_repo)
    repos.insert(0, preferred_repo)

    threaded_for_js_files(repos, get_git_root(view), on_path, on_done)


class PhetDevCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view

    print(get_repo(view))

class PhetFindCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view

    if len(view.sel()):
      view.run_command('phet_internal_search', {'pattern': re.escape(view.substr(view.word(view.sel()[0])))})

class PhetFindRegexCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view

    def on_done(str):
      view.run_command('phet_internal_search', {'pattern': str})

    view.window().show_input_panel('Find regex', '', on_done, None, None)

class PhetShowFindCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view

    sublime.active_window().run_command('show_panel', {"panel": "output.phetfind"})

class PhetWipeFindCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view

    output_view = sublime.active_window().create_output_panel('phetfind')
    output_view.erase(edit, sublime.Region(0,output_view.size()))
    clear_goto_region(output_view.id())

class PhetAbortFindCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view

    abort_search = True;

    output_view = sublime.active_window().create_output_panel('phetfind')
    output_view.erase(edit, sublime.Region(0,output_view.size()))
    clear_goto_region(output_view.id())

class PhetLintCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    repo = get_repo(view)
    if repo:
      execute('grunt', ['lint', '--no-color'], get_git_root(view) + '/' + repo, show_lint_output)

class PhetLintEverythingCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    execute('grunt', ['lint-everything', '--no-color'], get_git_root(view) + '/perennial', show_lint_output)

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

class PhetEventListener(sublime_plugin.EventListener):
  def on_load(self, view):
    id = view.id()
    if id in load_actions:
      load_actions[id]()
      del load_actions[id]
  def on_selection_modified_async(self, view):
    for region in view.sel():
      entry = lookup_goto_region(view.id(), region.begin())
      if entry:
        new_view = sublime.active_window().open_file(entry['to_file'], sublime.TRANSIENT)
        def on_loaded():
          to = entry['to']
          if isinstance(to, sublime.Region):
            to_region = to
          else:
            point = new_view.text_point(to[0], to[1])
            to_region = sublime.Region(point, point)
          new_view.sel().clear()
          new_view.sel().add(to_region)
          if new_view.window():
            new_view.window().focus_view(new_view)
            new_view.window().run_command('focus_neighboring_group')
          sublime.active_window().focus_view(new_view)
          sublime.set_timeout(lambda: new_view.window().focus_view(new_view), 10)
          new_view.show_at_center(to_region)
        if new_view.is_loading():
          load_actions[new_view.id()] = on_loaded
        else:
          on_loaded()



