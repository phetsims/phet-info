import sublime, sublime_plugin, os

from functools import reduce

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

def lookup_import_paths(view, str):
  """Returns a list of relative paths for modules detected to str"""
  current_path = os.path.dirname(view.file_name())
  locations = list(filter(lambda x: (str + '.js') in x[0] and not ('blue-rain' in x[0]), view.window().lookup_symbol_in_index(str)))
  return list(map(lambda x: os.path.relpath(x[0], current_path), locations))

def count_up_directory(path):
  return path.count('../')

def filter_preferred_paths(paths):
  min_directory_up_count = min(map(count_up_directory,paths))
  return filter(lambda path: count_up_directory(path) == min_directory_up_count, paths)

def contains_import(view, str):
  return not view.find('import ' + str, 0).empty()

def cover_regions(regions):
  return reduce((lambda maybe,region: region if maybe == None else maybe.cover(region)),regions,None)

def find_import_regions(view):
  return view.find_all(r'^import .+;$');

def sort_imports(view, edit):
  import_regions = find_import_regions(view)
  start_index = cover_regions(import_regions).begin()
  import_strings = []

  for region in reversed(import_regions):
    import_strings.append(view.substr(region))
    view.erase(edit,view.full_line(region))

  for import_string in sorted(import_strings,key=(lambda str: str.split('\'')[ 1 ]), reverse=True):
    view.insert(edit, start_index, import_string + '\n')


def insert_import_in_front(view, edit, import_text):
  start_index = cover_regions(find_import_regions(view)).begin()
  view.insert(edit, start_index, import_text + '\n')

def insert_import_and_sort(view, edit, name, path):
  # for relative paths, we need the ./
  if path[0] != '.':
    path = './' + path

  insert_import_in_front(view, edit, 'import ' + name + ' from \'' + path +'\';')
  sort_imports(view, edit)

def test_print(str):
  print(str)

def run_sort_imports(command, view, edit):
  sort_imports(view, edit)

def run_import(command, view, edit):
  for region in view.sel():
    name = view.substr(view.word(region))
    if not contains_import(view, name):
      paths = lookup_import_paths(view, name)
      if paths:
        paths = list(filter_preferred_paths(paths))
        if len(paths) == 1:
          insert_import_and_sort(view, edit, name, paths[0])
        else:
          view.show_popup_menu(paths, lambda index: insert_import_and_sort(view, edit, name, paths[index]) if index >= 0 else 0)
      else:
        view.window().status_message('could not find: ' + name)
    else:
      view.window().status_message('contains import for: ' + name)






