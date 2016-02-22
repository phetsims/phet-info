#!/bin/bash

# .credentials is a file with your github creds in the format username:password
# This should probably be replaced with oAuth
CREDS=`cat .credentials`
if [[ "$CREDS" = "" ]]
then
  echo "Requires .credential file"
  exit 1
fi

if [[ $1 -eq '' ]] 
then
  echo "Usage: $0 '{\"name\":\"labelName\",\"color\":\"hexcode\"}'"
else

  REPO=$1

for r in `~/jq-win64.exe -c .[].name github-labels.json`
do
  REPO="phetsims/$r"

  URL=https://api.github.com/repos/$REPO/labels
  curl -iH 'User-Agent: "phet"' -u "mattpen:M13t4hKurtz" -d "$1" "$URL"
done