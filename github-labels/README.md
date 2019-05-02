## Updating Github Repo Labels

### NOTE: The `.phet/.credentials` file is no longer required.
This file is not used anywhere else in the project and may be safely removed.  Instead, you are asked for your credentials in an interactive prompt.  While slightly
inconvenient this is far more secure.

#### To standardize the labels on a new repo
1. Run `./new-repo-add-labels.sh phetsims/{{new-repo-name}}`

#### To add a new label to all the organization's repos
1. Choose a new label following the [labeling-scheme](labeling-scheme.md)
2. Run `./new-label-all-repos.sh {{new-label-name}} {{new-label-color}}`.  `new-label-color` should be the hexcode with no #
symbol, e.g. FF00AA.

#### To change the text and/or color of a label
1. Update the desired lable, following the [labeling-scheme](labeling-scheme.md)
2. Run `./change-label.sh {{old-label-name}} {{new-label-name}} {{new-label-color}}`.  `new-label-color` should be the
hexcode with no # symbol, e.g. `FF00AA`.

#### To remove a label from all repos
2. Run `./delete-label.sh {{label-name}}`.

### FAQ

* #### Why do we need the list of repos in github-labels/, could the script just depend on perennial/data/active-repos instead?

    We do need two lists, because there are active repos missing from "active-repos". There are some repos, like website, which are active but very large and not collaborated on by all team members. Because active-repos is shared by the clone-missing-repos script, this creates a significant inconvenience in terms of storage.
