#!/bin/bash

# .credentials is a file with your github creds in the format username:password
# This should probably be replaced with oAuth
CREDS=`cat ~/.credentials`
if [[ "$CREDS" = "" ]]
then
  echo "Requires .credential file"
  exit 1
fi

#REPO should be in the format "organization/repo"
#REPO="phetsims/friction"
if [[ $1 -eq '' ]] 
then
  echo "Usage: $0 organization/repo"
else

  REPO=$1
  URL=https://api.github.com/repos/$REPO/labels


  #delete the "invalid" label
  curl -iH 'User-Agent: "PhET"' -u "$CREDS" -X "DELETE" "$URL/invalid"

  # Replace standard-issue labels with phet-specific labels if they exist
  REPLACE='{
      "name": "type:wontfix",
      "color": "ffffff"
    }'
  curl -iH 'User-Agent: "PhET"' -u "$CREDS" -d "$REPLACE" "$URL/wontfix"

  REPLACE='{
      "name": "type:question",
      "color": "EDCB62"
    }'
  curl -iH 'User-Agent: "PhET"' -u "$CREDS" -d "$REPLACE" "$URL/question"

  REPLACE='{
      "name": "dev:help-wanted",
      "color": "63D1F4"
    }'
  curl -iH 'User-Agent: "PhET"' -u "$CREDS" -d "$REPLACE" "$URL/help%20wanted"

  REPLACE='{
      "name": "dev:enhancement",
      "color": "0276FD"
    }'
  curl -iH 'User-Agent: "PhET"' -u "$CREDS" -d "$REPLACE" "$URL/enhancement"

  REPLACE='{
      "name": "type:duplicate",
      "color": "EEEED1"
    }'
  curl -iH 'User-Agent: "PhET"' -u "$CREDS" -d "$REPLACE" "$URL/duplicate"

  REPLACE='{
      "name": "type:bug",
      "color": "FF00AA"
    }'
  curl -iH 'User-Agent: "PhET"' -u "$CREDS" -d "$REPLACE" "$URL/bug"

  #Add labels from JSON file
  for label in `jq -c .[] github-labels.json`
  do
    curl -iH 'User-Agent: "PhET"' -u "$CREDS" -d "$label" "$URL"
  done
fi



