More in here later, but for the moment..

For windows users:
 when you install git bash in "Adujusting your PATH environment" choose "use GIt from the Windows Command Prompt" this should allow you to use Git from Git Bash

make a .bashrc file in the top level directory (the directory in which your phetsims folder lives) something like c:\users\username
To create the .bashrc file make it in notepad and do **Save as** ".bashrc" (you must use the quotes or notepad will append a .txt extension)

use the `$PATH` command to find the correct diretory to insert the file
assuming the folder for your files is "phetsims" the .bashrc file should look something like `PATH=${PATH}:${HOME}/gitdev/chipper/bin`
this will allow chipper scripts (such as 'pull-all.sh') to be run from anywhere in git-bash

For full capabilities need to install node.js
in the chipper directory run `npm install`
run `npm install -g grunt`
run `npm install -g eslint`

