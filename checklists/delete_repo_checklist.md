# Delete/Archive Repo Checklist

## Before using this checklist:
Decide whether the repo is being (a) deleted (b) archived or (c) removed from active-repos.
- A repo should be deleted if
  * it is clutter
  * it will never be used again
  * there is no valuable information in the GitHub issues
  * it is not referenced by any SHA in any published simulation
- A repo should be archived if
  * we don't want to continue development on the repo, but it needs to stay for reference or because its SHAs are used.
  * We want a paper trail for issues/decisions/commits made in the repo.
  * you may also want to make it private, if it should not be used for reference by 3rd parties
- A repo should be removed from active-repos if
  * We cannot maintain it at the moment, but we expect to bring it back into maintenance in the future.

## Do not remove repos that:
- Are listed as dependencies of any published simulation.
- Would prevent checking out old versions of sims (do not mess with the bisection).
- Contain otherwise useful information that is linked to

## Deleting or Archiving Steps
- [ ] Before deleting something, it should be approved for deletion at a dev meeting
- [ ] If not confident about some of the above questions/advice, bring it to a dev meeting
- [ ] Create a delete/archive repo github issue in special-ops.
- [ ] Inform the dev team to delete their local copy (perhaps put a checklist of developers in the github issue)
- [ ] If issues crop up they should be documented in the associated github issue for the dev responsible for deletion
- [ ] The repo should be removed from active-repos, ideally a few minutes before archiving/deleting (so automated processes do not try to pull it)
- [ ] In general, removing the repo should not break much, if empty rows in CT are a concern,restart CT
- [ ] If archiving, update the repo's README.md file to indicate why it is archived
- [ ] Remove from chipper/tsconfig/all/tsconfig.json (if present)

We should explicitly state whether something needs to be done to delete the directory from aqua, build-server, and phettest, or whether these directories get automatically deleted, or just hang around forever with no consequences
