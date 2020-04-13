# PhET Sublime Package

## Usage

This package can be used with sublime to add phet tasks to the command palette. To use these tools, you must know how to access the `command palette` (Command-shift-P on Mac, control-shift-P on Windows defaults). Open the command palette, then start typing something to auto-complete to a command name (starting with `phet` is useful). Once the command is highlighted, hit enter to run.

You can open up the Sublime terminal (command/ctrl + \`) to see results from scripts that are run (things are written in Python)

## Commands

###PhET: Import

This will attempt to import the text word that the cursor is over, either with an import or node.js require (depending on what type of file is detected), and then imports will be sorted.

###PhET: Sort Imports

Sorts the import statements of the file.

### PhET: Document Function

When over a function name in a class/other definition, it will stub out JSDoc comments in front with parameter/return value detection.

### PhET: Remove Unused Imports

Searches each import to see if it's unused in the file (currently based on a substring search, so if it's commented it won't remove it currently).

### PhET: Clean

Removes unused imports, and then sorts imports.

## Installing

To add these to your copy of sublime, locate your Packages folder. `Preferences --> Browse Packages`. Then copy this
folder the  `phet-plugin` folder into the `Packages` directory. (On Windows the file path looks like:
`C:\Users\{{USER}}\AppData\Roaming\Sublime Text 3\Packages\`, on Mac it's `~/Library/Application Support/Sublime Text 3/Packages/`).

When these commands are added into the `Packages` folder in the Sublime installation directory, then they will also be
added to the command palette, although a restart may be required.

