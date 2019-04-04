# Steps to create a new simulation

- [ ] Create the repo: Go to https://github.com/phetsims, hit the "New" button). Copy (with modifications) the description from another sim, keep "Public" for visibility and DO NOT INITIALIZE the repo (we'll do that later).
- [ ] In perennial, `grunt create-sim --repo={{REPO}} --author="{{AUTHOR_STRING}}" --title="{{TITLE}}"`. This will create the file structure for the sim.
- [ ] In the sim repo: `git init`
- [ ] `git add * .gitignore`
- [ ] `git commit -m "Initial commit"`
- [ ] `git remote add origin https://github.com/phetsims/{{REPO}}.git`
- [ ] `git push -u origin master`
- [ ] In github (sim repo => "Settings" => Collaborators and Teams), add the teams used in another public sim (currently QA, design and development), and give equivalent permissions.
- [ ] Add to perennial/data/active-repos, run `clone-missing-repos.sh`to check your change, commit and push. (After a few minutes, an automated process should update the other files under perennial/data. pull perennial so you can find the sim in phetmarks.)
- [ ] Notify dev-public and email, e.g. "Just added {{REPO}} to active repos. Please pull perennial and clone-missing-repos at your convenience."
- [ ] Create a sim issue from the template https://github.com/phetsims/phet-info/blob/master/checklists/sim_new_checklist.md. Put the title as the issue name. Assign @ariel-phet.
- [ ] Follow remaining "Implementation" tasks in the checklist (e.g. add to responsible-dev.md, etc.), and as part of that use https://github.com/phetsims/phet-info/blob/master/github-labels/README.md for updating labels.
- [ ] If using IDEA/Webstorm (pre-2018), add the git source root for the repository
- [ ] If applicable, add any needed dependencies to `phetLibs` in package.json. If that changes, run `grunt update` afterwards.
- [ ] Navigate to phettest.colorado.edu and click the "Refresh Perennial" button

# Steps to create a different type of repo

- [ ] Create the repo: Go to https://github.com/phetsims, hit the "New" button). Come up with a description, decide on visibility, and generally do not initialize.
- [ ] Create the file structure locally. It's best to start (currently) by copying from a similar repository (but without the `.git` directory). Make sure to keep `.gitignore`, etc.
- [ ] In the new repo: `git init`
- [ ] `git add * .gitignore`
- [ ] `git commit -m "Initial commit"`
- [ ] `git remote add origin https://github.com/phetsims/{{REPO}}.git`
- [ ] `git push -u origin master`
- [ ] In github (sim repo => "Settings" => Collaborators and Teams), and add the desired teams. NOTE: If the repo is private, it is REQUIRED to add the Machine User collaborator (so automated processes can clone/pull the repo). CT will break otherwise.
- [ ] If applicable, Add to perennial/data/active-repos, run `clone-missing-repos.sh`to check your change, commit and push. (after a few minutes, an automated process should update the other files under perennial/data. pull perennial so you can find the sim in phetmarks)
- [ ] Notify dev-public and email, e.g. "Just added {{REPO}} to active repos. Please pull perennial and clone-missing-repos at your convenience."
- [ ] Follow instructions at https://github.com/phetsims/phet-info/blob/master/github-labels/README.md for setting up labels.
- [ ] If using IDEA/Webstorm (pre-2018), add the git source root for the repository
