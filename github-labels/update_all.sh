#!/bin/bash

# .credentials is a file with your github creds in the format username:password
# This should probably be replaced with oAuth
CREDS=`cat .credentials`
if [[ "$CREDS" = "" ]]
then
  echo "Requires .credential file"
  exit 1
fi

if [[ $1 = '' ]] || [[ $2 = '' ]]
then
  echo "Usage: $0 \"labelName\" \"color(hexcode with no # symbol)\""
  exit 1
else
  LABEL={\"name\":\"$1\",\"color\":\"$2\"}
  echo "$LABEL"
fi

for r in `~/jq-win64.exe -c .[].name phetsims-repos.json`
do
  REPO=`echo phetsims/$r | tr -d '"'`
  echo "$REPO"
  URL=https://api.github.com/repos/$REPO/labels
  echo "$URL"
  curl -iH 'User-Agent: "phet"' -u "$CREDS" -d "$LABEL" "$URL"
done
