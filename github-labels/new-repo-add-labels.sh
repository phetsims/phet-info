#!/bin/bash

# new-repo-add-labels.sh
#
# This script adds all labels in github-labels to the specified repo

if [[ -z "$1" ]]
then
  echo "Usage: $0 organization/repo"
  exit 1
fi
echo $1

binDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
creds=`node ${binDir}/printGithubAuthorization.js`

node ./update-repos-list.js

echo 'For each repo, this script should print "200 OK", "201 Created" or "204 No Content" to indicate success.'
echo '"422 Unprocessable Entity" indicates an attempt to duplicate a label and can be ignored.'

repo=$1
url=https://api.github.com/repos/${repo}/labels


#delete the "invalid" label
echo "Path: ${url}/invalid"
echo "Result (204 expected):"
curl -isH 'User-Agent: "PhET"' -u "$creds" -X DELETE "$url/invalid" | head -n 1

# Replace standard-issue labels with phet-specific labels if they exist
replace='{
  "name": "type:wontfix",
  "color": "ffffff"
}'
echo "Path: ${url}/wontfix"
echo "Data: ${replace}"
echo "Result (200 expected):"
curl -isH 'User-Agent: "PhET"' -u "$creds" -d "$replace" -X PATCH "$url/wontfix" | head -n 1

replace='{
  "name": "type:question",
  "color": "EDCB62"
}'
echo "Path: ${url}/question"
echo "Data: ${replace}"
echo "Result (200 expected):"
curl -isH 'User-Agent: "PhET"' -u "$creds" -d "$replace" -X PATCH "$url/question" | head -n 1

replace='{
  "name": "dev:help-wanted",
  "color": "63D1F4"
}'
echo "Path: ${url}/20wanted"
echo "Data: ${replace}"
echo "Result (200 expected):"
curl -isH 'User-Agent: "PhET"' -u "$creds" -d "$replace" -X PATCH "$url/help%20wanted" | head -n 1

replace='{
  "name": "dev:enhancement",
  "color": "0276FD"
}'
echo "Path: ${url}/enhancement"
echo "Data: ${replace}"
echo "Result (200 expected):"
curl -isH 'User-Agent: "PhET"' -u "$creds" -d "$replace" -X PATCH "$url/enhancement" | head -n 1

replace='{
  "name": "type:duplicate",
  "color": "EEEED1"
}'
echo "Path: ${url}/duplicate"
echo "Data: ${replace}"
echo "Result (200 expected):"
curl -isH 'User-Agent: "PhET"' -u "$creds" -d "$replace" -X PATCH "$url/duplicate" | head -n 1

replace='{
  "name": "type:bug",
  "color": "FF00AA"
}'
echo "Path: ${url}/bug"
echo "Data: ${replace}"
echo "Result (200 expected):"
curl -isH 'User-Agent: "PhET"' -u "$creds" -d "$replace" -X PATCH "$url/bug" | head -n 1

#Add labels from file
for label in `cat github-labels`
do
name=`echo ${label} | cut -f1 -d,`
color=`echo ${label} | cut -f2 -d,`
json="{\"name\":\"$name\",\"color\":\"$color\"}"
echo "Path: ${url}"
echo "Data: ${json}"
echo "Result (201 expected):"
curl -isH 'User-Agent: "PhET"' -u "$creds" -d "$json" -X POST "$url" | head -n 1
done

echo "Complete."


