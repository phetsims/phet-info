# Deploying a PhET Simulation

## Step 1. Set up the codebase
* DEV: Dev deploys are often made from master using `pull-all.sh`, but you can use code from branches if you wish 
* FIRST_RC: create a branch with MAJOR.MINOR matching the sim to be published, such as 1.2.  For instance: `git checkout -b 1.2` 
* SUBSEQUENT_RC | PRODUCTION: check out the branch with MAJOR.MINOR and any supporting branches from other repos.  `npm update` in the sim repo and `npm update` in chipper.  If there are failures during
 `npm update` then you must `rm -rf node_modules` and `npm install` in that directory instead.

## Step 2. Update the version number in package.json and commit it
Use version names of the following form: 
* DEV: The version number should contain -dev, such as "1.0.0-dev.2". 
* RC: "1.0.0-rc.2" 
* PRODUCTION: "1.0.1"
* PHET_IO: use the patterns above and the build process will automatically append "-phetio" into the version name

## Step 3. Build the simulation with chipper
* PHET_BRAND: `grunt`
* PHET_IO: `grunt --brand=phet-io`

## Step 4. Test the built version
* PHET_BRAND: Launch the simulation and make sure it behaves properly
* PHET_IO: Test wrappers such as the instance-proxies wrapper, and use ?relativeSimPath so it will use relative path instead of looking on phet-io.colorado.edu
* For version numbers 1.0.0 and higher without suffixes, an update check failure message appears in the console. This is expected for local viewing, and will not appear when the sim is published on the PhET Website

## Step 5. Deploy the tested version
* FIRST DEV RELEASE FOR A SIM: `grunt deploy-dev --mkdir` (requires 2 password inputs or ssh key)
* SECOND OR LATER DEV RELEASE: `grunt deploy-dev`
* RC: `grunt deploy-rc`
* RC for PHET_IO: `grunt deploy-rc --brand=phet-io`
* PRODUCTION: `grunt deploy-production --locales=*` (or just `grunt deploy-production` for ph-scale and ph-scale-basics, see https://github.com/phetsims/phet-info/issues/10).  This will instruct the build server to build the English version of the simulation as well as all currently deployed translated versions and deploy them on the web site.  This will also deploy the locally built version to the dev server.  (Note: If you're sure that the version of chipper that is being used is from Nov 10 2015 or later, the `--locales=*` flag can be omitted.)
* PRODUCTION for PHET_IO: `grunt deploy-production --brand=phet-io --locales=*` (or just `grunt deploy-production --brand=phet-io` for ph-scale and ph-scale-basics, see https://github.com/phetsims/phet-info/issues/10).  This will instruct the build server to build the English version of the simulation as well as all currently deployed translated versions and deploy them on the web site.  This will also deploy the locally built version to the dev server.  (Note: If you're sure that the version of chipper that is being used is from Nov 10 2015 or later, the `--locales=*` flag can be omitted.)

## Step 6. Test the deployed version
Run Step 4, but for the published version

## Step 7. Post-publication steps
* PRODUCTION PHET_BRAND: 
 - [ ] If this is a new sim, both the simulation and project will need to marked "visible" in the website admin interface.
        Usually the person in charge of uploading all of the meta information will be responsible for doing this. After that,
        make sure the sim page appears correctly on the website. Talk to @jonathanolson or @jbphet if it hasn't appeared after marking the sim and project visible.
          - When viewing the website you may encounter stale content due to the varnish cache.  There are two ways to avoid this.
            - To check a small number of issues, add a unique parameter to the end of every query. You must change it every time you refresh the url. Example: `http://phet.colorado.edu/sims/html/example-sim/latest/example-sim_en.html?test-parameter1`
            - To avoid the cache permanently, you need to add a cookie with the name `NO-CACHE` and with an arbitrary or empty value. Cookie usage cannot be covered in entirety here. To use cookies with `curl` see [this answer](http://stackoverflow.com/a/7186160/2496827). To add custom cookies in Chrome [see this solution](http://superuser.com/a/636697/493443)
        - [ ] If this is the initial publication, generate and check in (on the master branch) the auto-generated readme file for a published sim.  The README.md file can be created using ```grunt published-README```.
        - [ ] If this is *not* a new simulation, verify that any previously existing translations are still available and that
        their version numbers are correct.
        - [ ] Update the "Latest fully tested SHAs" in the PhET brand RC version of this document.
        - [ ] After the new simulation is available from the website, the 3rd party contributions page must be updated.  Directions for how to do this are in reportThirdParty.js.
* PRODUCTION PHET_IO_BRAND:
  - [ ] If this is a version that will be used with students, then make sure to remove the password protection. See https://github.com/phetsims/phet-io/blob/master/doc/phetio-security.md for details.
* RC | PRODUCTION: Update the "latest SHAs under testing" above, if appropriate.  Keep in mind that not all sims use all repos.

## Step 8. Restore your working copy
* Check out master for dependencies: `grunt checkout-master`
* Check out master for the sim repo: `git checkout master`
* Update node_modules: `npm update` in the sim repo and `npm update` in chipper.  If there are failures during `npm update` then you must `rm -rf node_modules` and `npm install` in that directory instead.