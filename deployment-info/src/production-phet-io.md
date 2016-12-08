
## Publishing a PhET-iO version for production

Production versions are deployed to phet-server.int.colorado.edu at http://phet-io.colorado.edu.
By default, publishing a production version also deploys a dev version.

To publish a production version:

- [ ] A production version is generally based on some rc version, which comes from an rc branch.  Make sure you're working from that branch. If a branch doesn't exist for your major.minor-phetio version, go to phet-io-rc and create one.
- [ ] Update the version identifier to the form "major.minor.maintenance", removing any "-rc.x" portion if present. For example, if the published version is based on "1.1.0-rc.4", then the published version identifier will be "1.1.0".  Make sure this is committed and pushed.
- [ ] Check out the correct SHAs using `grunt checkout-shas`. Note that this is a different set of trusted shas from the phet-branded version. To build from master (or other current working branches) on all repos, skip this step.
- [ ] Run `grunt --brand=phet-io` to build a local version. To test locally, use the steps in "PhET-iO Testing after deployment" for guidance. (Note that for version numbers 1.0.0 and higher without suffixes, an update check failure message appears in the console. This is expected for local viewing, and will not appear when the sim goes online.)
- [ ] Run `grunt deploy-production --brand=phet-io --locales=*` (or just `grunt deploy-production --brand=phet-io` for ph-scale and ph-scale-basics, see https://github.com/phetsims/phet-info/issues/10).  This will instruct the build server to build the English version of the simulation as well as all currently deployed translated versions and deploy them on the web site.  This will also deploy the locally built version to the dev server.  (Note: If you're sure that the version of chipper that is being used is from Nov 10 2015 or later, the `--locales=*` flag can be omitted.)
- [ ] If this is a version that will be used with students, then make sure to remove the password protection. See https://github.com/phetsims/phet-io/blob/master/doc/managing-passwords.md for details.

### Steps followed by @samreid on Nov 2, 2016 to deploy a batch of production sims

Steps to roll out a batch of PhET-iO sims to master
(a) pull-all.sh, we will use same master (without pulling) to deploy all.  Do not pull between the other steps.

(b)
* checkout branch for sim
* merge master to it
* update version number + commit + push
* make sure version is not already published on phet-io site

```
grunt --brand=phet-io
cp build/dependencies.json dependencies.json
git commit -am "updated dependencies.json"
git push
grunt deploy-production --brand=phet-io
```

(c)
* review dependencies.json and make sure they match
* update version in master
