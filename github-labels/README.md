#Updating Github Repo Labels

####Requirements
+ Scripts are run from a linux terminal - requires use of `curl`
+ Install `jq` - https://stedolan.github.io/jq/


###To standardize the labels on a new repo
1. Add the new repo name to phetsims-repos.json
2. Run `./add-labels phetsims/newRepoName`

###To add a new label to all the organizations repos
1. Add the new label to github-labels.json
2. Run `./update_all.sh '{"name":"newLabelName","color":"newLabelColor"}`