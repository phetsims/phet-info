Updating metadata
=============

For anything that could potentially change checked-in top-level sim HTML or config files, the following should be done:

- [ ] `perennial/bin/for-each.sh active-repos npm prune`
- [ ] `perennial/bin/for-each.sh active-repos npm update`
- [ ] `perennial/bin/for-each.sh active-repos grunt update` (or run `grunt update` in affected repos)
- [ ] If possible, run local aqua testing (`/aqua/test-server/test-sims.html?ea&audioVolume=0&testDuration=10000&testConcurrentBuilds=4&brand=phet&fuzzMouse`) to make sure nothing broke horribly.
- [ ] git add the relevant files, commit (referencing the issue for the change) and push.

This should be done for any changes to:

- Preloads (build.json)
- Dependencies (build.json or sim-specific phetLibs in package.json)
- Package.json changes that affect what files should be generated (unit tests/colors/a11y/etc.)

Note that for package.json changes that add flags, an automated process on bayes should update the perennial/data files automatically.
