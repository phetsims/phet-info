**Simulation Deployment Guidelines**
=============

Variables to replace in the instructions below:

```
SIM = the name of your sim's repo
VERSION = the identifier of your sim, eg "1.0.0-rc.2"
USERNAME = your username on spot and figaro
```

**Steps to publish a 'dev' version with grunt deploy-dev:**

If this is the first time you've deployed a dev version with grunt deploy-dev, you'll
need to create a file `$HOME/.phet/build-local.json` with a field "devUsername": [spot user name].
Optionally, you can add fields for "devDeployServer" and "devDeployPath"
if you want to deploy to another server and path besides spot.

Optionally, create an ssh key to avoid entering your password:

- create an rsa key in ~/.ssh (run "ssh-keygen -t rsa" to generate a key if you don't already have one).
- add an entry for spot in ~/.ssh/authorized_keys like so (you may need to create this file):

```
Host spot
   HostName spot.colorado.edu
   User [identikey]
   Port 22
   IdentityFile ~/.ssh/id_rsa
```
- On spot, you'll need to add your public key (found in ~/.ssh/id_rsa.pub) to a file ~/.ssh/authorized_keys

To deploy to spot:

1. Update the version identifier in package.json. The identifier should contain "dev", e.g. "1.0.0-dev.2".
2. Commit & push.
3. Run the build process: `grunt`
4. If this is the first time you've deployed anything for this sim, deploy with `grunt deploy-dev --mkdir` (requires 2 password inputs if ssh key is not set up)
5. Otherwise just use `grunt deploy-dev`

**Steps to publish a 'dev' version with deploy-dev.sh (depricated):**

If this is the first time you've deployed anything for this sim, log in to spot and do this:

```
cd /htdocs/UCB/AcademicAffairs/ArtsSciences/physics/phet/dev/html
mkdir $SIM
cp example-sim/.htaccess $SIM
```
Then:

1. Update the version identifier in package.json. The identifier should contain "dev", e.g. "1.0.0-dev.2".
2. Commit & push.
3. Run the build process: `grunt`
4. Deploy to the server: deploy-dev.sh $USERNAME

**Steps to publish a 'rc' (release candidate) version:**

If this is the first release candidate on a release branch:

1. Create a release branch and switch to it, e.g.: `git checkout -b 1.0`. Release branches are named using major and minor version numbers, eg "1.0".
2. Update the version identifier in package.json. The first rc version should have suffix "rc.1", eg "1.0.0-rc.1".
3. Commit & push.
4. Run the build process: `grunt`
5. Deploy to the server: `grunt deploy-dev` (or `deploy-dev.sh $USERNAME`)

If this is not the first release candidate on a release branch:

1. Check out the release branch, e.g.: `git checkout 1.0`
2. Check out the correct shas for dependencies: `grunt checkout-shas`
3. Update the version identifier in package.json. The identifier should contain "rc", e.g. "1.0.0-rc.2".
4. Commit & push.
5. Run the build process: `grunt`
6. Deploy to the server: (or `deploy-dev.sh $USERNAME`)
7. (optional) Check out master for dependencies: `grunt checkout-master`

**Steps to publish a public version:**

1. Create a screenshot that is 2048x1344.  Generally this is done by taking a screenshot on an iPad 3 or higher (since
it has the retina display) with multiple tabs open, then crop the chrome off of it to 2048x1342, then pad the top with 2
pixels of the sim's background color (to 2048x1344) and save as /assets/$SIM-screenshot.png.  Eventually, quick and easy
creation of this screen shot will be supported through the screenshot feature from the PhET menu, but as of this writing
this support doesn't exist.
2. A public version is generally based on some rc version, with an updated version identifier. Follow the steps above for
publishing an rc version, but use a version identifier of the form "major.minor.maintenance". For example, if the published
version is based on "1.1.0-rc.4", then the published version identier will be "1.1.0".
3. If this is the first time you've deployed a public version of this sim, log in to figaro and do this:
   + `mkdir /data/web/htdocs/phetsims/sims/html/$SIM`
   + `copy a .htaccess file from another sim to /data/web/htdocs/phetsims/sims/html/$SIM/.htaccess`
   + `edit /data/web/htdocs/phetsims/sims/html/$SIM/.htaccess to have the correct sim`
4. Create the deploy directory on figaro:
   + `mkdir /data/web/htdocs/phetsims/sims/html/$SIM/$VERSION`
5. Create 600x394 and 128x84 resized copies of the screenshot by running `grunt generate-thumbnails`.  The images
will be placed into the build directory.  Open the images to verify that they were correctly generated.
6. On your local machine, move the files to figaro by entering the command:
`cd build; scp -r * $USERNAME@figaro:/data/web/htdocs/phetsims/sims/html/$SIM/$VERSION`
7. Edit /data/web/htdocs/phetsims/sims/html/$SIM/.htaccess to have the correct version number (this makes the sim
'live').
8. You'll need to add a .htaccess file to the version directory in order to make the download link actually do a download rather than open in the browser. You can copy this from a previously deployed HTML5-only sim, such as from ```/data/web/htdocs/phetsims/sims/html/area-builder/1.0.0/.htaccess```.  Note that this is a different .htaccess file that lives in the versioned directory, not in the sim root.
9. Test: http://phet.colorado.edu/sims/html/$SIM/latest/$SIM_en.html
10. If this was a first public deploy, ask @jonathanolson or @aaronsamuel137 to make it appear on the website.
11. If this is the initial publication, generate and check in (on the master branch) the auto-generated readme file for a published sim.  The README.md file can be created using ```grunt generate-published-README```.
12. The 3rd party contributions page must be updated.  Directions for how to do this are in reportThirdParty.js.  
Brace yourself-- this will take >30 minutes since you will need to build all of the simulations in order to access 
their 3rd party encumbrances.  After running this, the updated third-party-licenses.md file should be checked in to GitHub,
which will make it publicly available to people who click on "3rd party contributions" from the sim.  If this process
is too cumbersome, in the future we can discuss ways to just generate a report for the new sim and integrate it into the existing report.