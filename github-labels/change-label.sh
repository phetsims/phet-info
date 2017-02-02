#!/bin/bash

# This script replaces the color and/or text of a github label for all phetsims organization repositories.
#
#
# .credentials is a file with your github creds in the format username:password

# This could probably be replaced with oAuth
CREDS=`cat ~/.phet/.credentials`
if [[ "$CREDS" = "" ]]
then
  echo "Requires .credential file"
  exit 1
fi

if [[ $1 = '' ]] || [[ $2 = '' ]] || [[ $3 = '' ]]
then
  echo "Usage: $0 old-label-name new-label-name new-color"
  exit 1
else
  NEW={\"name\":\"$2\",\"color\":\"$3\"}
  OLD=$1
  echo "$LABEL"
fi



for r in `jq -c .[].name phetsims-repos.json`
do
  REPO=`echo phetsims/$r | tr -d '"'`
  echo "$REPO"
  URL=https://api.github.com/repos/$REPO/labels
  echo "$URL"
  curl -iH 'User-Agent: "PhET"' -u "$CREDS" -d "$NEW" "$URL/$OLD"
done
