Web Development Intern Setup
=

####Initial machine setup:
######Hardware Requirements
* 30-40 GB free storage
* 8GB+ RAM

There are developers at PhET using Windows and MacOS, if you use a different host OS you may need to independently find solutions.

######Create file directory:
* Create a folder named /phet
* Create subfolders /phet/git and /phet/svn
	
######Setup SSH client:
* Windows: Install putty from http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html
	
####Setup SVN:		
######Install SVN:
* Windows:  You will need access to the command line tools.  
  * SilkSVN is known to be compatible https://sliksvn.com/download
  
######Checkout the svn trunk:
* You will need a good network connection and time as this repository is very large.
* In the `/phet/svn` directory, run the following command
  * `svn checkout https://phet.unfuddle.com/svn/phet_svn/trunk trunk --username guest --password guest`
	
####Setup Git:
######Sign up for a Github account.  
* Go to https://github.com/join.  
* Use the email address that you intend to use for PhET.  
* You will receive a lot of email, so choose your account accordingly.

######Install Git:
* Windows: Install the software found at http://www.git-scm.com/download/win
* If you want git to remember your usename and password (highly recommended), run this command: git config --global credential.helper store
		
######Checkout the website repo from Github:
In the phet/git directory, run this command:
  *	`git clone https://github.com/phetsims/website.git`

######Learn the common git commands:
[Git Tutorial] (http://git-scm.com/docs/gittutorial)

####Setup the VM:
1. Install VirtualBox: https://www.virtualbox.org/wiki/Downloads
1. Get the OVA file. (From Aaron)
2. Import the OVA file in VirtualBox.
3. Setup networking:
	1. Select the VM
	2. Make sure the VM is in "Powered Off" state
	3. Go to Settings > Network > Adapter 1
	4. Make sure the checkbox for "Enable Network Adapter" is checked
	5. Change "Attached to:" to "NAT".  This allows the VM to access the internet via the host.
	6. Go to the Adapter 2 tab
	7. Make sure the checkbox for "Enable Network Adapter" is checked
	8. Change "Attached to:" to "Host-Only Network".  This sets up a network internal to your host so that the VM IP address remains static.
4. Launch the VM:
	> Username: phet
	>	Password: phet

######Setup SSH and sync the DB with figaro
*Requires access to figaro*

1. Add this text to a new file ~/.ssh/config
    ```
    host figaro
    hostname figaro.colorado.edu
    user [YOUR Identikey here]
    port 22
    identityfile ~/.ssh/id_rsa
    ```
    
2. Create an RSA key
    Enter this command in the terminal: ```ssh-keygen -t rsa```

    Press enter 4 times, leave the file path as default and the password blank.
    
3. Copy the contents of ~/.ssh/id_rsa.pub from the VM to ~/.ssh/authorized_keys on figaro.
4. You should now be able to sync the local VM database with figaro by running ~/Desktop/sync.sh (or get the script from Aaron)
	
######Common commands on the VM:
* logs = displays the last 10 lines of the Tomcat logfile and appends it to the console in real time.
* apps = cd to the tomcat7 directory
* restart = restarts the varnish service (clears static cache)
* /var/lib/tomcat7/webapps/restart.sh = Delete unpacked files from war and restart tomcat service
* deploy = Rebuilds application from war.  Needs to be run after restart.sh
		
	

####Setup IntelliJ Idea	
######Initial Setup
1. Sign up for a jetbrains account at the link provided by PhET (Ask Aaron).
2. Download the IntelliJ Idea Ultimate edition https://www.jetbrains.com/idea/download/
3. On initial launch, sign in with your Jetbrains username and password.
	
######Project Setup:
1. Launch IntelliJ
2. Choose Open an existing project.
3. Navigate to phet/svn and click on the "trunk" folder.  It should have an IntelliJ icon, not a normal folder icon.
3. Click OK
4. Setup Java SDK
  1. Go to File > Project Structure > Project Settings:Project 
  5. Select the your locally installed Java SDK under "Project SDK"
  6. Click OK
5. Import Website
  6. Go to Project Settings:Modules
  7. Hit the + in the upper left corner and select "Import Module"
  8. Open phet/git/website/ide/intellij/website.iml		
  9. Click OK
6. Setup the style template:
  1. Download the template xml file from https://github.com/phetsims/phet-info/blob/master/ide/idea/phet-idea-codestyle.xml
  2. Put the file in the local IntelliJ directory.  
    * Try $HOMEPATH$/.IntelliJIdea14/config/codestyles
  3. Restart IntelliJ, go to File > Settings > Editor > Code Style > Java.
  4. Click the "Manage" button next to "Scheme" and select "phet-idea-codestyle".

####Build-tools setup
1. Update lines 62-71 in phet/svn/trunk/build-tools/build-local.properties.template with the following:
    ```
    # Local website development credentials
    local-server.username=phet
    local-server.password=phet

    # Local website Tomcat Manager credentials
    local-server.tomcatmanager.username=phet
    local-server.tomcatmanager.password=phet

    Local website IP address
    local-server.ip={IP of the "host-only" network adapter for the VM}
    ```
3. Update the tomcatmanager credentials for the figaro and simian.  These are provided by the PhET web developer.
4. Update git.root to be the absolute file path of the phet/git directory you created on your machine.
2. Update the ssh credentials for figaro and simian to be your IdentiKey username/password.
3. The file in the same directory as "build-local.properties" 


