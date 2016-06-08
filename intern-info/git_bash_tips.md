More in here later, but for the moment..

For windows users:
I think when you install git bash in "Adujusting your PATH environment" choose "use GIt from the Windows Command Prompt" this should allow you to use Git from Git Bash

Don't forget to make a .bashrc file
use the `$PATH` command to find the correct diretory to insert the file
file should look something like `PATH=${PATH}:${HOME}/gitdev/chipper/bin`
this will allow chipper scripts (such as 'pull-all.sh') to be run from anywhere in git-bash

For full capabilities need to install node.js

