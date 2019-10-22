# New Repository Checklist

These steps contain the following placeholders that you'll need to fill in:

- `{{AUTHOR}}}` - the name that will appear in `@author` code annotations, e.g. `Jane Doe` 
- `{{REPO}}` - the repository name, e.g. `gas-properties`
- `{{TITLE}}` - the simulation's title, e.g. `Gas Properties`

## Steps to create a new simulation repo

At https://github.com/phetsims:
- [ ] Press the "New" button. 
- [ ] Set the Description field to `"{{TITLE}}" is an educational simulation in HTML5, by PhET Interactive Simulations.`  
- [ ] Set visibility to "Public". 
- [ ] DO NOT check the "Initialize this repository with a README" checkbox. 
- [ ] Leave "Add .gitignore" set to "None"
- [ ] Leave "Add a license" set to "None". 

In your working copy of perennial repo:
- [ ] Run `grunt create-sim --repo={{REPO}} --author="{{AUTHOR}}" --title="{{TITLE}}"` to create the file structure and skeleton code for the sim.

In your working copy of the sim repo: 
- [ ] `git init`
- [ ] `git add * .gitignore`
- [ ] `git commit -m "Initial commit"`
- [ ] `git remote add origin https://github.com/phetsims/{{REPO}}.git`
- [ ] `git push -u origin master`

In your working copy of perennial repo:
- [ ] Add the new repo to `perennial/data/active-repos`. Run `clone-missing-repos.sh` to check your change, commit and push. After a few minutes, an automated process should update the other files under perennial/data/. Pull perennial so you can find the sim in phetmarks.

At https://github.com/phetsims/{{REPO}}:
- [ ] Go to Settings => Collaborators and Teams, add the teams used in another public sims (currently Design, Development, and Quality Assurance) with "Write" permissions.
- [ ] Create a Master Checklist issue using template [sim_new_checklist.md](https://github.com/phetsims/phet-info/blob/master/checklists/sim_new_checklist.md). Use "{{TITLE}} Master Checklist" as the issue name. Assign to @ariel-phet.

Other:
- [ ] Navigate to phettest.colorado.edu and click the "Refresh Perennial" button. If you're off campus, [CU's VPN service](https://oit.colorado.edu/services/network-internet-services/vpn) is required to access phettest.colorado.edu.
- [ ] Apply GitHub labels. See [github-labels/README.md](https://github.com/phetsims/phet-info/blob/master/github-labels/README.md).
- [ ] Notify Slack channel dev-public that the repo has been created. E.g. "I just added a new repository, {{REPO}}. Please pull perennial and run `clone-missing-repos.sh` at your convenience."
- [ ] If using IDEA/Webstorm (pre-2018), add the git source root for the repository.
- [ ] Follow any remaining "Implementation" tasks in the Master Checklist issue that you created above.
- [ ] If applicable, add any needed dependencies to `phetLibs` in package.json. If you change package.json, run `grunt update`.
- [ ] Add the sim to [responsible_dev.md](https://github.com/phetsims/phet-info/blob/master/sim-info/responsible_dev.md).

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
- [ ] `git remote add origin https://github.com/phetsims/{{REPO}}.git`
- [ ] `git push -u origin master`

At https://github.com/phetsims/{{REPO}}:
- [ ] Go to Settings => Collaborators and Teams, add the teams used in another public sims (currently Design, Development, and Quality Assurance) with "Write" permissions. _NOTE: If the repo is private, it is REQUIRED to add the Machine User collaborator (so automated processes can clone/pull the repo). CT will break otherwise._

In your working copy of perennial repo:
- [ ] If applicable: Add the new repo to `perennial/data/active-repos`. Run `clone-missing-repos.sh` to check your change, commit and push. After a few minutes, an automated process should update the other files under perennial/data/. Pull perennial so you can find the sim in phetmarks.

Other:
- [ ] Notify Slack channel dev-public that the repo has been created. E.g. "I just added a new repository, {{REPO}}. Please pull perennial and run `clone-missing-repos.sh` at your convenience."
- [ ] Apply GitHub labels. See [github-labels/README.md](https://github.com/phetsims/phet-info/blob/master/github-labels/README.md).
- [ ] If using IDEA/Webstorm (pre-2018), add the git source root for the repository.
