
# Maintenance Release Process for Multiple Simulations

This document describes the process for performing maintenance releases that affect multiple simulations.  For the
single simulation process, please see sim_deployment.md.

## Branches, dependencies.json and releases

The goal of this process is to efficiently create commits on common repositories in simulation-specific branches (e.g. acid-base-solutions-1.1), sharing SHAs where possible, then update dependencies.json in the sim's branch (e.g. 1.1 branch in acid-base-solutions contains the new commit to where acid-base-solutions-1.1 points), and when ready do RC and production deployments.

## Overview of process

Generally, the first step is to identify the list of simulations that will need patches. There is no current script support for this, but in the future it may be possible to do some of this automatically.

For each patch/fix that needs to be applied, you'll want to identify which repositories will need to be patched. For instance, if you're applying a Scenery fix that uses PHET_CORE/Platform, you should check to see if phet-core is compatible for all simulations (maybe it doesn't have a check for the relevant browser in older sims).

If (for example), the repositories that need patches are scenery and phet-core, it could be possible that changes to one repository (say phet-core) aren't compatible with all scenery SHAs that were also used in the same simulations. Say we have one SHA for phet-core (A) that is both compatible with Scenery SHAs (B) and (C). There may be no (good) way of patching A (A*) that can be compatible with both the changes in B (B*) and C (C*). The maintenance release process supports this, and allows separate patches of phet-core's A for both B and C.

Thus the maintenance release process will group simulations together so that all simulations in a group will have the same SHAs for each repository that needs to be patched (so phet-core A and scenery B will not be grouped with sims that use scenery C). NOTE: If you want to apply the same patch to phet-core A (that works with Scenery B and C), just save the SHA used for the first case, and check it out as the fix in the future cases.

For each group, the process helps you check out SHAs so you can apply the changes/test them. Once you are satisfied, it will be able to automatically apply the commits to branches as necessary (and create them if needed), and will update dependencies.json.

For example, it would be able to update the 'acid-base-solutions-1.1' branch in phetcommon AND create a 'acid-base-solutions-1.1' branch in Scenery automatically, and then those SHAs would be included in the dependencies.json in acid-base-solutions' 1.1 branch.

Once this is done for each patch/fix (and for each of those, each group of sims), it provides support for RC and production deployment.

Note that currently I'm recommending the debug flag (```--debug```), since this prints out more information in case something unexpected happens.

Pseudo-code for the below process:
```
grunt --debug maintenance-start --sims=<list of sims, comma separated>
for each ( fix in fixes to be applied ) {
  repositoryList = the repositories affected by the expected patches, comma-separated.
  grunt --debug maintenance-patch-info --repos=<repositoryList>
  for each ( shaList in maintenance-patch-info output ) {
    grunt --debug maintenance-patch-checkout --repos=<repositoryList> --shas=<shaList>
    // apply fix commit(s) to common repos, e.g. git cherry-pick -x <patch>
    grunt --debug maintenance-patch-apply --repos=<repositoryList> --message=<issue(s) for patch>
  }
}
for each ( simulation that is fully patched ) {
  while ( hasn't passed testing ) {
    grunt --debug maintenance-deploy-rc --sim=<simulation> --message=<issue(s) for patches/deploy>
  }
  grunt --debug maintenance-deploy-production --sim=<simulation> --message=<issue(s) for patches/deploy>
}
```

## Steps

### 1. maintenance-start

Given a list of simulations, you'll want to run the maintenance-start task. This will check current production versions of the simulations, and will store this information for future tasks.

For example:
```sh
grunt --debug maintenance-start --sims=acid-base-solutions,arithmetic,balancing-chemical-equations,balloons-and-static-electricity,beers-law-lab,bending-light,color-vision,concentration,faradays-law,friction,graphing-lines,hookes-law,molarity,molecule-shapes,molecule-shapes-basics,molecules-and-light,neuron,ohms-law,ph-scale,ph-scale-basics,reactants-products-and-leftovers,trig-tour,wave-on-a-string
```

This will also print out a list of current sim versions (from which it will extract maintenance release branch names, etc.):
```
acid-base-solutions/1.2.2
arithmetic/1.0.2
balancing-chemical-equations/1.1.2
balloons-and-static-electricity/1.1.0
beers-law-lab/1.3.3
bending-light/1.0.1
color-vision/1.1.1
concentration/1.2.2
faradays-law/1.1.2
friction/1.2.3
graphing-lines/1.1.2
hookes-law/1.0.2
molarity/1.2.2
molecule-shapes/1.1.3
molecule-shapes-basics/1.1.1
molecules-and-light/1.1.2
neuron/1.0.0
ohms-law/1.3.0
ph-scale/1.2.2
ph-scale-basics/1.2.2
reactants-products-and-leftovers/1.1.2
trig-tour/1.0.1
wave-on-a-string/1.1.0
```

NOTE: Do not re-run this when partially through the process! It overwrites metadata for the maintenance release, and
should just be used for starting it off.

### 2. For each fix

A series of steps should be done for every standalone patch.

#### 2a. maintenance-patch-info

For the given repository (or repositories) that need to be included with the patch, running ```grunt maintenance-patch-info```  will print out SHA information for all of the simulations (and store it for future use).

For example:
```sh
grunt --debug maintenance-patch-info --repos=phetcommon
```

This will print out SHAs of the repositories for each simulation, and also will print out a report about which simulations share SHA combinations, e.g.:
```
Map for phetcommon

85b70897a659e03af24c5ef6293b263e78205e27
  acid-base-solutions
  beers-law-lab
  concentration
  faradays-law
d712ace0fd0fa47ab617934aec8721228aefc0fc
  arithmetic
  bending-light
  molecule-shapes
  molecule-shapes-basics
  neuron
20ce6f04ef6406acce29d91cad5e8dc457dc38a4
  balancing-chemical-equations
  graphing-lines
  reactants-products-and-leftovers
35c2abc1378ec6a00435124922a360b721576a72
  balloons-and-static-electricity
  color-vision
  ohms-law
d9e99f253599e63794fd12ff5fdb3a993b5fef27
  friction
  hookes-law
  molarity
  molecules-and-light
5d2e53a961c1587e5b582a833a849edfc0beeafb
  ph-scale
  ph-scale-basics
3db92af30d53b7d6bb3ce3c47c632f622f17986c
  trig-tour
68270b86c92ddd0af0cca1885cd750d9c857796c
  wave-on-a-string
```

It's important to store this list, as we'll want to patch each SHA independently with the following process.

NOTE: It is recommended to avoid re-running this halfway-through patching, as it will show the new SHAs for the sims you have already patched, and will prevent maintenance-patch-checkout on older SHAs.

#### 2b. For each SHA (combination)

We'll want to apply patches to each SHA (or SHA combination) separately. For example, we'll tackle the 85b70897a659e03af24c5ef6293b263e78205e27 sha from above, which is used by 4 simulations.

##### 2b(i). maintenance-patch-checkout

This command will check out testable SHAs for one of the simulations (pass a ```--sim=simName``` if you want to test a particular one). Pass in the SHA combination from the list above.

```sh
grunt --debug maintenance-patch-checkout --repos=phetcommon --shas=85b70897a659e03af24c5ef6293b263e78205e27
```

This requires that maintenance-patch-info was run with the repository list provided AND that the SHA combination was from that list.

##### 2b(ii). Create commits on the common repositories

Now, time to apply our patch. We will commit on top of detached HEAD(s), and this is fine (the maintenance release scripts will add our orphaned commit to the relevant branches).

A quick way to do this for simple changes is to try cherry-picking. In this example case, I only had to go to phetcommon and type:
```sh
git cherry-pick -x 380b1fb5f15d097133bfceaf119d3eaf40a3a2d4
```

and it applies the fix I need directly to the code. Make sure you aren't left in a merge/conflict state!

However you patch things, there should now be new commit(s) on the common repositories that you're patching.

##### 2b(iii) maintenance-patch-apply

This will read the current SHA(s) in the common repositories, and for each simulation in that SHA's group it will merge it into its branch (or create a new branch). This will ensure that for (in our example phetcommon), it will have an acid-base-solutions-1.2 branch pointed to the correct commit.

Additionally, it will include this fix in the dependencies.json on the maintenance release branch.

For example:
```sh
grunt --debug maintenance-patch-apply --repos=phetcommon --message="https://github.com/phetsims/chipper/issues/429"
```

In the example, it creates or updates (merges) the branches in phetcommon (acid-base-solutions-1.2, beers-law-lab-1.3, concentration-1.2, and faradays-law-1.1), builds each sim, and includes the latest-built dependencies.json on their respective branches (i.e. acid-base-solutions branch 1.2 will have updated dependencies.json).

NOTE: The actual commit message will be ```'Bumping dependencies.json for ' + message```

### 3. Deploying RCs (release candidates)

NOTE: Please set up SSHs to spot so that interactive password/passphrase/etc. is not needed. This has been tested with:
```sh
exec ssh-agent bash
```
to ensure interactive credential input isn't needed.

Once all of the patches are applied (or even some), you can kick off an RC deployment, for example:
```sh
grunt --debug maintenance-deploy-rc --sim=acid-base-solutions --message="https://github.com/phetsims/chipper/issues/429"
```

This will handle incrementing the version number as necessary (e.g. 1.0.0 => 1.0.1-rc.1, 1.0.1-rc.1 => 1.0.1-rc.2, etc.), and can be included in a bash loop for many simulations (recommend testing one first).

Typically, after RCs, you'll want to create a tasks issue that specifies both "~30 second check to make sure the sim works" and additionally checks the specific behavior that you are patching (if applicable), or you'll want to verify it yourself.

NOTE: Some older chippers don't flag "deployment failure" as something that prints an error message.

NOTE: The actual commit message will be ```'Bumping version to ' + newVersionString + ' for ' + message```

### 4. Deploying to production

NOTE: Please set up SSHs to spot so that interactive password/passphrase/etc. is not needed. This has been tested with:
```sh
exec ssh-agent bash
```
to ensure interactive credential input isn't needed.

Once the brief testing is complete, sims can be pushed to production. It's similar to the RC deployment, for example:
```sh
grunt --debug maintenance-deploy-production --sim=acid-base-solutions --message="https://github.com/phetsims/chipper/issues/429"
```

It will also bump the version (and will fail out if the version is NOT an RC version).

NOTE: Some older chippers don't flag "deployment failure" as something that prints an error message.

NOTE: The actual commit message will be ```'Bumping version to ' + newVersionString + ' for ' + message```

## Dealing with problems

Generally, see where the problem occurred in the maintenance release task that was run. The most general "routine" for this is:

1. Check what's currently checked out. May have detached HEADs checked out. ```grunt checkout-master-all``` in perennial can help here.
2. Check what has been committed to the repositories (Do the sim-specific branches on common repos exist, and are they correct? Do the release branches on the sim repos contain correct dependencies.json entries?)
3. Correct the above, and continue, or contact @jonathanolson if you have concerns.

If no patches have been applied (not yet done with 2b(ii)), you can restart at 'maintenance-start'.

If you need to re-deploy an RC where the deployment failed (but version push worked), use 'maintenance-deploy-rc-no-version-bump' (could be refactored in the future).

If you need to re-deploy to production where it failed (but version push worked), use perennial's checkout-shas as usual, and do it manually.

