**Steps to publish a 'rc' (release candidate) version**

The latest fully-tested SHAs (use these if appropriate): https://github.com/phetsims/atomic-interactions/blob/1.0/dependencies.json

The latest SHAs under testing (use these if appropriate): https://github.com/phetsims/forces-and-motion-basics/blob/2.1/dependencies.json

RC versions are deployed to spot.colorado.edu at http://www.colorado.edu/physics/phet/dev/html/

If this is the first release candidate on a release branch:

- [ ] Create a release branch and switch to it, e.g.: `git checkout -b 1.0`. The branches are named using major and minor version numbers, eg "1.0".

If this is not the first release candidate on a release branch:

- [ ] Check out the release branch, e.g.: `git checkout 1.0`
- [ ] Check out the correct shas for dependencies: `grunt checkout-shas`
- [ ] If you've branched (for the purposes of patching) any of the dependency repositories since the last rc version was
published, you'll need to explicitly checkout those branches. For example, if you branched vegas for the 1.1 release of
graphing-lines, do `cd ../vegas ; git checkout graphing-lines-1.1`.

After setting up the release-candidate branches, continue the build and deploy:

- [ ] Update the version identifier in package.json, commit and push. The version should be something like "1.0.0-rc.2".
- [ ] Run the build process: `grunt`
- [ ] Deploy to spot using the build server: `grunt deploy-rc`
- [ ] Test the deployed RC on spot to make sure it is working properly. If the build server is having issues,
you can ssh into phet and look at the build-server logs with: `sudo journalctl -fu build-server`. Launch the sim and make sure it is working correctly.
- [ ] After following these steps, please update the "latest SHAs under testing" above, if appropriate.
- [ ] Check out master for dependencies: `grunt checkout-master` (optional)
