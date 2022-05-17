# Deploying a PhET Simulation

#### Variables to replace in the instructions below:
 
 ```
 {{SIM}} = the name of your sim's repo
 {{VERSION}} = the version identifier of your sim, eg "1.0.0-rc.2"
 {{IDENTIKEY}} = your CU IdentiKey login name
 ```
 
## Before Beginning.

#### Don't use chipper 1.0 tools unless you have to
Chipper 1.0 tools may not work because old chipper SHAs still have code that points to spot, a decommissioned server.
See https://github.com/phetsims/chipper/issues/1248.

If you got an error from using chipper 2.0 tools like ```chipper 0.0.0 cannot build multiple brands at a time```
try using chipper 2.0 steps but just building and deploying each brand separately before moving on to chipper-1.0.

#### Configure the build process
                     
 Before building or deploying a simulation, familiarize yourself with configuration options for PhET's build process.
 
 Your default build configuration is specified in `~/.phet/build-local.json`. Describing or identifying the entries 
 in `build-local.json` is beyond the scope of this document; ask a PhET developer for help in setting up this file. At 
 a minimum you will need `devUsername` and `buildServerAuthorizationCode`. A few handy keys:
* `buildServerNotifyEmail`: add your email to be notified on the success or failure of your builds to the build server.
* `brand:phet` to automatically build the phet brand instead of the adapted-from-phet brand.

 Run `grunt --help` for a list of build tasks and their options. Values specified on the `grunt` command line typically override values specified in `build-local.json`.
 
#### Configure an RSA key 

Configure an RSA key, or you will be prompted multiple times for a password during dev-related build tasks.
 
 - If you don't already have an RSA key, generate one by running `ssh-keygen -t rsa`.
 - Add an entry for spot in `localhost@~/.ssh/config` using this template:
 
 ```
 Host spot
    HostName spot.colorado.edu
    User {{IDENTIKEY}}
    Port 22
    IdentityFile ~/.ssh/id_rsa
 ```
 - Add your public key (found in `localhost@~/.ssh/id_rsa.pub`) to `spot@~/.ssh/authorized_keys`
 - Change the permissions of `authorized_keys` so it is not group writable: `chmod g-w authorized_keys`

## Shortcut for dev deployment:
If you are working in master, would like to release a dev version by updating the dev number, and your working copy is clean then you can use `grunt deploy-next-dev`. This will run a trial build and if there are any lint or build errors the process will halt. If there are no lint or build errors, package.json will be updated with the next version number and the simulation will be built and deployed.

## Step 1. Set up the codebase
* **DEV**: Dev deploys are often made from master using `pull-all.sh` in `perennial/bin`, but you can use code from branches if you wish
* **RC_FIRST**: 
    + **PHET_IO:**: Add `-phetio` to the end of the branch name.
    + Create a branch with MAJOR.MINOR matching the sim to be published, such as 1.2.  For instance: `git checkout -b 1.2`
    + Update the version id in package.json for master. Master should be set up for what 
would be the _next_ release branch name.  So if you just created release branch 1.3, then the version should be "1.4.0-dev.0" in master. (Note the "0" for the dev number, so that `grunt bump-version` works properly.)
* **RC_SUBSEQUENT | PRODUCTION**: 
    + Checkout the branch with MAJOR.MINOR (**PHET_IO** branches will end with `-phetio`). If a branch does not exist for your 
    version, make, following the step above, like you are publishing the first rc.
    + `grunt checkout-shas` to checkout any supporting branches from other repos. 
    + If checkout-shas didn't already do so: `npm prune` and `npm update` in the sim repo and in chipper.
    `rm -rf node_modules` and `npm install` in that directory instead.
    + **Maintenance Release**:  If you needed to branch any dependency repositories for the purposes of patching, name the branches
       after the sim and version you are performing the maintenance release on. For example, running `git checkout -b graphing-lines-1.1` in the vegas repository will branch vegas for use by the graphing-lines 1.1 branch. 
    + **Maintenance Release**:  After the commits have been made, update the top level `dependencies.json` to reflect the new shas and          branches of the maintenance release. When you deploy, this step should be done automatically. This top level `dependencies.json`
       is only important for checking out shas.
    + **Maintenance Release**:  If there is a parallel brand that has the same minor number as your branch (i.e. 1.3 and 1.3-phetio), it
       means that these branches should have the same shas (not always true in practice, but mostly accurate, so check your shas). Make 
       sure that all of your commits are cherry-picked onto that branch too (if they apply), so that the branches stay in sync. 
* **PRODUCTION**: Update the QA credits before continuing.
* **PHET PRODUCTION_FIRST**: Complete the simulation master checklist (beyond the scope of this document). Notably, this 
      includes adding a screenshot so that thumbnails and the twitter card are properly generated in the initial deployment.
* **ALL RC and PRODUCTION**: please see https://github.com/phetsims/chipper/issues/587 for a description of branch names and 
      how to keep phet and phet-io branch names in sync  

## Step 2. Update the version number in package.json
Use version names of the following form: 
* **DEV**: The version number should contain -dev, such as "1.0.0-dev.2". 
* **RC**: The version number should contain -rc, such as "1.0.0-rc.2" 
* **PRODUCTION**: "1.0.1"
* **PHET_IO**: use the patterns above and the build process will automatically insert "phetio" into the version name.  
For instance, 2.1.7-phetiodev.3, 2.1.6-phetiorc.4 or 2.2.3-phetio.
* Commit & push to Github.

## Step 3. Build the simulation with chipper
* **PHET_BRAND**: `grunt`
* **PHET_IO**: `grunt --brand=phet-io`

## Step 4. Test the built version locally
* For version numbers 1.0.0 and higher without suffixes, an update check failure message appears in the console. This is 
expected for local viewing, and should not appear when the sim is published on the PhET Website
* **PHET_BRAND**: Test {{SIM}}/build/{{SIM}}_en.html.
* **PHET_IO**: Navigate to {{SIM}}/build/wrappers/index and test all of the links.

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
* **PRODUCTION**: 
    + **PHET**: Versions are deployed to https://phet.colorado.edu/sims/html/{{SIM}}/latest/{{SIM}}_en.html
    + **PHET_IO**: Versions are deployed to phet-io.colorado.edu at: https://phet-io.colorado.edu/sims/{{SIM}}/{{VERSION}}/.
* **PHET_IO**: 
    + Test using the wrapper index, located at {{SIM}}/{{VERSION}}/wrappers/index. 
    + You will need a password. Verify that your password works.
* Run Step 4, but for the published version. NOTE: A username and password are required to test deployed wrappers 
for phet-io versions. Ask a PhET developer for credentials.

## Step 7. Post-publication steps
* **PRODUCTION FOR PHET_BRAND**: 
    + **NEW_SIM**: Both the simulation and project will need to marked "visible" in the website admin interface.
        Usually the person in charge of uploading all of the meta information will be responsible for doing this. After that,
        make sure the sim page appears correctly on the website. Talk to @jonathanolson or @jbphet if it has not appeared after marking the sim and project visible.
      - When viewing the website you may encounter stale content due to the varnish cache.  There are two ways to avoid this:
        - To check a small number of issues, add a unique parameter to the end of every query. You must change it every time you 
          refresh the url. Example: `https://phet.colorado.edu/sims/html/example-sim/latest/example-sim_en.html?test-parameter1`
        - To avoid the cache permanently, you need to add a cookie with the name `NO-CACHE` and with an arbitrary or 
          empty value. Cookie usage cannot be covered in entirety here. To use cookies with `curl` 
          see [this answer](http://stackoverflow.com/a/7186160/2496827). To add custom cookies in 
          Chrome [see this solution](http://superuser.com/a/636697/493443).
   + **INITIAL_PUBLICATION**: Generate and check in (on the master branch) the auto-generated readme file for a published sim.  The README.md file can be created using ```grunt published-README```.
   + **NOT_A_NEW_SIMULATION**: Verify that any previously existing translations are still available and that
        their version numbers are correct. 
* **PRODUCTION FOR PHET_IO_BRAND**:
   + If this is a version that will be used with students, then make sure to remove the password protection. See https://github.com/phetsims/phet-io/blob/master/doc/phet-io-security.md for details.
   + Make sure that the current level of instrumentation is represented here in the [Instrumentation Status Spreadsheet](https://docs.google.com/spreadsheets/d/1pU9izdNQkd9vr8TvLAfXe_v68yh-7potH-y712FBPr8/edit#gid=0). MAKE SURE TO UPDATE THE "Latest Published Version" COLUMN.
   + If you are delivering this to a partner, update [partners.md](https://github.com/phetsims/phet-io/blob/master/doc/partners.md) to show this delivery. Read the intro of the document to make sure that you format the entry correctly.

## Step 8. Restore your working copy
* Check out master for dependencies: `grunt checkout-master`
* Run again to prune and update node modules: `grunt checkout-master`, **Skip This Step** if you are using a chipper sha that is newer than Jan 24th, 2017.
* Check out master for the sim repo: `git checkout master`
* Run `npm update` in chipper.
* Run `perennial/bin/status.sh` as a sanity check.
  
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
