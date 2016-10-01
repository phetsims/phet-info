 **Simulation Deployment Guidelines**
=====================================

Variables to replace in the instructions below:

```
$SIM = the name of your sim's repo
$VERSION = the identifier of your sim, eg "1.0.0-rc.2"
$USERNAME = your username on spot, figaro, and phet-server
$HOME = your home directory
```

**Build process configuration**

Before building or deploying a simulation, familiarize yourself with configuration options for PhET's build process.

Your default build configuration is specified in `$HOME/.phet/build-local.json`. Describing or identifying the entries in `build-local.json` is beyond the scope of this document; ask a PhET developer for help in setting up this file. At a minimum you will need `devUsername` and `buildServerAuthorizationCode`.

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

**Steps to publish a 'dev' (development) version**

Dev versions are deployed to spot.colorado.edu at http://www.colorado.edu/physics/phet/dev/html/.

To deploy to dev version:

- [ ] Are your PhET repos up to date? Run pull-all.sh in chipper/bin if not.
- [ ] Update the version identifier in package.json.
 * For PhET Brand, the identifier should contain "dev", e.g. "1.0.0-dev.2".
 * For PhET-iO, the identifier should contain "phetiodev", e.g. "1.1.0-phetiodev.3".
- [ ] Commit & push.
- [ ] Run the build process: `grunt`
 * For PhET-iO, instead use `grunt --brand=phet-io`
- [ ] Open the generated HTML file locally and interact with it to check that all is well.
 * For PhET-iO, test wrappers such as the instance-proxies wrapper, and use ?launchLocalVersion so it will use relative path instead of looking on phet-io.colorado.edu
- [ ] If this is the first time you've deployed anything for this sim, deploy with `grunt deploy-dev --mkdir` (requires 2 password inputs if ssh key is not set up). Otherwise just use `grunt deploy-dev`

**Steps to publish a 'rc' (release candidate) version**

The latest fully-tested SHAs (use these if appropriate): https://github.com/phetsims/atomic-interactions/blob/1.0/dependencies.json

The latest SHAs under testing (use these if appropriate): https://github.com/phetsims/forces-and-motion-basics/blob/2.1/dependencies.json

RC versions are deployed to spot.colorado.edu at http://www.colorado.edu/physics/phet/dev/html/.

If this is the first release candidate on a release branch:

- [ ] Create a release branch and switch to it, e.g.: `git checkout -b 1.0`. Release branches are named using major and minor version numbers, eg "1.0".
 * for PhET-iO the branch name should include "phetio", such as "1.1-phetio"
- [ ] Update the version identifier in package.json. The first rc version should have suffix "rc.1", eg "1.0.0-rc.1".
 * for PhET-iO, the version name should include "phetiorc" instead of "rc"
- [ ] Commit & push.
- [ ] Run the build process: `grunt`
 * for PhET-iO instead use `grunt --brand=phet-io`
- [ ] Deploy to the server: `grunt deploy-rc` to deploy the rc using the build server.
- [ ] After following these steps, please update the "Other SHAs under testing" above, if appropriate.

If this is not the first release candidate on a release branch:

- [ ] Check out the release branch, e.g.: `git checkout 1.0`
- [ ] Check out the correct shas for dependencies: `grunt checkout-shas`
- [ ] If you've branched (for the purposes of patching) any of the dependency repositories since the last rc version was published, you'll need to explicitly checkout those branches. For example, if you branched vegas for the 1.1 release of graphing-lines, do `cd ../vegas ; git checkout graphing-lines-1.1`.
- [ ] Update the version identifier in package.json. The identifier should contain "rc", e.g. "1.0.0-rc.2". Commit & push.
 * for PhET-iO the identifier should include "phetiorc"
- [ ] Run the build process: `grunt`
 * for PhET-iO use instead `grunt --brand=phet-io`
- [ ] Deploy to the server: `grunt deploy-rc` to deploy the rc version using the build-server.
- [ ] Check out master for dependencies: `grunt checkout-master` (optional)
- [ ] After following these steps, please update the "latest SHAs under testing" link above, if appropriate.

**Steps to publish a public version**

Public versions are deployed to phet-server.int.colorado.edu at http://phet.colorado.edu.
By default, publishing a public version also deploys a dev version.

To publish a public version:

- [ ] Update (if needed) or create a screenshot that is 2048x1344.  Generally this is done by taking a screenshot on an iPad 3 or higher (since it has the retina display) with multiple tabs open, then crop the chrome off of it to 2048x1342, then pad the top with 2
pixels of the sim's background color (to 2048x1344) and save as /assets/$SIM-screenshot.png.  Eventually, quick and easy
creation of this screen shot will be supported through the screenshot feature from the PhET menu, but as of this writing
this support doesn't exist.
 * for PhET-iO this step is not necessary
- [ ] A public version is generally based on some rc version, which generally comes from an rc branch.  Make sure you're
working from that branch, and then update the version identifier to the form "major.minor.maintenance", removing any
"-rc.x" portion if present. For example, if the published version is based on "1.1.0-rc.4", then the published version
identifier will be "1.1.0".  Make sure this is committed and pushed.
 * for PhET-iO the version should include "-phetio", such as "1.1.0-phetio"
- [ ] Check out the correct SHAs using `grunt checkout-shas`.
- [ ] Run `grunt` to build a local version and sanity test it. (Note that for version numbers 1.0.0 and higher without suffixes, an update check failure message appears in the console. This is expected for local viewing, and will not appear when the sim goes online.)
 * for PhET-iO use `grunt --brand=phet-io`
- [ ] Run `grunt deploy-production --locales=*` (or just `grunt deploy-production` for ph-scale and ph-scale-basics, see https://github.com/phetsims/phet-info/issues/10).  This will instruct the build server to build the English version of the
simulation as well as all currently deployed translated versions and deploy them on the web site.  This will also deploy
the locally built version to the dev server.  (Note: If you're sure that the version of chipper that is being used is
from Nov 10 2015 or later, the `--locales=*` flag can be omitted.)
* Following steps are for PhET brand only (not PhET-iO).  Instead for PhET-iO please test the deployed version.
- [ ] Wait a few minutes for the build server to do its thing, and then test: http://phet.colorado.edu/sims/html/$SIM/latest/$SIM_en.html
- [ ] If this is a new sim, both the simulation and project will need to marked "visible" in the website admin interface.
Usually the person in charge of uploading all of the meta information will be responsible for doing this. After that,
make sure the sim page appears correctly on the website. Talk to @jonathanolson or @jbphet if it hasn't appeared after marking the
sim and project visible.
  - When viewing the website you may encounter stale content due to the varnish cache.  There are two ways to avoid this.  
    - To check a small number of issues, add a unique parameter to the end of every query. You must change it every time you refresh the url. Example: `http://phet.colorado.edu/sims/html/example-sim/latest/example-sim_en.html?test-parameter1`
    - To avoid the cache permanently, you need to add a cookie with the name `NO-CACHE` and with an arbitrary or empty value.   Cookie usage cannot be covered in entirety here.  To use cookies with `curl` see [this answer](http://stackoverflow.com/a/7186160/2496827).  To add custom cookies in Chrome [see this solution](http://superuser.com/a/636697/493443)
- [ ] If this is the initial publication, generate and check in (on the master branch) the auto-generated readme file for a
published sim.  The README.md file can be created using ```grunt published-README```.
- [ ] If this is *not* a new simulation, verify that any previously existing translations are still available and that
their version numbers are correct.
- [ ] Update the "Latest fully tested SHAs" above.
- [ ] After the new simulation is available from the website, the 3rd party contributions page must be updated.  Directions
for how to do this are in reportThirdParty.js.

## PhET-iO Testing after deployment

These instructions above show how to deploy PhET or PhET-iO branded simulations.  To test PhET-iO branded simulations:
- [ ] Check that all files were deployed properly to spot for rc or spot and phet-server for production. At a minimum check:
    - Try launching the wrappers page `protected/index.html`.  This should be password protected.  Verify that your password works.
    - Test the screenshot and instance-proxies wrappers.  If it is a dev or rc version, use ?launchLocalVersion
    - Try launching the phet-io sim, for example: `sim-name_en-phetio.html?phet-io.standalone=true`.
