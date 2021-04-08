#!/bin/bash

# delete-label.sh
#
# This script removes the label from all repos

if [[ $1 = '' ]]
then
    echo "Usage: $0 label-name"
    exit 1
else
    label=$1
    echo "$label"
fi

binDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
creds=`node ${binDir}/printGithubAuthorization.js`

node ./update-repos-list.js

echo 'For each repo, this script should print "204 No Content" to indicate success'

for repo in `cat .repos`
do
    repo=`echo ${repo}`
    url=https://api.github.com/repos/phetsims/${repo}/labels/${label}
    echo "Path: ${url}"
    echo "Result:"
    curl -isH 'User-Agent: "phet"' -u "$creds" -X DELETE ${url} | head -n 1
done

sed -n /${ppp}/'!p' github-labels > .tmp && mv .tmp github-labels
sort github-labels -o github-labels
git pull && git commit github-labels -m "Removed github label ${label}" && git push

echo "Complete."

