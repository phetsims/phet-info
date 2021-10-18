Updating metadata
=============

If you make a change to any of the following, the single sim (or all sims) will need updates:

- Preloads (build.json)
- Dependencies (build.json or sim-specific phetLibs in package.json)
- Package.json changes that affect what files should be generated (unit tests/colors/a11y/etc.)

For anything that could potentially change checked-in top-level sim HTML or config files, the following should be done:

- [ ] `perennial/bin/for-each.sh active-repos npm prune`
- [ ] `perennial/bin/for-each.sh active-repos npm update`
- [ ] `perennial/bin/for-each.sh active-repos grunt update` (or run `grunt update` in affected repos)
- [ ] If possible, run local aqua testing (`/aqua/test-server/test-sims.html?ea&audio=disabled&testDuration=10000&testConcurrentBuilds=4&brand=phet&fuzz`) to make sure nothing broke horribly.
- [ ] `git add` the relevant files, `git commit`  (referencing the issue for the change) and `git push`.

Note that for package.json changes that add flags, an automated process on bayes should update the perennial/data/ files automatically.
