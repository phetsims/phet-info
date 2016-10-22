
## Publishing a public PhET-iO version

Public versions are deployed to phet-server.int.colorado.edu at http://phet-io.colorado.edu.
By default, publishing a public version also deploys a dev version.

To publish a public version:

- [ ] A public version is generally based on some rc version, which generally comes from an rc branch.  Make sure you're working from that branch, and then update the version identifier to the form "major.minor.maintenance", removing any "-rc.x" portion if present. For example, if the published version is based on "1.1.0-rc.4", then the published version identifier will be "1.1.0-phetio".  Make sure this is committed and pushed.
- [ ] Check out the correct SHAs using `grunt checkout-shas`. Note that this is a different set of trusted shas from the phet-branded version.
- [ ] Run `grunt --brand=phet-io` to build a local version and sanity test it. (Note that for version numbers 1.0.0 and higher without suffixes, an update check failure message appears in the console. This is expected for local viewing, and will not appear when the sim goes online.)
- [ ] Run `grunt deploy-production --brand=phet-io --locales=*` (or just `grunt deploy-production --brand=phet-io` for ph-scale and ph-scale-basics, see https://github.com/phetsims/phet-info/issues/10).  This will instruct the build server to build the English version of the
simulation as well as all currently deployed translated versions and deploy them on the web site.  This will also deploy
the locally built version to the dev server.  (Note: If you're sure that the version of chipper that is being used is
from Nov 10 2015 or later, the `--locales=*` flag can be omitted.)
