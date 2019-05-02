#!/bin/bash

# update_all.sh
#
# This file adds a new label to all repos in phetsims-repos
# The user must add the new label to the github-labels file manually
#
# TODO: automatically update github-labels when this script is run

if [[ $1 = '' ]] || [[ $2 = '' ]]
then
  echo "Usage: $0 label-name color"
  exit 1
else
  label={\"name\":\"$1\",\"color\":\"$2\"}
  echo "$label"
fi

read -p "Github Username: " username
read -sp "Github Password: " password
echo ''
creds=${username}:${password}

update-repos-list.sh ${username} ${password}

echo 'For each repo, this script should print "201 Created" to indicate success"'

for repo in `cat .repos`
do
  repo=`echo ${repo}`
  url=https://api.github.com/repos/phetsims/$repo/labels
  echo "Path: ${url}"
  echo "Data: ${label}"
  echo "Result:"
  curl -isH 'User-Agent: "phet"' -u "$creds" -d "$label" -X POST "$url" | head -n 1
done

echo ${label},${color} >> github-labels
sort github-labels -o github-labels
git pull && git commit github-labels -m "Added github label from ${label}" && git push

echo "Complete."
