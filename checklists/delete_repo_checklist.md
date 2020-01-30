# Draft Delete Repo Checklist

## Before using this checklist:
Decide whether the repo is being deleted or archived. 
- A repo should be deleted if...
- A repo should be archived if...

## Do not remove repos that:
- Are listed as dependencies of any published simulation. 
- Would prevent  checking out old versions of sims (do not mess with the bisection). 
- Contain otherwise useful information that is linked to

## Deleting or Archiving Steps
- [ ] If not confident about some of the above questions/advice, bring it to a dev meeting
- [ ] Create a delete/archive repo github issue in? (perhaps in tasks) 
- [ ] Inform the dev team to delete their local copy (perhaps put a checklist of developers in the github issue)
- [ ] If issues crop up put them in the associated github issue and inform the dev responsible for deletion
- [ ] The repo should be removed from active-repos, ideally a few minutes before archiving/deleting (so automated processes don't try to pull it)
  
    
We should explicitly state whether something needs to be done to delete the directory from aqua, build-server, and phettest, or whether these directories get automatically deleted, or just hang around forever with no consequences
  
- [ ] If archiving, update the README file 
