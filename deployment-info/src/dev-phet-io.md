
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
