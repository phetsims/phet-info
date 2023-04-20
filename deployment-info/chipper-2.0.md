# Deployment Info for chipper 2.0

# Table of Contents

* [Building simulation](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#building-simulations)
* [Updating supported brands](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#updating-supported-brands)
* [Building standalone repositories](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#building-standalone-repositories)
* [Building wrapper repositories](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#building-standalone-repositories)
* [Deploying simulations](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#deploying-simulations)
  * [If working off campus, install the VPN](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#if-working-off-campus-install-the-vpn)
  * [Configure build-local.json settings](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#configure-remote-bashrc)
  * [Configure remote ~/.bashrc](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#configure-remote-bashrc)
  * [Configure an RSA key](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#configure-an-rsa-key)
  * [Dev deployments](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#dev-deployments)
  * [One-off deployments](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#one-off-deployments)
  * [RC/production deployments and release branches](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#rcproduction-deployments-and-release-branches)
    * [If the release branch does not yet exist](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#if-the-release-branch-does-not-yet-exist)
    * [RC/production deployment on an existing branch](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#rcproduction-deployment-on-an-existing-branch)
    * [Manual maintenance patching](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#manual-maintenance-patching)
  * [Prototype deployments](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#prototype-deployments)
  * [PhET-iO Wrapper deployments](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#phet-io-wrapper-deployments)
* [Branch Protections](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#branch-protections)
* [Deploying pre-chipper-2.0 things](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#deploying-pre-chipper-20-things)

# Building simulations

`grunt` (no arguments) in a sim directory will build whatever brands (listed in build-local.json) are supported by the
simulation. If this doesn't exist, it will fall back to adapted-from-phet. It's highly recommended that, where there is
a `brand: 'phet'` in your build-local.json, it should be augmented by a `brands: [ 'phet', 'phet-io' ]` (or whatever
brands you would like to build by default).

`grunt --brands=phet,phet-io` (using `--brands`) will override and build the desired brands. If any brand given like
this is not supported, the build will fail out.

Chipper 2.0 also adds the `--debugHTML` option to builds (will build another version with the `_debug` suffix), and has
the `-allHTML` option (not relevant for the phet-io brand). Additionally, it is possible to build a sim with a one-off
version identifier with `--oneOff={{ONE_OFF_NAME}}`, which will be included in the version identifier. This is a build
flag, and is not provided to deployment tasks.

# Updating supported brands

In each sim's package.json, it lists the brands that are supported. When a phet-io sim is instrumented, it should be
added as a supported brand in package.json. The files under perennial/data (simulation lists, based on phet-io or other
support) will be automatically updated by a process running on bayes (grunt generate-data).

# Building standalone repositories

Scenery/Kite/Dot/etc. can be built as a standalone file that can be included (e.g. that file is used for Scenery
examples and documentation). Just `grunt` in the repository should do the trick, and note that there are no brands, so
it does not create brand directories.

# Building wrapper repositories

Repositories like phet-io-wrapper-sonification can also be built with `grunt`, placing the files to be uploaded in the
build directory.

# Deploying simulations

If you haven't run perennial commands in a while, `npm prune` and `npm update` under perennial, perennial-alias and
chipper may be needed. I'll notify for any further module changes.

Note that all perennial commands (including those for dev/rc/production deployments) can be run from newer (as of
sometime December 2017) simulations from the simulation directory. For instance, `grunt checkout-shas` now lives in
perennial, but newer chipper SHAs will detect this and spawn the correct perennial grunt task. It will add
a `--repo={{REPO}}` command line flag to the perennial command so that it knows which repository is the target.

So, for example,

```
chains# grunt dev --brands=phet,phet-io
```

will run

```
perennial# grunt dev --repo=chains --brands=phet,phet-io
```

## If working off campus, install the VPN

- If you work exclusively on campus, this step is not required.
- If you plan on deploying sims from a remote location, install the Cisco Anyconnect Secure Mobility Client
  from https://oit.colorado.edu/services/network-internet-services/vpn.

## Configure build-local.json settings

Your default build configuration is specified in `~/.phet/build-local.json`. Describing or identifying the entries
in `build-local.json` is beyond the scope of this document; ask a PhET developer for help in setting up this file. At a
minimum you will need `devUsername` and `buildServerAuthorizationCode`. A few handy keys:

- `buildServerNotifyEmail`: add your email to be notified on the success or failure of your builds to the build server.
- `brand:phet` for older (pre 2.0) chipper SHAs: to automatically build the phet brand instead of the adapted-from-phet
  brand. NOTE: this will be ignored if `--brand` is specified on the command line.
- `brands: [ 'phet', 'phet-io' ]` for newer chipper SHAs: to automatically build those brands instead of
  adapted-from-phet. NOTE: This will be ignored if `--brands` is specified on the command line. In particular, since our
  deployment process does this, this will be ignored for deployments.

It is generally beneficial to include both `brand:` and `brands:` entries in the `build-local.json`, so that it will
work on simulations both before and after the chipper 2.0 conversion.

## Configure remote ~/.bashrc

In order to ensure that all files you write to the dev server are accessible by other phet users (both people and
machines), please add the following line at the bottom of ~/.bashrc on bayes.colorado.edu.

```
umask g+w
```

## Configure an RSA key

Configure an RSA key, or you will be prompted multiple times for a password during dev-related build tasks.

- If you don't already have an RSA key, generate one by running `ssh-keygen -t rsa`.
- Add an entry for bayes in `localhost@~/.ssh/config` using this template:

 ```
 Host bayes
    HostName bayes.colorado.edu
    User {{IDENTIKEY}}
    Port 22
    IdentityFile ~/.ssh/id_rsa
 ```

- Add your public key (found in `localhost@~/.ssh/id_rsa.pub`) to `bayes@~/.ssh/authorized_keys`.
  - This can usually be accomplished by running `ssh-copy-id bayes`.
  - If you don't have `ssh-copy-id`,
    use `cat ~/.ssh/id_rsa.pub | ssh {{IDENTIKEY}}@bayes.colorado.edu "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"`
- Change the permissions of `authorized_keys` so it is not group writable: `chmod g-w authorized_keys`
- Test ssh from your local machine at least once so that you can accept the remote RSA key from bayes by
  running `ssh bayes`.

## Dev deployments

**Normal dev deployments can only be done from master. If you want to deploy off of a branch, do a one-off deployment
** (with a clean working copy on the sim being deployed). To deploy a dev version, run:

```sh
grunt dev --brands={{BRANDS}}
```

in the simulation repository. Typically you would have `--brands=phet` or `--brands=phet,phet-io` or some combination.

This will do the entirety of what the checklist did before (and may prompt about certain questions). Notably, it will
increment the version test number (e.g. the 2 in 1.3-dev.2). For example, if the package.json specified a version of '
1.2-dev.3' before deployment, then '1.2-dev.4' will be committed and deployed.

## One-off deployments

These are like dev deployments, but should be done from a named branch (where the name does not contain any `-` or `.`
characters).

Prior to branch creation, be sure to create a GitHub issue within the associated repo. Its title should be of the
form `branch: {{branchName}}`, and the description should describe the purpose of the branch, expected lifetime of the
branch, and links to any other relevant issues.

To create a branch (easily) for one-off deployments, run:

```sh
grunt create-one-off --branch={{BRANCH}}
```

This will create the branch with the relevant name, and set up the package.json appropriately.

Thus a normal `grunt` will build with the one-off version from the branch. To deploy a one-off version:

```sh
grunt one-off --brands={{BRANDS}}
```

from the branch.

## RC/production deployments and release branches

Chipper 2.0 release branches support building of all brands. The branch name will ONLY ever be of the
format `{{MAJOR}}.{{MINOR}}`, e.g. `1.7`, and that branch will only support building/deploying versions that match that
major/minor combination.

NOTE: Release branches are created for RCs. If you need to make a change after the first RC (but before publication),
you will still want to follow the process for maintenance patches.

### If the release branch does not yet exist

First, make sure you have checked out all of the repo SHAs that you intend to use for the release branch. If you want to
also deploy an RC (which is typical when creating the release branch), just run the RC deployment command, and it will
prompt you whether the release branch should be created. For example, if `1.6` was the latest release branch, and you
want to create `1.7` and deploy an RC, just fire off `grunt rc --branch=1.7 --brands={{BRANDS}}`.

If you do not want to deploy an RC when creating the release branch, instead directly
do `grunt create-release --branch=1.7 --brands={{BRANDS}}` (which will handle all steps to create the new branch).
Release branches should be created using either `grunt rc` or `grunt create-release`, as this sets them up with the
correct package.json version and dependencies.json content.

NOTE: The `--brands` you include in the command will be set as the only supported brands for the release
branch in the `package.json`.
NOTE: It will initialize the branch to a version of 1.0.0-rc.0, and then increment/deploy to 1.0.0-rc.1.


### RC/production deployment on an existing branch

For deploying a RC (Release Candidate), execute:

```sh
grunt rc --brands={{BRANDS}} --branch={{BRANCH}}
```

For deploying a production version, execute either:

```sh
grunt production --brands={{BRANDS}} --branch={{BRANCH}}
```

for a published, non-prototype sim, or

```sh
grunt prototype --brands={{BRANDS}} --branch={{BRANCH}}
```

for a published sim.

For all of these, follow the prompts. It should handle all of the steps in the older deployment checklist, and will
notify you about any additional tasks that you will need to take afterwards.

### Manual maintenance patching

If you want to make a change to the sim's own repo on the release branch (and no changes to other dependencies), then
generally first do the following:

- From perennial, `grunt checkout-target --repo={{REPO}} --target={{BRANCH}}`,
  e.g. `grunt checkout-target --repo=chains --target=1.2`.
- Apply the change to the sim's branch (either a usual commit, or by cherry-picking a change,
  e.g. `git cherry-pick -x {{SHA}}` in the sim repo).
- Test it. You can `grunt` in the sim repo (the `checkout-target` above did the NPM magic for it to work)
- Push the change to the sim branch (e.g. `git push origin 1.2`).

Otherwise if a dependency (e.g. scenery or any "common" repo) needs patching:

- From perennial, `grunt checkout-target --repo={{SIM}} --target={{BRANCH}}`,
  e.g. `grunt checkout-target --repo=chains --target=1.2`.
- Check the common repo to see if it has a branch named `{{SIM}}-{{BRANCH}}`, e.g. does scenery have a branch named
  chains-1.2
  - If it HAS the branch, ensure that the branch's HEAD commit is the same as the currently-checked-out commit. THEN
    checkout the branch (e.g. `git checkout chains-1.2`) in the common repo. If the commits don't match, INVESTIGATE as
    something went wrong before. Talk to @jonathanolson?
  - If there IS NO branch, create it in the common repo with `git checkout -b {{SIM}}-{{BRANCH}}`,
    e.g. `git checkout -b chains-1.2`
- Apply the change to the sim's branch (it's almost always a cherry-pick, e.g. `git cherry-pick -x {{SHA}}` in the
  common repo).
- Test it. You can `grunt` in the sim repo (the `checkout-target` above did the NPM magic for it to work)
- Push the change to the common branch (e.g. `git push origin chains-1.2`)
- If you didn't build it before, run `grunt` in the sim repo.
- Copy the dependencies.json from the build directory to the top-level directory in the sim.
  - Newer sims (chipper 2.0): `cp build/phet/dependencies.json .`
  - Older sims: `cp build/dependencies.json .`
- `git add dependencies.json`
- `git commit --no-verify -m {{MESSAGE}}`, where `{{MESSAGE}}` includes the GitHub issue URL(s) for the maintenance
  release.
- `git push origin {{BRANCH}}`.

This will ensure that the top level dependencies.json will properly reference the common-code fixed SHA, and that we'll
always have a consistent common code branch for the sim branch.

This would usually be followed by 1+ RC deployments and then a production deployment.

If you need to get back to master, use `grunt checkout-master` from the sim repo.

## Prototype deployments

A prototype is defined as a sim version that is deemed worthy of early release to the public before it has gone through
the full production process. Prototypes will typically be published for legacy sims that are not yet available in HTML5.

How prototypes differ from production versions:

- A prototype is not necessarily feature-complete, and release will typically occur before formal code review and
  production-level QA testing.
- Known issues may be present in prototypes. These will generally be of the nature of "polish" issues, but pedagogical
  issues or crashing will generally be considered "showstoppers".
- Testing will not be as thorough as a production RC and will focus on "normal" usability and pedagogical accuracy.
  Issues found in testing that go beyond these requirements will typically be deferred.
- A prototype will be published at the appropriate "latest" link, but the sim's page on phet.colorado.edu **WILL NOT**
  be made visible.
- The first version of a prototype will typically be 1.0, and there may be more than one minor release of a prototype.
  Therefore the first version visible at phet.colorado.edu will have the version schema "1.N.0", where N is >= 1. For
  example, if we had 2 prototypes with versions 1.0.0 and 1.1.0, then the first version visible at phet.colorado.edu
  would be 1.2.0.
- When cost-effective, maintenance releases can be performed on a prototype release branch. When not cost-effective, a
  new version of a prototype may require a new release branch.

Prototypes will follow the process
for [RC/production deployments](https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-2.0.md#rcproduction-deployments-and-release-branches)
using `grunt prototype`, with the following differences:

- Use `grunt prototype` instead of `grunt production`. `grunt rc` works as normal. DO NOT use `grunt production`, as
  this will mark it as a published branch.
- When the RC test issue is created:
  - Use
    the [prototype testing template](https://github.com/phetsims/QA/blob/master/issue-templates/prototype-test-template.md).
  - Issue title format is "Prototype test: ${{SIM}} {{VERSION}}", for example "Prototype test: Natural Selection
    1.0.0-rc.1".
  - Label the issue `QA:prototype-test`.
- After publishing, the developer will:
  - Inform the lead designer that the prototype is published.
- After publishing, the designer will:
  - Mark the sim as a prototype on the [Admin page](https://phet.colorado.edu/admin/main).
  - Add the sim to
    the [HTML5 Prototypes Google Doc](https://docs.google.com/document/d/1d9j8OGO7qPgdL2YvdMeSbztYt7hGXiAL7hAQLXnH-bU/edit)
  - Notify AP so that he can announce on social media.
  - Notify ON so that he can announce via email.

# Branch Protections

Production branches are "protected" on github so that they cannot be deleted unless absolutely necessary. This includes
all branches used in deployed sims in the simulation and common code repositories. Branches are protected by "rules"
where each rule has an `fnmatch` pattern string. Branches with names matching the pattern cannot be deleted. If you must
delete a branch you need to delete the protection rule, delete the branch, and then add the protection rule back. The
steps for this are:

1. Delete the branch rule. Go to https://github.com/phetsims/{{SIM-NAME}}/settings/branches. Find the rule that is
   protecting the branch you want to delete and delete it. For example, if you need to delete the `1.1` branch you can
   delete the Branch protection rule with the pattern `*[0-9].[0-9]*`.
2. Delete the branch.
3. Add the rule back.
   Use [This script to do so](https://github.com/phetsims/perennial/blob/master/js/scripts/protect-branches-for-repo.js).
   For example, you can run this to add back protection rules to john-travoltage.

  ```
  node perennial/js/scripts/protect-branches-for-repo.js john-travoltage
  ```

# Deploying pre-chipper-2.0 things

If you get an error during the deploy command like ```chipper 0.0.0 cannot build multiple brands at a time``` try using
chipper 2.0 steps but just building and deploying each brand separately before moving on to chipper-1.0.

See https://github.com/phetsims/phet-info/blob/master/deployment-info/chipper-1.0.md
