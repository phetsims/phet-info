# Rename Repo Checklist

## Steps for renaming a repo

- [ ] Make sure all commits are pushed to that repo.
- [ ] On Github.com, go to repo -> Settings -> Options -> "Repository name"  and rename.
- [ ] Rename in `perennial/data/active-repos` and any other perennial data files it occurs in,
  like `active-runnables`, `active-sims`, `phet-io`, etc. Push the change to perennial and then pull perennial-alias.
- [ ] Clone the new repo by running `grunt sync`.
- [ ] Update `package.json` accordingly. Including but not necessarily limited to:
  * `name`
  * `repository.url`
  * `phet.requirejsNamespace`
- [ ] Change entry
  in [responsible_dev.json](https://github.com/phetsims/phet-info/blob/main/sim-info/responsible_dev.json).
- [ ] If applicable, "Sync" on phettest.
- [ ] Remove old repo directories in `chipper/dist/**/${oldRepo}`
- [ ] Run `rm -rf {{OLD_REPO}}` from the phetsims directory
- [ ] Notify Slack channel dev-public that the repo has been renamed. E.g. "I just renamed repository {{OLD_REPO}} to
  {{NEW_REPO}}. Please sync at your convenience, remove
  {{OLD_REPO}} references from `chipper/dist/` directories (such as `tsc/outdir/` and `eslint/cache/`), and restart your transpiler."

### If this is a simulation. . .

- [ ] Rename many files:
  * `*en.json` string file
  * `main.js` file
  * Screens/Views/Models?
  * Namespace file
- [ ] Make sure to update the title in the `*en.json` string file and update its usage in the main js file
- [ ] Run `grunt modulify`
- [ ] update usages of the Namespace file
- [ ] Looks through all usages in the repo of the previous name to make sure issues links, comments and code are
  updated. This especially applies to imports for the namespace and strings.
- [ ] Use  `find` to search for files with the old repo name in generated files outside of the sim repo. For example, from your root directory:
  * `find . -name quantum-measurement* -print`
- [ ] Search the entire codebase references to the old repo name.