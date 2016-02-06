#!/bin/bash

# .credentials is a file with your github creds in the format username:password
# This should probably be replaced with oAuth
CREDS=`cat .credentials`

#REPO should be in the format "organization/repo"
#REPO="phetsims/friction"
REPOS=(phetcommon energy-skate-park-basics scenery build-an-atom ohms-law example-sim beers-law-lab faraday resistance-in-a-wire forces-and-motion-basics dot molecule-shapes assert build-a-molecule nitroglycerin kite scenery-phet phet-core balloons-and-static-electricity sun joist john-travoltage chipper tween.js molarity axon gravity-force-lab phetmarks wave-on-a-string phet-info gravity-and-orbits graphing-lines blast fraction-matcher build-a-fraction-deprecated fractions-intro-deprecated vibe sherpa concentration mobius friction balancing-act vegas ph-scale slater ph-scale-basics under-pressure fraction-comparison acid-base-solutions fraction-common-deprecated phet-io molecule-polarity estimation all-sims arithmetic griddle balancing-chemical-equations seasons area-builder color-vision circuit-construction-kit-basics fluid-pressure-and-flow optics-lab tasks graphing-quadratics plinko-probability states-of-matter-basics reactants-products-and-leftovers brand chronicle preface datamite molecules-and-light faradays-law protein-synthesis simula-rasa energy-forms-and-changes neuron litmus website pendulum-lab molecule-shapes-basics atomic-interactions isotopes-and-atomic-mass charges-and-fields least-squares-regression capacitor-lab-basics sugar-and-salt-solutions states-of-matter shred installer-builder blackbody-spectrum bending-light curve-fitting babel function-builder projectile-motion chains rosetta simulation-picker rutherford-scattering special-ops tandem phet-metacog hookes-law beaker gene-expression-basics making-tens calculus-grapher trig-tour yotta phet-edmodo phet-cafepress perennial phet-app expression-exchange models-of-the-hydrogen-atom masses-and-springs phet-io-site)

for r in "${REPOS[@]}"
do
  REPO="phetsims/$r"
  URL=https://api.github.com/repos/$REPO/labels


  #delete the "invalid" label
  curl -iH 'User-Agent: "phet"' -u "$CREDS" -X "DELETE" "$URL/invalid"

  # Replace stand-issue labels if they exist
  REPLACE='{
      "name": "type:wontfix",
      "color": "ffffff",
      "User-Agent": "PhET"
    }'
  curl -iH 'User-Agent: "phet"' -u "$CREDS" -d "$REPLACE" "$URL/wontfix"

  REPLACE='{
      "name": "type:question",
      "color": "EDCB62",
      "User-Agent": "PhET"
    }'
  curl -iH 'User-Agent: "phet"' -u "$CREDS" -d "$REPLACE" "$URL/question"

  REPLACE='{
      "name": "dev:help-wanted",
      "color": "63D1F4",
      "User-Agent": "PhET"
    }'
  curl -iH 'User-Agent: "phet"' -u "$CREDS" -d "$REPLACE" "$URL/help%20wanted"

  REPLACE='{
      "name": "dev:enhancement",
      "color": "0276FD",
      "User-Agent": "PhET"
    }'
  curl -iH 'User-Agent: "phet"' -u "$CREDS" -d "$REPLACE" "$URL/enhancement"

  REPLACE='{
      "name": "type:duplicate",
      "color": "EEEED1",
      "User-Agent": "PhET"
    }'
  curl -iH 'User-Agent: "phet"' -u "$CREDS" -d "$REPLACE" "$URL/duplicate"

  REPLACE='{
      "name": "type:bug",
      "color": "FF00AA",
      "User-Agent": "PhET"
    }'
  curl -iH 'User-Agent: "phet"' -u "$CREDS" -d "$REPLACE" "$URL/bug"



  #add new labels
  LABELS=()
  LABELS+=('{
      "name": "type:bug",
      "color": "FF00AA",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "type:duplicate",
      "color": "EEEED1",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "dev:enhancement",
      "color": "0276FD",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "dev:help-wanted",
      "color": "63D1F4",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "type:question",
      "color": "EDCB62",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "type:wontfix",
      "color": "ffffff",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "type:multitouch",
      "color": "72587F",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "priority:2-high",
      "color": "e11d21",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "status:fixed-pending-testing",
      "color": "00FFCC",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "priority:1-top",
      "color": "FF007F",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "priority:3-medium",
      "color": "FFE600",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "priority:4-low",
      "color": "c7def8",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "project:master-checklist",
      "color": "42426F",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "project:requires-kathy",
      "color": "0000FF",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "design:artwork",
      "color": "d4c5f9",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "type:i18n",
      "color": "B452CD",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "type:misc",
      "color": "B87333",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "type: licensing",
      "color": "4B0082",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "priority:5-deferred",
      "color": "FFFAFA",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "dev:a11y",
      "color": "008080",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "type:performance",
      "color": "8B1C62",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "dev:code-review",
      "color": "104E8B",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "design:teaching-resources",
      "color": "F7B3DA",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "meeting:developer",
      "color": "000000",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "dev:phet-io",
      "color": "1FFFFF",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "meeting:phet-io",
      "color": "000000",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "design:general",
      "color": "F6CCDA",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "meeting:status",
      "color": "000000",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "meeting:design",
      "color": "000000",
      "User-Agent": "PhET"
    }')
  LABELS+=('{
      "name": "status:in-progress",
      "color": "CCFFCC",
      "User-Agent": "PhET"
    }')


  for i in "${LABELS[@]}"
  do
    curl -iH 'User-Agent: "phet"' -u "$CREDS" -d "$i" "$URL"
  done
done





