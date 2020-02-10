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
  new={\"name\":\"${newLabel}\",\"color\":\"${newColor}\"}
fi

binDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
creds=`node ${binDir}/printGithubAuthorization.js`
./update-repos-list.sh

echo 'For each repo, this script should print "200 OK" to indicate success'

for repo in `cat .repos`
do
  repo=`echo ${repo}`
  url=https://api.github.com/repos/phetsims/${repo}/labels/${old}
  echo "Path: ${url}"
  echo "Data: ${new}"
  echo "Result:"
  curl -isH 'User-Agent: "PhET"' -u "$creds" -d "$new" -X PATCH "$url" | head -n 1
done

sed s/${oldLabel}.*/${newLabel},${newColor}/ github-labels > .tmp && mv .tmp github-labels
sort github-labels -o github-labels
git pull && git commit github-labels -m "Changed github label from ${old} to ${new}" && git push

echo "Complete."