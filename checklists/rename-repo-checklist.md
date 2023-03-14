# Rename Repo Checklist

## Steps for renaming a repo
- [ ] Make sure all commits are pushed to that repo.
- [ ] On Github.com, go to repo -> Settings -> Options -> "Repository name"  and rename.
- [ ] Rename in `perennial/data/active-repos` and any other perennial data files it occurs in, like `active-runnables`, `active-sims`, `phet-io`, etc. Push the change to perennial and then pull perennial-alias.
- [ ] Delete the old repo
- [ ] Run `perennial/bin/clone-missting/repos.sh`.
- [ ] Update `package.json` accordingly. Including but not necessarily limited to:
  * `name`
  * `repository.url`
  * `phet.requirejsNamespace`
- [ ] Change entry in [responsible_dev.json](https://github.com/phetsims/phet-info/blob/master/sim-info/responsible_dev.json).
- [ ] If applicable, "refresh perennial" on phettest.
- [ ] Add the sim to chipper/tsconfig/all/tsconfig.json
- [ ] Remove old repo directories in `chipper/dist/js`, `chipper/dist/declarations`, and `chipper/dist/js-cache-status.json` and and restart your transpiler.
- [ ] Notify Slack channel dev-public that the repo has been renamed. E.g. "I just renamed repository {{OLD_REPO}} to {{NEW_REPO}}. Please pull perennial and perennial-alias, run `clone-missing-repos.sh` at your convenience, remove {{OLD_REPO}} in `chipper/dist/js`, `chipper/dist/declarations`, and `chipper/dist/js-cache-status.json` and restart your transpiler."

### If this is a simulation. . .
  - [ ] Rename many files:
    * `*en.json` string file
    * `main.js` file
    * Screens/Views/Models?
    * Namespace file
  - [ ] Make sure to update the title in the `*en.json` string file and update its usage in the main js file
  - [ ] Run `grunt modulify`
  - [ ] update usages of the Namespace file
  - [ ] Looks through all usages in the repo of the previous name to make sure issues links, comments and code are updated.
  This especially applies to imports for the namespace and strings.
