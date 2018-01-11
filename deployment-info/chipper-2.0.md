
**NOTE: Until chipper 2.0 is merged into master, please check out the `2.0` branch of chipper and the `chipper2.0` branch of phet-io-wrappers. The `chipper-2.0` branch of phetmarks may also be useful if you use phetmarks. Leave perennial on master (unless you are @mattpen or working on the build-server)**

# Building simulations

`grunt` (no arguments) in a sim directory will build whatever brands (listed in build-local.json) are supported by the simulation. If this doesn't exist, it will fall back to adapted-from-phet. It's highly recommended that, where there is a `brand: 'phet'` in your build-local.json, it should be augmented by a `brands: [ 'phet', 'phet-io' ]` (or whatever brands you would like to build by default).

`grunt --brands=phet,phet-io` (using `--brands`) will override and build the desired brands. If any brand given like this is not supported, the build will fail out.

Chipper 2.0 also adds the `--debugHTML` option to builds (will build another version with the `_debug` suffix), and has the `-allHTML` option (not relevant for the phet-io brand). Additionally, it is possible to build a sim with a one-off version identifier with `--oneOff={{ONE_OFF_NAME}}`, which will be included in the version identifier. This is a build flag, and is not provided to deployment tasks.

Most other build options should be preserved, and apply to all brands that are built.

# Updating supported brands

In each sim's package.json, it lists the brands that are supported. When a phet-io sim is instrumented, it should be added as a supported brand in package.json. The files under perennial/data (simulation lists, based on phet-io or other support) will be automatically updated by a process running on bayes (grunt generate-data).

# Building standalone repositories

Scenery/Kite/Dot/etc. can be built as a standalone file that can be included (e.g. that file is used for Scenery examples and documentation). Just `grunt` in the repository should do the trick, and note that there are no brands, so it does not create brand directories.

# Building wrapper repositories

Repositories like phet-io-wrapper-sonification can also be built with `grunt`, placing the files to be uploaded in the build directory.

# Deploying simulations

If you haven't run perennial commands in a while, `npm prune` and `npm update` under perennial will probably be needed. I'll notify for any further module changes.

Note that all perennial commands (including those for dev/rc/production deployments) can be run from newer (as of sometime December 2017) simulations from the simulation directory. For instance, `grunt checkout-shas` now lives in perennial, but newer chipper SHAs will detect this and spawn the correct perennial grunt task. It will add a `--repo={{REPO}}` command line flag to the perennial command so that it knows which repository is the target.

So, for example,
```
chains# grunt dev --brands=phet,phet-io
```
will run
```
perennial# grunt dev --repo=chains --brands=phet,phet-io
```

## Configure build-local.json settings

Your default build configuration is specified in `~/.phet/build-local.json`. Describing or identifying the entries in `build-local.json` is beyond the scope of this document; ask a PhET developer for help in setting up this file. At a minimum you will need `devUsername` and `buildServerAuthorizationCode`. A few handy keys:

- `buildServerNotifyEmail`: add your email to be notified on the success or failure of your builds to the build server.
- `brand:phet` for older (pre 2.0) chipper SHAs: to automatically build the phet brand instead of the adapted-from-phet brand. NOTE: this will be ignored if `--brand` is specified on the command line.
- `brands: [ 'phet', 'phet-io' ]` for newer chipper SHAs: to automatically build those brands instead of adapted-from-phet. NOTE: This will be ignored if `--brands` is specified on the command line. In particular, since our deployment process does this, this will be ignored for deployments.

It is generally beneficial to include both `brand:` and `brands:` entries in the `build-local.json`, so that it will work on simulations both before and after the chipper 2.0 conversion.

## Configure an RSA key

Configure an RSA key, or you will be prompted multiple times for a password during dev-related build tasks.

 - If you don't already have an RSA key, generate one by running `ssh-keygen -t rsa`.
 - Add an entry for spot in `localhost@~/.ssh/config` using this template:

 ```
 Host spot
    HostName spot.colorado.edu
    User {{IDENTIKEY}}
    Port 22
    IdentityFile ~/.ssh/id_rsa
 ```
 - Add your public key (found in `localhost@~/.ssh/id_rsa.pub`) to `spot@~/.ssh/authorized_keys`
 - Change the permissions of `authorized_keys` so it is not group writable: `chmod g-w authorized_keys`

## Dev deployments

**Normal dev deployments can only be done from master** (with a clean working copy on the sim being deployed). To deploy a dev version, run:
```sh
grunt dev --brands={{BRANDS}}
```
in the simulation repository. Typically you would have `--brands=phet` or `--brands=phet,phet-io` or some combination.

This will do the entirety of what the checklist did before (and may prompt about certain questions). Notably, it will increment the version test number (e.g. the 2 in 1.3-dev.2). For example, if the package.json specified a version of '1.2-dev.3' before deployment, then '1.2-dev.4' will be committed and deployed.

## One-off deployments

NOT YET IMPLEMENTED

## RC/production deployments and release branches

New chipper 2.0 release branches will support building of all brands. The branch name will ONLY ever be of the format `{{MAJOR}}.{{MINOR}}`, e.g. `1.7`, and that branch will only support building/deploying versions that match that major/minor combination.

### If the release branch does not yet exist

First, make sure you have checked out all of the repo SHAs that you intend to use for the release branch. If you want to also deploy an RC (which is typical when creating the release branch), just run the RC deployment command, and it will prompt you whether the release branch should be created. For example, if `1.6` was the latest release branch, and you want to create `1.7` and deploy an RC, just fire off `grunt rc --branch=1.7 --brands={{BRANDS}}`.

If you do not want to deploy an RC when creating the release branch, instead directly do `grunt create-release --branch=1.7` (which will handle all of the steps to create the new branch).

### RC/production deployment on an existing branch

Just execute:
```sh
grunt rc --brands={{BRANDS}} --branch={{BRANCH}}
# or
grunt production --brands={{BRANDS}} --branch={{BRANCH}}
```
and follow the prompts. It should handle all of the steps in the older deployment checklist, and will notify you about any additional tasks that you will need to take afterwards.

### Maintenance patching

If you want to make a change to the sim's own repo on the release branch, just commit the change and push it to the branch. If the change affects other repositories, you'll want to create or update that repository's branch called {{SIM}}-{{BRANCH}}, and either manually update the top-level dependencies.json of the sim, or copy the entire file from a build directory (preferred).

For example, if I'm patching molecule-shapes and it needs a scenery fix, I'll:

- Apply the fix in the molecule-shapes repository on the branch (e.g. 1.7)
- Check to see if scenery has a branch named (e.g.) molecule-shapes-1.7
  - If it does not exist (assuming you have already checked out SHAs for the release branch), `git checkout -b molecule-shapes-1.7`, apply the fix, and push to that branch.
  - If it does exist, check it out, apply the fix and push.
- Build molecule-shapes (`grunt`)
- Copy `build/phet/dependencies.json` (or any other brand's copy, they are identical) to the top level (`molecule-shapes/dependencies.json`).
- Commit and push the change to the release branch.

This will ensure that the top level dependencies.json will properly reference the common-code fixed SHA, and that we'll always have a consistent common code branch for the sim branch.

This would usually be followed by 1+ RC deployments and then a production deployment.

# Deploying wrappers

`grunt wrapper` in a wrapper directory (e.g. phet-io-wrapper-sonification) should deploy the whole thing. Follow the prompts.

# Deploying pre-chipper-2.0 things

See https://github.com/phetsims/phet-info/blob/master/deployment-info/sim_deployment.md
