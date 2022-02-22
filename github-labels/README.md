# Updating Github Repo Labels

#### NOTE: The `.phet/.credentials` file is no longer required.
This file is not used anywhere else in the project and should be removed. We are now storing credentials in build-local.json. See Getting Started for details.

## Getting Started

1. Setup credentials 
    - You must add the developerGithubAccessToken and developerGithubUsername properties to ~/.phet/build-local.json.  See
https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line#creating-a-token
for creating a personal access token. Under "Select Scopes", the token should be given full "repo" access.
2. Install npm packages 
    - The node scripts in this repo require running `npm install` in the phet-info/github-labels directory.

## PhET Github Label operations

### To standardize the labels on a new repo
1. Run `./new-repo-add-labels.sh phetsims/{{new-repo-name}}`

### To add a new label to all the organization's repos
1. Choose a new label following the [labeling-scheme](labeling-scheme.md)
2. Run `./new-label-all-repos.sh {{new-label-name}} {{new-label-color}}`.  `new-label-color` should be the hexcode with no #
symbol, e.g. FF00AA.

### To change the text and/or color of a label
1. Update the desired label in [github-labels](github-labels), following the [labeling-scheme](labeling-scheme.md)
2. Run `./change-label.sh {{old-label-name}} {{new-label-name}} {{new-label-color}}`.  `new-label-color` should be the
hexcode with no # symbol, e.g. `FF00AA`.

### To remove a label from all repos
2. Run `./delete-label.sh {{label-name}}`.

## FAQ

* ### Error statuses during label script execution

    * __200, 201, etc__ - Anything in the 200 range indicates success.
    * __400 Bad Request__ - This probably indicates a fatal error. Verify if the change did not happen as expected and contact the responsible dev if not (Matt Pennington as of 2020).
    * __401 Unauthorized__ - This indicates that your credentials are incorrect.  Make sure your username and personal access token are entered in ~/.phet/build-local.json correctly and check the status of your PAT at https://github.com/settings/tokens.
    * __403 Forbidden__ - This indicates that the Github User that you used does not have admin access for that repo.  Make sure your username and personal access token are entered in ~/.phet/build-local.json correctly and contact any PhET Github Admin for further assistance.
    * __422 Unprocessable Entity__ - This is probably __*not*__ an error and most likely indicates that the script attempted a duplicate action. Verify if the change did not happen as expected and contact the responsible dev if not (Matt Pennington as of 2020).
