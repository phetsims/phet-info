# New Repository Checklist

These steps contain the following placeholders that you'll need to fill in:

- `{{AUTHOR}}}` - the name that will appear in `@author` code annotations, e.g. `Jane Doe`
- `{{REPO}}` - the repository name, e.g. `gas-properties`. This should be composed of lower-case characters and dashes, and should have <=214 characters (see naming constraints in https://docs.npmjs.com/cli/v7/configuring-npm/package-json).
- `{{TITLE}}` - the simulation's title, e.g. `Gas Properties`

## Steps to create a new simulation repo

At https://github.com/phetsims:
- [ ] Press the "New" button.
- [ ] In "Repository' text field, enter the repository name.
- [ ] In the Description field, enter `"{{TITLE}}" is an educational simulation in HTML5, by PhET Interactive Simulations.`
- [ ] Set visibility to "Public".
- [ ] Do not check the "Initialize this repository with a README" checkbox.
- [ ] Do not check "Add .gitignore".
- [ ] Do not check "Add a license".

In your working copy of perennial repo:
- [ ] Run `grunt create-sim --repo="{{REPO}}" --author="{{AUTHOR}}" --title="{{TITLE}}"` to create the file structure and skeleton code for the sim.

In your working copy of the sim repo:
- [ ] `git init`
- [ ] `git add * .gitignore`
- [ ] `git commit -m "Initial commit"`
- [ ] `git remote add origin https://github.com/phetsims/{{REPO}}.git`
- [ ] `git push -u origin master`

At https://github.com/phetsims/{{REPO}}:
- [ ] Go to _Settings => Collaborators and teams_. Press the "Add teams" button.
  See [team assignment.md](https://github.com/phetsims/phet-info/blob/master/policies/team%20assignment.md) for
  assignments by repo type.
- [ ] Create a Sim Checklist issue using
  template [sim-checklist.md](https://github.com/phetsims/phet-info/blob/master/checklists/sim-checklist.md). Use "
  {{TITLE}} Master Checklist" as the issue name. Assign to @ariel-phet.

In your working copy of perennial repo:
- [ ] Add the new repo to `perennial/data/active-repos`. Commit and push. Then pull perennial-alias so these two checkouts stay in sync. If needed immediately, run `cd perennial/ && grunt generate-data` and commit and push to update data lists. Otherwise it is done every night as part of daily grunt work.  _Note that your sim won't run in phetmarks until this is done._

Other:
- [ ] Navigate to https://bayes.colorado.edu/dev/phettest/ and click the "Refresh perennial, perennial-alias, and chipper" button. If you do not know the password, please ask another developer.
- [ ] Apply GitHub labels. See [github-labels/README.md](https://github.com/phetsims/phet-info/blob/master/github-labels/README.md).
- [ ] Apply branch protection rules using [protect-branches-for-repo.js](https://github.com/phetsims/perennial/blob/master/js/scripts/protect-branches-for-repo.js). Follow the instructions in the documentation at the top of the script.
- [ ] Notify Slack channel dev-public that the repo has been created. E.g. "I just added a new repository, {{REPO}}. Please pull perennial and perennial-alias and run `clone-missing-repos.sh` at your convenience."
- [ ] If using IDEA/Webstorm (pre-2018), add the git source root for the repository.
- [ ] Follow any remaining "Implementation" tasks in the Master Checklist issue that you created above.
- [ ] If applicable, add any needed dependencies to `phetLibs` in package.json. If you change package.json, run `grunt update`.
- [ ] Add the sim to [responsible_dev.json](https://github.com/phetsims/phet-info/blob/master/sim-info/responsible_dev.json).
- [ ] Add the sim to chipper/tsconfig/all/tsconfig.json
- [ ] If applicable, add corresponding dependencies from `phetLibs` in package.json to "references" in tsconfig.json. 

## Steps to create a different type of repo

At https://github.com/phetsims:
- [ ] Press the "New" button.
- [ ] Fill in the Description field.  (Ask other developers if you need suggestions.)
- [ ] Decide on visibility. (Ask other developers if you're not sure.)
- [ ] Typically do not select options that would initialize the repo by creating files (README, .gitignore, LICENSE).

In your working copy of the sim repo:
- [ ] Create the file structure locally. It's best to start (currently) by copying from a similar repository (but without the `.git` directory). Make sure to keep `.gitignore`, etc.
- [ ] `git init`
- [ ] `git add * .gitignore`
- [ ] `git commit -m "Initial commit"`
- [ ] `git branch -M master`
- [ ] `git remote add origin https://github.com/phetsims/{{REPO}}.git`
- [ ] `git push -u origin master`

At https://github.com/phetsims/{{REPO}}:
- [ ]Go to _Settings => Collaborators and teams_. Press the "Add teams" button. See [team assignment.md](https://github.com/phetsims/phet-info/blob/master/policies/team%20assignment.md) for assignments by repo type.

In your working copy of perennial repo:
- [ ] If applicable: Add the new repo to `perennial/data/active-repos`. Commit and push. Pull perennial-alias. If needed immediately, run `cd perennial/ && grunt generate-data` and commit and push to update data lists. Otherwise it is done every night as part of daily grunt work.

If this repo is a common code dependency for all sims:
- [ ] Add it to the list of `clone` commands in [phet-development-overview.md](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md)
- [ ] Update all sim published README files (because the "Quick Start" section has these git clone commands too).

Other:
- [ ] Notify Slack channel dev-public that the repo has been created. E.g. "I just added a new repository, {{REPO}}. Please pull perennial and perennial-alias and run `clone-missing-repos.sh` at your convenience."
- [ ] Apply GitHub labels. See [github-labels/README.md](https://github.com/phetsims/phet-info/blob/master/github-labels/README.md).
- [ ] Apply branch protection rules. Use [this script to do so](https://github.com/phetsims/perennial/blob/master/js/scripts/protect-branches-for-repo.js).
- [ ] If using IDEA/Webstorm (pre-2018), add the git source root for the repository.
- [ ] Add the repo to [responsible_dev.json](https://github.com/phetsims/phet-info/blob/master/sim-info/responsible_dev.json).
- [ ] Add the repo to chipper/tsconfig/all/tsconfig.json