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

## Publishing a 'dev' (development) version (PhET-iO brand)

Dev versions are deployed to spot.colorado.edu at http://www.colorado.edu/physics/phet/dev/html/

- [ ] Run `pull-all.sh` in chipper/bin
- [ ] Update the version identifier in package.json. The identifier should contain "phetiodev", e.g. "1.1.0-phetiodev.3".
- [ ] Commit & push.
- [ ] Run the build process: `grunt --brand=phet-io`
- [ ] Test locally before transferring the file to spot. Test wrappers such as the instance-proxies wrapper, and use ?launchLocalVersion so it will use
 relative path instead of looking on phet-io.colorado.edu
- [ ] Deploy to spot
 * First time this sim is deployed: `grunt deploy-dev --mkdir` (requires 2 password inputs or ssh key)
 * Second or later deployment: `grunt deploy-dev`

## PhET-iO Testing after deployment

To test PhET-iO branded simulations:
- [ ] Try launching the wrappers page `wrappers/index`.  This should be password protected.  Verify that your password works.
- [ ] Test the screenshot and instance-proxies wrappers.  If it is a dev or rc version, use ?launchLocalVersion
- [ ] Try launching the phet-io sim, for example: `sim-name_en-phetio.html?phet-io.standalone`.
- [ ] When testing on phet-server the location of the sim will be: https://phet-io.colorado.edu/sims/$SIM/$VERSION/wrappers/index
