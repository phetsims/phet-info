# PhET Sublime Package

This package can be used with sublime to add phet tasks to the command palette. To use these tools, 
you must know how to access the `command palette`.

To add these to your copy of sublime, locate your Packages folder. `Preferences --> Browse Packages`. Then copy this 
folder the  `phet-plugin` folder into the `Packages` directory. (On Windows the file path looks like: 
`C:\Users\{{USER}}\AppData\Roaming\Sublime Text 3\Packages\`).

When these commands are added into the `Packages` folder in the Sublime installation directory, then they will also be
added to the command palette, although a restart may be required.

Usage:

Type `PhET: ` into the command palette for a list of available scripts to be run.
You can open up the Sublime terminal (ctrl + \`) to see results from scripts that are run.


* PhET: Insert Require Statement
  * Used to add the require statement of the type that is highlighted. 
  * This will also sort the list of require statements.
  * Example: Highlight the word "Node"; open command palette; run command 