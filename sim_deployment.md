
** Simulation Deployment Guidelines **

Constants to replace:
SIM = the name of your sim's repo
VERSION = the version of your release candiate, eg "1.0.0-rc.2"
USERNAME = your username on spot and figaro

*Steps to publish a 'dev' version:*

1. Set version number to $VERSION in package.json and versions.js (commit & push)
2. grunt
3. If this is the first time you've deployed a 'dev' version of this sim, log in to spot and do this:
mkdir /htdocs/UCB/AcademicAffairs/ArtsSciences/physics/phet/dev/html/$SIM
4. deploy-dev.sh $USERNAME

*Steps to publish a 'rc' (release candidate) version:*

1. Create and checkout a new branch. The first rc version will be on a branch called "1.0"
2. Update the version number in package.json and js/version.js. The first rc version should be "1.0.0-rc.1"
3. Commit and push to the new branch.
4. Run grunt. Make sure that the correct libraries are listed under the key "phetLibs" in package.json. This should list
   all of the common libraries as well as the sim being published.
5. If this is getting a full test matrix, copy build/dependencies.json to the sim root. Commit and push to the new branch.
   Otherwise, if this sim is only getting spot testing or if this release candidate is getting promoted to production,
   /dependencies.json should remain as it was from the last well tested release candidate. In this case, to ensure that
   you are using the exact same dependency's shas, you can run grunt checkout-shas.
6. Run ../chipper/bin/deploy-dev $USERNAME from the sim root. The rc version should now be published!

*Steps to publish a public version:*

1. Create a screenshot on an iPad 3. Crop the chrome off of it (to 2048x1342), pad the top with 2 pixels of background
   color (to 2048x1344) and save as /assets/$SIM-screenshot.png.
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
