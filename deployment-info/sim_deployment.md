# Deploying a PhET Simulation

## Before Beginning.  
#### Build process configuration
                     
 Before building or deploying a simulation, familiarize yourself with configuration options for PhET's build process.
 
 Your default build configuration is specified in `$HOME/.phet/build-local.json`. Describing or identifying the entries 
 in `build-local.json` is beyond the scope of this document; ask a PhET developer for help in setting up this file. At 
 a minimum you will need `devUsername` and `buildServerAuthorizationCode`.
 
 Run `grunt --help` for a list of build tasks and their options. Values specified on the `grunt` command line typically override values specified in `build-local.json`.
 
 (Optional) Create an ssh key if you'd like to avoid entering your password for dev-related build tasks:
 
 - create an rsa key in ~/.ssh (run "ssh-keygen -t rsa" to generate a key if you don't already have one).
 - add an entry for spot in ~/.ssh/config like so (you may need to create this file):
 
 ```
 Host spot
    HostName spot.colorado.edu
    User [identikey]
    Port 22
    IdentityFile ~/.ssh/id_rsa
 ```
 - On spot, you'll need to add your public key (found in ~/.ssh/id_rsa.pub) to a file ~/.ssh/authorized_keys
 - Change the permissions of the file so it is not group writable: `chmod g-w authorized_keys`
 
 #### Variables to replace in the instructions below:
 
 ```
 $SIM = the name of your sim's repo
 $VERSION = the identifier of your sim, eg "1.0.0-rc.2"
 $HOME = your home directory
 ```
 
#### Latest SHAs: 
Keep in mind these SHAs may not include all of the repos for your sim, but you can still overwrite your 
dependencies with them, and the rest will be filled in with master during the build.

The latest fully-tested SHAs (use these if appropriate): 
http://www.colorado.edu/physics/phet/dev/html/unit-rates/1.0.0/dependencies.json

The latest SHAs under testing (use these if appropriate): 
http://www.colorado.edu/physics/phet/dev/html/graphing-slope-intercept/1.0.0-rc.1/dependencies.json


## Step 1. Set up the codebase
* **DEV**: Dev deploys are often made from master using `pull-all.sh` in `chipper/bin`, but you can use code from branches if you wish 
* **RC_FIRST**: 
    + **PHET_IO:**: Add `-phetio` to the end of the branch name.
    + Create a branch with MAJOR.MINOR matching the sim to be published, such as 1.2.  For instance: `git checkout -b 1.2` 
* **RC_SUBSEQUENT | PRODUCTION**: 
    + Checkout the branch with MAJOR.MINOR (**PHET_IO** branches will end with `-phetio`). If a branch does not exist for your 
    version, make, following the step above, like you are publishing the first rc.
    + If you are using the trusted SHAs from above, copy them into the top level `dependencies.json`
    + `grunt checkout-shas` to checkout any supporting branches from other repos. 
    + If checkout-shas didn't already do so: `npm prune` and `npm update` in the sim repo and in chipper.
    `rm -rf node_modules` and `npm install` in that directory instead.
    + **Maintenance Release**:  If you needed to branch any dependency repositories for the purposes of patching, name the branches
       after the sim and version you are performing the maintenance release on. For example, if you branched vegas for the 1.1 
       release of graphing-lines, the branch name in vegas will be graphing-lines-1.1.

## Step 2. Update the version number in package.json
Use version names of the following form: 
* **DEV**: The version number should contain -dev, such as "1.0.0-dev.2". 
* **RC**: The version number should contain -rc, such as "1.0.0-rc.2" 
* **PRODUCTION**: "1.0.1"
* **PHET_IO**: use the patterns above and the build process will automatically append "-phetio" into the version name
* Commit & push to Github.

## Step 3. Build the simulation with chipper
* **PHET_BRAND**: `grunt`
* **PHET_IO**: `grunt --brand=phet-io`

## Step 4. Test the built version locally
* For version numbers 1.0.0 and higher without suffixes, an update check failure message appears in the console. This is 
expected for local viewing, and should not appear when the sim is published on the PhET Website
* **PHET_BRAND**: Launch the simulation and make sure it behaves properly
* **PHET_IO**: Launch the wrappers page `wrappers/index` and test all the links

## Step 5. Deploy the tested version
* **PHET_IO**: add `--brand=phet-io` to the end of the command. 
* **DEV**: 
    + **FIRST TIME**: `grunt deploy-dev --mkdir` (requires 2 password inputs or ssh key)
    + **SECOND OR LATER**: `grunt deploy-dev`
* **RC**: `grunt deploy-rc` RC versions are deployed to spot.colorado.edu at http://www.colorado.edu/physics/phet/dev/html/
* **PRODUCTION**: 
This will instruct the build server to build the English version of 
the simulation as well as all currently deployed translated versions and deploy them on the web site.  This will also deploy 
the locally built version to the dev server.
    + Generally: `grunt deploy-production`
    + **NOTE**: If you're using a version of chipper that is from _**Nov 9, 2015**_ or earlier, add `--locales=*`.
    + For ph-scale and ph-scale-basics, ignore the above 'Note' and always use `grunt deploy-production`.
     See https://github.com/phetsims/phet-info/issues/10 for details.

## Step 6. Test the deployed version
* If the build server is having issues, you can ssh into phet and look at the build-server logs with: `sudo journalctl -fu build-server`. 
* **DEV | RC**: Versions are deployed to spot.colorado.edu at http://www.colorado.edu/physics/phet/dev/html/
* **PRODUCTION**: Versions are deployed to https://phet.colorado.edu/sims/html/$SIM/latest/$SIM_en.html
* **PHET_IO**: Versions are deployed to phet-io.colorado.edu at: https://phet-io.colorado.edu/sims/$SIM/$VERSION/wrappers/index/ 
  and should be password protected.  Verify that your password works.
* Run Step 4, but for the published version

## Step 7. Post-publication steps
* **PRODUCTION FOR PHET_BRAND**: 
    + **NEW_SIM**: Both the simulation and project will need to marked "visible" in the website admin interface.
        Usually the person in charge of uploading all of the meta information will be responsible for doing this. After that,
        make sure the sim page appears correctly on the website. Talk to @jonathanolson or @jbphet if it has not appeared after marking the sim and project visible.
      - When viewing the website you may encounter stale content due to the varnish cache.  There are two ways to avoid this:
        - To check a small number of issues, add a unique parameter to the end of every query. You must change it every time you 
          refresh the url. Example: `http://phet.colorado.edu/sims/html/example-sim/latest/example-sim_en.html?test-parameter1`
        - To avoid the cache permanently, you need to add a cookie with the name `NO-CACHE` and with an arbitrary or 
          empty value. Cookie usage cannot be covered in entirety here. To use cookies with `curl` 
          see [this answer](http://stackoverflow.com/a/7186160/2496827). To add custom cookies in 
          Chrome [see this solution](http://superuser.com/a/636697/493443).
   + **INITIAL_PUBLICATION**: Generate and check in (on the master branch) the auto-generated readme file for a published sim.  The README.md file can be created using ```grunt published-README```.
   + **NOT_A_NEW_SIMULATION**: Verify that any previously existing translations are still available and that
        their version numbers are correct.
   + After the new simulation is available from the website, the 3rd party contributions page must be updated.
    Directions for how to do this are in `chipper/js/grunt/reportThirdParty.js`. 
* **PRODUCTION FOR PHET_IO_BRAND**:
   + If this is a version that will be used with students, then make sure to remove the password protection. See https://github.com/phetsims/phet-io/blob/master/doc/phetio-security.md for details.
   + Make sure that the current level of instrumentation is represented here in the [Instrumentation Status Spreadsheet](https://docs.google.com/spreadsheets/d/1pU9izdNQkd9vr8TvLAfXe_v68yh-7potH-y712FBPr8/edit#gid=0). MAKE SURE TO UPDATE THE "Latest Published Version" COLUMN.
* **RC | PRODUCTION**: Update the "latest SHAs under testing" above, if appropriate.  **NOTE**: Keep in mind that not all sims use all repos.

## Step 8. Restore your working copy
* Check out master for dependencies: `grunt checkout-master`
* Run again to prune and update node modules: `grunt checkout-master`, **Skip This Step** if you are using a chipper sha that is newer than Jan 24th, 2017.
* Check out master for the sim repo: `git checkout master`
  
  
## Deploy a batch of production sims.
These steps were followed by @samreid on Nov 2, 2016 to roll out a batch of PhET-iO sims to master.

1. Setup: 
  * `pull-all.sh`, we will use same master (without pulling) to deploy all.  Do not pull between the other steps.

2. Publish:
  * checkout branch for sim.
  * merge master to it.
  * update version number + commit + push.
  * make sure version is not already published on phet-io site.
  ```
  grunt --brand=phet-io
  cp build/dependencies.json dependencies.json
  git commit -am "updated dependencies.json"
  git push
  grunt deploy-production --brand=phet-io
  ```

3. Cleanup:
  * review `dependencies.json` and make sure they match.
  * update version in master.
