# Using eslint through the SublimeLinter plugin

These steps were verified on Ubuntu 16.04 and Mac OS X 10.11 with Sublime Text 3, node 5.3.0 and eslint 2.9.0. Other setups and versions are also likely to work.

 - You should have node.js installed
 - You may already have the ST3 SublimeLinter package. If not, get it through Package Control in the usual way.
 - Install eslint system-wide: `sudo npm install -g eslint`
   - For Windows, enter in the git bash (MINGW64): `npm install -g eslint`
 - Make sure the eslint executable can be located by ST3 (in $PATH on OSX/Linux).
   - For Windows, make sure the directory of eslint.cmd is in your path:
     - Go to Control Panel > System and Security > System > Advanced system settings
     > Environment Variables > System variables > Path > Edit
     - Add a semicolon `;` at the end and your equivalent of `C:\Users\Andrea\AppData\Roaming\npm`
 - Install the eslint plugin (`SublimeLinter-eslint`) through Package control.
 - In ST3, open Preferences > Package Settings > SublimeLinter > Settings - User. Modify the arguments to include the PhET configuration and rules. For example (On Windows):
```json
// SublimeLinter Settings - User
{
  "linters": {
    "eslint": {
      "disable": false,
           "args": [
        "--config",
        "${folder}\\chipper\\eslint\\.eslintrc.js",
        "--rulesdir",
        "${folder}\\chipper\\eslint\\rules\\"
        ],
          "executable": "${folder}\\chipper\\node_modules\\.bin\\eslint.cmd",
          "lint_mode": "background"
    }
  }
}

```
Then, you can choose when you want it to run through Tools > SublimeLinter, (on load, save, perpetually in the background, etc.) Background mode is nice for real-time feedback.
