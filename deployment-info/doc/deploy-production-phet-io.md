Variables to replace in the instructions below:

```
$SIM = the name of your sim's repo
$VERSION = the identifier of your sim, eg "1.0.0-rc.2"
$HOME = your home directory
```


## Build process configuration

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

## Publishing a PhET-iO version for production

Production versions are deployed to phet-server.int.colorado.edu at http://phet-io.colorado.edu.
By default, publishing a production version also deploys a dev version.

To publish a production version:

- [ ] A production version is generally based on some rc version, which generally comes from an rc branch.  Make sure you're working from that branch, and then update the version identifier to the form "major.minor.maintenance", removing any "-rc.x" portion if present. For example, if the published version is based on "1.1.0-rc.4", then the published version identifier will be "1.1.0".  Make sure this is committed and pushed.
- [ ] Check out the correct SHAs using `grunt checkout-shas`. Note that this is a different set of trusted shas from the phet-branded version. To build from master (or other current working branches) on all repos, skip this step.
- [ ] Run `grunt --brand=phet-io` to build a local version. To test locally, use the steps in "PhET-iO Testing after deployment" for guidance. (Note that for version numbers 1.0.0 and higher without suffixes, an update check failure message appears in the console. This is expected for local viewing, and will not appear when the sim goes online.)
- [ ] Run `grunt deploy-production --brand=phet-io --locales=*` (or just `grunt deploy-production --brand=phet-io` for ph-scale and ph-scale-basics, see https://github.com/phetsims/phet-info/issues/10).  This will instruct the build server to build the English version of the simulation as well as all currently deployed translated versions and deploy them on the web site.  This will also deploy the locally built version to the dev server.  (Note: If you're sure that the version of chipper that is being used is from Nov 10 2015 or later, the `--locales=*` flag can be omitted.)

### Steps followed by @samreid on Nov 2, 2016 to deploy a batch of production sims

Steps to roll out a batch of PhET-iO sims to master
(a) pull-all.sh, we will use same master (without pulling) to deploy all.  Do not pull between the other steps.

(b)
checkout branch for sim
merge master to it
update version number + commit + push
make sure version is not already published on phet-io site

grunt --brand=phet-io
cp build/dependencies.json dependencies.json
git commit -am "updated dependencies.json"
git push
grunt deploy-production --brand=phet-io


(c)
review dependencies.json and make sure they match
update version in master
## PhET-iO Testing after deployment

To test PhET-iO branded simulations:
- [ ] Try launching the wrappers page `wrappers/index`.  This should be password protected.  Verify that your password works.
- [ ] Test the screenshot and instance-proxies wrappers.  If it is a dev or rc version, use ?launchLocalVersion
- [ ] Try launching the phet-io sim, for example: `sim-name_en-phetio.html?phet-io.standalone`.
- [ ] When testing on phet-server the location of the sim will be: https://phet-io.colorado.edu/sims/$SIM/$VERSION/wrappers/index/
