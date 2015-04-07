
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

1. Create a screenshot on an iPad 3. Crop the chrome off of it (to 2048x1344), pad the top with 2 pixels of background
   color (to 2048x1344) and save as /assets/$SIM-screenshot.png.
2. Publish a 'dev' version, as described above.
3. If this is the first time you've deployed a public version of this sim, log in to figaro and do this:
   + mkdir /data/web/htdocs/phetsims/sims/html/$SIM
   + copy a .htaccess file to /data/web/htdocs/phetsims/sims/html/$SIM/.htaccess
   + edit /data/web/htdocs/phetsims/sims/html/$SIM/.htaccess to have the correct sim
4. Create the deploy directory on figaro:
mkdir /data/web/htdocs/phetsims/sims/html/$SIM/$VERSION
5. Create 600x394 and 128x84 resized copies of the screenshot by running ```grunt generate-thumbnails```.  The images
will be placed into the build directory.
6. On your local machine, move the files to figaro by entering the command:
```cd build; scp -r * $USERNAME@figaro:/data/web/htdocs/phetsims/sims/html/$SIM/$VERSION```
7. edit /data/web/htdocs/phetsims/sims/html/$SIM/.htaccess to have the correct version number (this makes the sim 'live')
8. If this is an HTML5 only sim and you are publishing a new version (i.e. area-builder or ph-scale-basics), you'll need
   to copy 2 other files from an older version folder to the new version folder: $SIM-screenshot.png and .htaccess.
   The screenshot is what appears on the website sim page. The .htaccess allows the download link to work on Safari
   (note this is a different .htaccess file that lives in the versioned directory, not in the sim root). To do this, you
   can ssh into figaro and use cp -p. This is probably going to be a temporary step until we figure out our build system
   and how we want to do html sim pages. Contact @aaronsamuel137 with any questions.
9. test: http://phet.colorado.edu/sims/html/$SIM/latest/$SIM_en.html
10. If this was a first public deploy, ask JO or Aaron how to make it appear on the website.
