## Updating Github Repo Labels

###### Requirements
+ Create a .phet/.credentials file to your home directory.  The contents should be gitHubUsername:gitHubPassword
+ (Do not add this file to the git repo)
+ Download the jq executable from https://stedolan.github.io/jq/ and configure it to run from your path with the command `jq`.
  + On windows for example, I renamed the downloaded file to jq.exe, put it in this folder: C:\Users\username\phet, and added that folder to my PATH environment variable in System Properties.


#### To standardize the labels on a new repo
1. Add the new repo name to [phetsims-repos.json](phetsims-repos.json)
2. Run `./add-labels.sh phetsims/{{new-repo-name}}`


#### To add a new label to all the organization's repos
1. Following the [labeling-scheme](labeling-scheme.md), add the new label to [github-labels.json](github-labels.json).
2. Run `./update_all.sh {{new-label-name}} {{new-label-color}}`.  new-label-color should be the hexcode with no # symbol, e.g. FF00AA.
