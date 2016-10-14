
# Steps to publish a 'dev' (development) version (PhET brand)

Dev versions are deployed to spot.colorado.edu at http://www.colorado.edu/physics/phet/dev/html/

- [ ] Run `pull-all.sh` in chipper/bin
- [ ] Update the version identifier in package.json. The identifier should contain "dev", e.g. "1.0.0-dev.2".
- [ ] Commit & push.
- [ ] Run the build process: `grunt`
- [ ] Test locally before transferring the file to spot. Open the generated HTML file locally and interact with it to check that all is well.
- [ ] Deploy to spot
 * First time this sim is deployed: `grunt deploy-dev --mkdir` (requires 2 password inputs or ssh key)
 * Second or later deployment: `grunt deploy-dev`
