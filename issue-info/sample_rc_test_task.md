(*@ mention the appropriate parties, including designers*), [Sim Name] 1.X.X-rc.X is ready for RC testing.

**[Link to sim](http://www.colorado.edu/physics/phet/dev/html/sim-name/1.0.0-rc.1/sim-name.html)**

**[Link to iFrame](http://www.colorado.edu/physics/phet/dev/html/sim-name/1.0.0-rc.1/sim-name-iframe.html)**

**[Test Matrix](https://docs.google.com/spreadsheets/d/1nrGez8Z4HXelhgDXNkfVAd_qxWiC5z0nnG3a8Dzxwlc/edit?ts=573a195e#gid=2)**

**Issues to Verify**
(*all should be marked "status:fixed-pending-testing"*)  
Please test the following issues and check them off after addressing. If they are resolved, close them.  If not, they should be updated.

- [ ] https://github.com/phetsims/repo-name/issues/##
- [ ] https://github.com/phetsims/repo-name/issues/##
- [ ] https://github.com/phetsims/repo-name/issues/##
- [ ] https://github.com/phetsims/repo-name/issues/##


**Please also verify**
- [ ] stringTest=double (all strings doubled)
- [ ] stringTest=long (exceptionally long strings)
- [ ] stringTest=X (short strings)
- [ ] stringTest=rtl (right-to-left)
- [ ] stringTest=xss (test passes if sim does not redirect, OK if sim crashes or fails to fully start)
- [ ] showPointerAreas (touchArea=red, mouseArea=blue)
- [ ] Full screen test
- [ ] Screenshot test

If any new issues are found, please note them in https://github.com/phetsims/repo-name/issues and reference this issue.  

 
**(Other potentially useful items)**  

Sim-specific query parameters useful for testing:  
(*examples from function builder*)  
• `?populateOutput` - puts 1 of each card in the output carousel  
• `?slow` - reduces animation speed to 25% of normal, useful for testing multitouch  

Sim-specific terminology:  
(*examples from function builder*)  
• builder - the apparatus in the center of the screen  
• slots - places where you can drop functions in the builder  
• input carousel - vertical carousel on the left  
