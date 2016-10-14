
## Publishing a public version (PhET brand)

Public versions are deployed to phet-server.int.colorado.edu at http://phet.colorado.edu.
By default, publishing a public version also deploys a dev version.

To publish a public version:

- [ ] Update (if needed) or create a screenshot that is 2048x1344.  Generally this is done by taking a screenshot on an iPad 3 or higher (since it has the retina display) with multiple tabs open, then crop the chrome off of it to 2048x1342, then pad the top with 2
pixels of the sim's background color (to 2048x1344) and save as /assets/$SIM-screenshot.png.  Eventually, quick and easy
creation of this screen shot will be supported through the screenshot feature from the PhET menu, but as of this writing
this support doesn't exist.
- [ ] A public version is generally based on some rc version, which generally comes from an rc branch.  Make sure you're
working from that branch, and then update the version identifier to the form "major.minor.maintenance", removing any
"-rc.x" portion if present. For example, if the published version is based on "1.1.0-rc.4", then the published version
identifier will be "1.1.0".  Make sure this is committed and pushed.
- [ ] Check out the correct SHAs using `grunt checkout-shas`.
- [ ] Run `grunt` to build a local version and sanity test it. (Note that for version numbers 1.0.0 and higher without suffixes, an update check failure message appears in the console. This is expected for local viewing, and will not appear when the sim goes online.)
- [ ] Run `grunt deploy-production --locales=*` (or just `grunt deploy-production` for ph-scale and ph-scale-basics, see https://github.com/phetsims/phet-info/issues/10).  This will instruct the build server to build the English version of the
simulation as well as all currently deployed translated versions and deploy them on the web site.  This will also deploy
the locally built version to the dev server.  (Note: If you're sure that the version of chipper that is being used is
from Nov 10 2015 or later, the `--locales=*` flag can be omitted.)
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
