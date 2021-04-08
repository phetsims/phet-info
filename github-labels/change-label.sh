#!/bin/bash

# change-label.sh
#
# This script replaces the color and/or text of a github label for all repos

if [[ $1 = '' ]] || [[ $2 = '' ]] || [[ $3 = '' ]]
then
  echo "Usage: $0 old-label-name new-label-name new-color"
  exit 1
else
  oldLabel=$1
  newLabel=$2
  newColor=$3
  new={\"new_name\":\"${newLabel}\",\"color\":\"${newColor}\"}
fi

binDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
creds=`node ${binDir}/printGithubAuthorization.js`
node ./update-repos-list.js

echo 'For each repo, this script should print "200 OK" to indicate success'
echo 'If a 404 Not Found is printed, that repo is likely missing the standard label set.'
echo 'If a 403 Forbidden is printed, that repo has probably been archived and this is correct.  If you believe the repo should have been updated, check that your Github OAuth token is correct.'
echo ''

for repo in `cat .repos`
do
  repo=`echo ${repo}`
  url=https://api.github.com/repos/phetsims/${repo}/labels/${oldLabel}
  echo "Path: ${url}"
  echo "Data: ${new}"
  echo "Result:"
  curl -isH 'User-Agent: "PhET"' -u "$creds" -d "$new" -X PATCH "$url" | head -n 1
  echo ''
done

sed s/${oldLabel}.*/${newLabel},${newColor}/ github-labels > .tmp && mv .tmp github-labels
sort github-labels -o github-labels
git pull && git commit github-labels -m "Changed github label from ${oldLabel} to ${new}" && git push

echo "Complete."