
** Simulation Deployment Guidelines **

Variables to replace:
SIM = the name of your sim's repo
VERSION = the identifier of your sim, eg "1.0.0-rc.2"
USERNAME = your username on spot and figaro

*Steps to publish a 'dev' version:*

1. Update the version identifier in package.json. The identifier should contain "dev", eg "1.0.0-dev.2".
2. Commit & push.
3. Run the build process: `grunt`
4. If this is the first time you've deployed a "dev" version of this sim, log in to spot and do this:
```
    cd /htdocs/UCB/AcademicAffairs/ArtsSciences/physics/phet/dev/html
    mkdir $SIM
    cp example-sim/.htaccess $SIM
```
5. Deploy to the server: `deploy-dev.sh $USERNAME`

*Steps to publish a 'rc' (release candidate) version:*

If this is the first release candidate on a release branch:

1. Create a release branch. Release branches are named using major and minor version numbers, eg "1.0".
2. Check out the release branch, eg `git checkout 1.0`
3. Update the version identifier in package.json. The first rc version should have suffix "rc.1", eg "1.0.0-rc.1".
4. Commit & push.
5. Run the build process: `grunt`
6. Deploy to the server: `deploy-dev $USERNAME`

If this is not the first release candidate on a release branch:

1. Check out the release branch, eg `git checkout 1.0`
2. Check out the correct shas for dependencies: `grunt checkout-shas`
3. Update the version identifier in package.json. The identifier should contain "rc", eg "1.0.0-rc.2".
4. Commit & push.
5. Run the build process: `grunt`
6. Deploy to the server: `deploy-dev $USERNAME`
7. (optional) Check out master for dependencies: `grunt checkout-master`

*Steps to publish a public version:*

1. Create a screenshot that is 2048x1344.  Generally this is done by taking a screenshot on an iPad 3 or higher (since
it has the retina display) with multiple tabs open, then crop the chrome off of it to 2048x1342, then pad the top with 2
pixels of the sim's background color (to 2048x1344) and save as /assets/$SIM-screenshot.png.  Eventually, quick and easy
creation of this screen shot will be supported through the screenshot feature from the PhET menu, but as of this writing
this support doesn't exist.
2. Publish a 'dev' version, as described above.
3. If this is the first time you've deployed a public version of this sim, log in to figaro and do this:
   + mkdir /data/web/htdocs/phetsims/sims/html/$SIM
   + copy a .htaccess file to /data/web/htdocs/phetsims/sims/html/$SIM/.htaccess
   + edit /data/web/htdocs/phetsims/sims/html/$SIM/.htaccess to have the correct sim
4. Create the deploy directory on figaro:
mkdir /data/web/htdocs/phetsims/sims/html/$SIM/$VERSION
5. Create 600x394 and 128x84 resized copies of the screenshot by running ```grunt generate-thumbnails```.  The images
will be placed into the build directory.  Open the images to verify that they were correctly generated.
6. If this is an HTML5-only sim you'll need to include a screenshot with a width of 300 (the height doesn't matter).
 You can create this by scaling the screenshot in the assets directly.  This should be placed into the build directory
 and named $SIM-screenshot.png.
7. On your local machine, move the files to figaro by entering the command:
```cd build; scp -r * $USERNAME@figaro:/data/web/htdocs/phetsims/sims/html/$SIM/$VERSION```
8. Edit /data/web/htdocs/phetsims/sims/html/$SIM/.htaccess to have the correct version number (this makes the sim
'live').
9. You'll need to add a .htaccess file to the version directory in order to make the download link actually do a download rather than open in the browser. You can copy this from a previously deployed HTML5-only sim, such as from ```/data/web/htdocs/phetsims/sims/html/area-builder/1.0.0/.htaccess```.  Note that this is a different .htaccess file that lives in the versioned directory, not in the sim root.
10. Test: http://phet.colorado.edu/sims/html/$SIM/latest/$SIM_en.html
11. If this was a first public deploy, ask @jonathanolson or @aaronsamuel137 to make it appear on the website.
12. If this is the initial publication, generate and check in (on the master branch) the auto-generated readme file for a published sim.  The readme file can be created using ```grunt generate-published-README```.
