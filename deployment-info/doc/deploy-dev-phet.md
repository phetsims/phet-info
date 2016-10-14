Variables to replace in the instructions below:

```
$SIM = the name of your sim's repo
$VERSION = the identifier of your sim, eg "1.0.0-rc.2"
$USERNAME = your username on spot, figaro, and phet-server
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

## Publishing a 'dev' (development) version (PhET brand)

Dev versions are deployed to spot.colorado.edu at http://www.colorado.edu/physics/phet/dev/html/

- [ ] Run `pull-all.sh` in chipper/bin
- [ ] Update the version identifier in package.json. The identifier should contain "dev", e.g. "1.0.0-dev.2".
- [ ] Commit & push.
- [ ] Run the build process: `grunt`
- [ ] Test locally before transferring the file to spot. Open the generated HTML file locally and interact with it to check that all is well.
- [ ] Deploy to spot
 * First time this sim is deployed: `grunt deploy-dev --mkdir` (requires 2 password inputs or ssh key)
 * Second or later deployment: `grunt deploy-dev`
