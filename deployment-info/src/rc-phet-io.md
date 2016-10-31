
## Publishing an 'rc' (release candidate) version (PhET-iO brand)

NOTE: as of 10/31/16 phet-io testing is in flux, so we are constantly using master to build.
The latest fully-tested SHAs (use these if appropriate): 

The latest SHAs under testing (use these if appropriate): 

TODO: should the following sentence go in rc-phet.md also?
Keep in mind these SHAs may not include all of the repos for your sim, 
but you can still overwrite your dependencies with them, and the rest will be filled in with master during the build.

RC versions are deployed to spot.colorado.edu at http://www.colorado.edu/physics/phet/dev/html/

If this is the first release candidate on a release branch:

- [ ] Create a release branch and switch to it, e.g.: `git checkout -b 1.0-phetio`. The branch name should include "phetio", such as "1.1-phetio"

If this is not the first release candidate on a release branch:

- [ ] Check out the release branch, e.g.: `git checkout 1.1-phetio`

Now if this is is not the first release, or you are using trusted shas above:

- [ ] Check out the correct shas for dependencies: `grunt checkout-shas`

- [ ] If you've branched (for the purposes of patching) any of the dependency repositories since the last rc version was
published, you'll need to explicitly checkout those branches. For example, if you branched vegas for the 1.1 release of
graphing-lines, do `cd ../vegas ; git checkout graphing-lines-1.1`.

After setting up the release-candidate branches, continue the build and deploy:


- [ ] If you are using the trusted shas from above, copy them into `dependencies.json`
- [ ] Update the version identifier in package.json, commit and push. The version should be something like "1.0.0-rc.2".
The build process will automatically insert the substring `phetio` after the hyphen, so it will be deployed e.g., as 1.0.0-phetiorc.2. 
If you don't do this step deploying to spot will not work, as there will already be that version's folder.
- [ ] Push your changes to github.
- [ ] Run the build process: `grunt --brand=phet-io`
- [ ] Deploy to spot using the build server: `grunt deploy-rc --brand=phet-io`
- [ ] Test the deployed RC on spot to make sure it is working properly. If the build server is having issues,
you can ssh into phet and look at the build-server logs with: `sudo journalctl -fu build-server`
 * PhET Brand: Launch the sim and make sure it is working correctly.
 * PhET-iO Brand: please see the "PhET-iO Testing after deployment" section below
- [ ] After following these steps, please update the "latest SHAs under testing" above, if appropriate.  Keep in mind
that not all sims use all repos.
- [ ] Check out master for dependencies: `grunt checkout-master` (optional)
