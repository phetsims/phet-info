#!/bin/bash

# .credentials is a file with your github creds in the format username:password
# This should probably be replaced with oAuth
CREDS=`cat .credentials`
if [[ $CREDS -eq '' ]]
then
  echo "Requires .credential file"
  exit 1
fi

#REPO should be in the format "organization/repo"
#REPO="phetsims/friction"
if [[ $1 -eq '' ]] 
then
  echo "Usage: $0 \"organization/repo\""
else

  REPO=$1
  URL=https://api.github.com/repos/$REPO/labels


  #delete the "invalid" label
  curl -iH 'User-Agent: "PhET"' -u "$CREDS" -X "DELETE" "$URL/invalid"

  # Replace stand-issue labels if they exist
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



  #add new labels
  LABELS=()
  LABELS+=('{
      "name": "type:bug",
      "color": "FF00AA"
    }')
  LABELS+=('{
      "name": "type:duplicate",
      "color": "EEEED1"
    }')
  LABELS+=('{
      "name": "dev:enhancement",
      "color": "0276FD"
    }')
  LABELS+=('{
      "name": "dev:help-wanted",
      "color": "63D1F4"
    }')
  LABELS+=('{
      "name": "type:question",
      "color": "EDCB62"
    }')
  LABELS+=('{
      "name": "type:wontfix",
      "color": "ffffff"
    }')
  LABELS+=('{
      "name": "type:multitouch",
      "color": "72587F"
    }')
  LABELS+=('{
      "name": "priority:2-high",
      "color": "e11d21"
    }')
  LABELS+=('{
      "name": "status:fixed-pending-testing",
      "color": "00FFCC"
    }')
  LABELS+=('{
      "name": "priority:1-top",
      "color": "FF007F"
    }')
  LABELS+=('{
      "name": "priority:3-medium",
      "color": "FFE600"
    }')
  LABELS+=('{
      "name": "priority:4-low",
      "color": "c7def8"
    }')
  LABELS+=('{
      "name": "project:master-checklist",
      "color": "42426F"
    }')
  LABELS+=('{
      "name": "project:requires-kathy",
      "color": "0000FF"
    }')
  LABELS+=('{
      "name": "design:artwork",
      "color": "d4c5f9"
    }')
  LABELS+=('{
      "name": "type:i18n",
      "color": "B452CD"
    }')
  LABELS+=('{
      "name": "type:misc",
      "color": "B87333"
    }')
  LABELS+=('{
      "name": "type:licensing",
      "color": "4B0082"
    }')
  LABELS+=('{
      "name": "priority:5-deferred",
      "color": "FFFAFA"
    }')
  LABELS+=('{
      "name": "dev:a11y",
      "color": "008080"
    }')
  LABELS+=('{
      "name": "type:performance",
      "color": "8B1C62"
    }')
  LABELS+=('{
      "name": "dev:code-review",
      "color": "104E8B"
    }')
  LABELS+=('{
      "name": "design:teaching-resources",
      "color": "F7B3DA"
    }')
  LABELS+=('{
      "name": "meeting:developer",
      "color": "000000"
    }')
  LABELS+=('{
      "name": "dev:PhET-io",
      "color": "1FFFFF"
    }')
  LABELS+=('{
      "name": "meeting:PhET-io",
      "color": "000000"
    }')
  LABELS+=('{
      "name": "design:general",
      "color": "F6CCDA"
    }')
  LABELS+=('{
      "name": "meeting:status",
      "color": "000000"
    }')
  LABELS+=('{
      "name": "meeting:design",
      "color": "000000"
    }')
  LABELS+=('{
      "name": "status:in-progress",
      "color": "CCFFCC"
    }')
  LABELS+='{
    "name": "status:ready-to-test",
    "color": "006400"
  }'
  LABELS+='{
    "name": "status:ready-for-review",
    "color": "3E766D"
  }'

  for i in "${LABELS[@]}"
  do
    curl -iH 'User-Agent: "PhET"' -u "$CREDS" -d "$i" "$URL"
  done
fi



