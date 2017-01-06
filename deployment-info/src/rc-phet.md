
## Publishing an 'rc' (release candidate) version (PhET brand)

The latest fully-tested SHAs (use these if appropriate): https://github.com/phetsims/states-of-matter/blob/1.0/dependencies.json

The latest SHAs under testing (use these if appropriate): https://github.com/phetsims/states-of-matter/blob/1.0/dependencies.json

RC versions are deployed to spot.colorado.edu at http://www.colorado.edu/physics/phet/dev/html/

If this is the first release candidate on a release branch:

- [ ] Create a release branch and switch to it, e.g.: `git checkout -b 1.0`. The branches are named using major and minor version numbers, eg "1.0".

If this is not the first release candidate on a release branch:

- [ ] Check out the release branch, e.g.: `git checkout 1.0`
- [ ] Check out the correct shas for dependencies: `grunt checkout-shas`
- [ ] Run `npm update` in the sim repo and in chipper
- [ ] If you are making a maintenance release, then you will have to branch that repo to perform the fix. To do so, name the branch
 after the sim and version you are performing the maintenance release on. For example, if you branched vegas for the 1.1 
 release of graphing-lines, the branch name in vegas will be graphing-lines-1.1.

After setting up the release-candidate branches, continue the build and deploy:

- [ ] Update the version identifier in package.json, commit and push. The version should be something like "1.0.0-rc.2".
- [ ] Push your changes to github.
- [ ] Run the build process: `grunt`
- [ ] Deploy to spot using the build server: `grunt deploy-rc`
- [ ] Test the deployed RC on spot to make sure it is working properly. 
    * If the build server is having issues, you can ssh into phet and look at the build-server logs with: `sudo journalctl -fu build-server`. 
    * Launch the sim and make sure it is working correctly.
- [ ] After following these steps, please update the "latest SHAs under testing" above, if appropriate.
- [ ] Check out master for dependencies: `grunt checkout-master` (optional)
