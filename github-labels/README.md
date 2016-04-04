##Updating Github Repo Labels

######Requirements
+ Create a .credentials file in this directory in the format gitHubUsername:gitHubPassword
+ (Do not add this file to the git repo)
+ Install `jq` - https://stedolan.github.io/jq/


####To standardize the labels on a new repo
1. Add the new repo name to [phetsims-repos.json](phetsims-repos.json)
2. Run `./add-labels phetsims/newRepoName`, replacing newRepoName.

####To add a new label to all the organization's repos
1. Following the [labeling-scheme](labeling-scheme.md), add the new label to [github-labels.json](github-labels.json).
2. Run `./update_all.sh '{"name":"newLabelName","color":"newLabelColor"}'`, replacing newLabelName and newLabelColor
