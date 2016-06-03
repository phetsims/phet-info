# Using eslint through the SublimeLinter plugin

These steps were verified on Ubuntu 16.04 and Mac OS X 10.11 with Sublime Text 3, node 5.3.0 and eslint 2.9.0. Other setups and versions are also likely to work.

 - You should have node.js installed
 - You may already have the ST3 SublimeLinter package. If not, get it through Package Control in the usual way.
 - Install eslint system-wide: `sudo npm install -g eslint`
 - Make sure the eslint executable can be located by ST3 (in $PATH on OSX/Linux). TODO: Windows.
 - Install the eslint plugin (`SublimeLinter-contrib-eslint`).
 - In ST3, open Preferences > Package Settings > SublimeLinter > Settings - User. Modify the arguments to include the PhET configuration and rules. For example:
```json
   "eslint": {
       "@disable": false,
       "args": [
           "--config",
           "/Users/adare/phetsims/chipper/eslint/.eslintrc",
           "--rulesdir",
           "/Users/adare/phetsims/chipper/eslint/rules/"
       ],
       "excludes": []
   },
```
Then, you can choose when you want it to run through Tools > SublimeLinter, (on load, save, perpetually in the background, etc.) Background mode is nice for real-time feedback.
