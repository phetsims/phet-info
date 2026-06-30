# Deployment Info for chipper 2.0

# Table of Contents

* <!-- TOC -->
* [Building simulation](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#building-simulations)
* [Deployment Info for chipper 2.0](#deployment-info-for-chipper-20)
* [Table of Contents](#table-of-contents)
* [Building simulations](#building-simulations)
* [Updating supported brands](#updating-supported-brands)
* [Building standalone repositories](#building-standalone-repositories)
* [Deploying simulations](#deploying-simulations)
  * [Running commands](#running-commands)
  * [If working off campus, install the VPN](#if-working-off-campus-install-the-vpn)
  * [Configure build-local.json settings](#configure-build-localjson-settings)
  * [Configure remote ~/.bashrc](#configure-remote-bashrc)
  * [Configure an RSA key](#configure-an-rsa-key)
  * [Dev deployments](#dev-deployments)
  * [One-off deployments](#one-off-deployments)
  * [RC/production deployments and release branches](#rcproduction-deployments-and-release-branches)
    * [If the release branch does not yet exist](#if-the-release-branch-does-not-yet-exist)
    * [RC/production deployment on an existing branch](#rcproduction-deployment-on-an-existing-branch)
    * [Manual maintenance patching](#manual-maintenance-patching)
  * [Prototype deployments](#prototype-deployments)
* [Branch Protections](#branch-protections)
* [Deploying pre-sim-deployment things](#deploying-pre-chipper-20-things)
<!-- TOC -->[Updating supported brands](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#updating-supported-brands)
* [Building standalone repositories](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#building-standalone-repositories)
* [Building wrapper repositories](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#building-standalone-repositories)
* [Deploying simulations](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#deploying-simulations)
  * [Running commands in perennial](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#running-commands-in-perennial)
  * [If working off campus, install the VPN](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#if-working-off-campus-install-the-vpn)
  * [Configure build-local.json settings](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#configure-remote-bashrc)
  * [Configure remote ~/.bashrc](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#configure-remote-bashrc)
  * [Configure an RSA key](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#configure-an-rsa-key)
  * [Dev deployments](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#dev-deployments)
  * [One-off deployments](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#one-off-deployments)
  * [RC/production deployments and release branches](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#rcproduction-deployments-and-release-branches)
    * [If the release branch does not yet exist](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#if-the-release-branch-does-not-yet-exist)
    * [RC/production deployment on an existing branch](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#rcproduction-deployment-on-an-existing-branch)
    * [Manual maintenance patching](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#manual-maintenance-patching)
  * [Prototype deployments](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#prototype-deployments)
  * [PhET-iO Wrapper deployments](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#phet-io-wrapper-deployments)
* [Branch Protections](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#branch-protections)
* [Deploying pre-sim-deployment things](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#deploying-pre-chipper-20-things)

# Building simulations

As a general prerequisite, `npm ci` should be done at the top level of `totality/` before doing any other actions.

`bin/grunt --repo={{SIM}}` (or using `bin/use {{SIM}}` to set the active sim) will build the simulation for brands in your
`build-local.json`'s brand list that are supported by the simulation. It will fall back to `adapted-from-phet`. It is highly
recommended that `build-local.json` should have `brands: [ 'phet', 'phet-io' ]`.

`bin/grunt --repo={{SIM}} --brands=phet,phet-io` (using `--brands`) will override and build the desired brands. If any brand given like
this is not supported, the build will fail out.

# Updating supported brands

In each sim's package.json, it lists the brands that are supported. When a phet-io sim is instrumented, it should be
added as a supported brand in package.json. The files under perennial/data (simulation lists, based on phet-io or other
support) will be automatically updated by a process running on bayes (grunt generate-data).

# Building standalone repositories

Scenery/Kite/Dot/etc. can be built as a standalone file that can be included (e.g. that file is used for Scenery
examples and documentation). Just `bin/grunt --repo=${REPO}` in the repository should do the trick, and note that there
are no brands, so it does not create brand directories.

# Deploying simulations

As noted above, `npm ci` at the top level of `totality/` should be done before doing any other actions.

## Running commands

Build commands are run from the bin/ directory. For example:
```sh
bin/dev --repo={{SIM}}
```

## If working off campus, install the VPN

- If you work exclusively on campus, this step is not required.
- If you plan on deploying sims from a remote location, install the Cisco Anyconnect Secure Mobility Client
  from https://oit.colorado.edu/services/network-internet-services/vpn.

## Configure build-local.json settings

Your default build configuration is specified in `~/.phet/build-local.json`. Describing or identifying the entries in
`build-local.json` is beyond the scope of this document; ask a PhET developer for help in setting up this file. At a
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
  - If you don't have `ssh-copy-id`, use
    `cat ~/.ssh/id_rsa.pub | ssh {{IDENTIKEY}}@bayes.colorado.edu "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"`
- Change the permissions of `authorized_keys` so it is not group writable: `chmod g-w authorized_keys`
- Test ssh from your local machine at least once so that you can accept the remote RSA key from bayes by running
  `ssh bayes`.

## Dev deployments

**Normal dev deployments can only be done from main. If you want to deploy off of a branch, do a one-off deployment
** (with a clean working copy on the sim being deployed). To deploy a dev version, run:

```sh
bin/dev --repo={{SIM}}
```

in the simulation repository. It will publish with the normally-built brands.

This will do the entirety of what the checklist did before (and may prompt about certain questions). Notably, it will
increment the version test number (e.g. the 2 in 1.3-dev.2). For example, if the package.json specified a version of '
1.2-dev.3' before deployment, then '1.2-dev.4' will be committed and deployed.

## One-off deployments

TODO: Not yet finished with totality, see https://github.com/phetsims/totality/issues/140
NOTE: DO NOT try one-off deployments yet

These are like dev deployments, but are done from a named branch that is not "main" (where the branch name does not
contain any `-` or `.` characters). One-offs are useful to keep track of shas for maintenance or reproducibility, but
are not a formal, versioned release.

Prior to branch creation, be sure to create a GitHub issue within the associated repo. Its title should be of the form
`branch: {{branchName}}`, and the description should describe the purpose of the branch, expected lifetime of the
branch, and links to any other relevant issues.

To create a branch (easily) for one-off deployments run the following command from the exact SHAs that you want in your
one-off. You may want to run `grunt checkout-target` first to create the one-off from a release branch instead of
`main`.

```sh
# DEPRECATED, will be different
grunt create-one-off --branch={{BRANCH}}
```

This will create the branch with the relevant name, and set up the package.json appropriately. Thus a normal `grunt`
will build with the one-off version from the branch. To deploy a one-off version:

```sh
# DEPRECATED, will be different
grunt one-off --brands={{BRANDS}} --branch={{BRANCH}}
```

This will checkout the branch and its dependencies, and deploy using the "dev" version deployment algorithm.

## RC/production deployments and release branches

Branch versions for new branches are exclusively in the format of `{{MAJOR}}.{{MINOR}}`, e.g. `1.7`.

Totality will have a branch for each "release branch" with the name `releases/{{SIM}}/{{MAJOR}}.{{MINOR}}`, e.g. `releases/area-builder/1.7`.
This branch in general should NOT be checked out in your main working copy, will live in a worktree under
your worktree directory (by default `totality/worktrees/` unless overridden in build-local.json). It has minimal structure,
so checking out in your primary copy may result in unexpected issues due to deleted directories and a .gitignore that is
more minimal.

NOTE: Release branches are created for RCs. If you need to make a change after the first RC (but before publication),
you will still want to follow the process for maintenance patches.

### If the release branch does not yet exist

First, make sure you have checked out all of the repo SHAs that you intend to use for the release branch. If you want to
also deploy an RC (which is typical when creating the release branch), just run the RC deployment command, and it will
prompt you whether the release branch should be created. For example, if `1.6` was the latest release branch, and you
want to create `1.7` and deploy an RC, just fire off `bin/rc --repo={{SIM}} --branch=1.7`.

If you do not want to deploy an RC when creating the release branch, instead directly do
`bin/create-release --repo={{SIM}} --branch=1.7 --brands={{BRANDS}}` (which will handle all steps to create the new branch). Release
branches should be created using either `bin/rc` or `bin/create-release`, as this sets them up with the correct
package.json version and dependencies.json content.

NOTE: The `--brands` you include in the command will be set as the only supported brands for the release branch in the
`package.json`. NOTE: It will initialize the branch to a version of 1.0.0-rc.0, and then increment/deploy to 1.0.0-rc.1.

### RC/production deployment on an existing branch

For deploying a RC (Release Candidate), execute:

```sh
bin/rc --repo={{SIM}} --branch={{BRANCH}}
```

For deploying a production version, execute either:

```sh
bin/production --repo={{SIM}} --branch={{BRANCH}}
```

for a full production (non-prototype) sim, or

```sh
# DEPRECATED: TODO: Needs to be redone for totality, see https://github.com/phetsims/totality/issues/140
grunt prototype --brands={{BRANDS}} --branch={{BRANCH}}
```

for a prototype sim.

For all of these, follow the prompts. It should handle all of the steps in the older deployment checklist, and will
notify you about any additional tasks that you will need to take afterwards.

### Manual maintenance patching

First ensure the release branch is checked out into your worktree with:

```sh
bin/update-release --repo={{SIM}} --branch={{BRANCH}}
```

Then you can visit the worktree (`cd totality/worktrees/releases/{{SIM}}/{{MAJOR}}.{{MINOR}}`) and make direct changes
there, including cherry-picking in changes from main (assuming the changes only hit the top-level directories included
in the release branch). After making changes, you can simply push the changes (`git push origin releases/{{SIM}}/{{MAJOR}}.{{MINOR}}`).

This would usually be followed by 1+ RC deployments and then a production deployment.

## Prototype deployments

TODO: Prototype deployments are not yet fully implemented in totality, see https://github.com/phetsims/totality/issues/140

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
for [RC/production deployments](https://github.com/phetsims/phet-info/blob/main/deployment-info/sim-deployment.md#rcproduction-deployments-and-release-branches)
using `grunt prototype`, with the following differences:

- Use `grunt prototype` instead of `grunt production`. `grunt rc` works as normal. DO NOT use `grunt production`, as
  this will mark it as a published branch.
- When the RC test issue is created:
  - Use
    the [prototype testing template](https://github.com/phetsims/QA/blob/main/issue-templates/prototype-test-template.md).
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

## Redeploying Screenshots for a Sim

If we do everything correctly, screenshots should be updated prior to a release branch being created for a sim, and
they will be deployed as part of the normal deployment process. However, if that step was missed, or if you need to
update screenshots for some other reason, you can do so by running the following command:

```
bin/deploy-images --simulation={{SIM}}
```

It can take a while for the updates to show up on the main website due to caching, but you can check immediately using
phet-origin.colorado.edu.  As a real world example, screenshots were updated in May 2026 for Isotopes and Atomic Mass
using the command:

```
bin/deploy-images --simulation=isotopes-and-atomic-mass
```

...and the images were then verified by checking:
https://phet-origin.colorado.edu/sims/html/isotopes-and-atomic-mass/latest/isotopes-and-atomic-mass-900-alt2.png
https://phet-origin.colorado.edu/sims/html/isotopes-and-atomic-mass/latest/isotopes-and-atomic-mass-900-alt1.png
https://phet-origin.colorado.edu/sims/html/isotopes-and-atomic-mass/latest/isotopes-and-atomic-mass-900.png
.
.
.


# Branch Protections

TODO: unclear what the current status of this is, see https://github.com/phetsims/totality/issues/140

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
   Use [This script to do so](https://github.com/phetsims/perennial/blob/main/js/scripts/protect-branches-for-repo.js).
   For example, you can run this to add back protection rules to john-travoltage.

  ```
  sage run perennial/js/scripts/protect-branches-for-repo.js john-travoltage
  ```