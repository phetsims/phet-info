#!/bin/bash

# change-label.sh
#
# This script replaces the color and/or text of a github label for all repos in phetsims-repos
# The color and text need to be updated manually in github-labels
#
# TODO: automatically update github-labels when this script is run

if [[ $1 = '' ]] || [[ $2 = '' ]] || [[ $3 = '' ]]
then
  echo "Usage: $0 old-label-name new-label-name new-color"
  exit 1
else
  new={\"name\":\"$2\",\"color\":\"$3\"}
  old=$1
fi

read -p "Github Username: " username
read -sp "Github Password: " password
echo ''
creds=${username}:${password}

echo 'For each repo, this script should print "200 OK" to indicate success'

for repo in `cat phetsims-repos`
do
  repo=`echo ${repo}`
  url=https://api.github.com/repos/phetsims/${repo}/labels/${old}
  echo "Path: ${url}"
  echo "Data: ${new}"
  echo "Result:"
  curl -isH 'User-Agent: "PhET"' -u "$creds" -d "$new" -X PATCH "$url" | head -n 1
done

echo "Complete. Don't forget to update the label in the github-labels file"