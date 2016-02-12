#!/bin/bash

# .credentials is a file with your github creds in the format username:password
# This should probably be replaced with oAuth
CREDS=`cat .credentials`

#REPO should be in the format "organization/repo"
#REPO="phetsims/friction"
REPOS=(phetcommon energy-skate-park-basics scenery build-an-atom ohms-law example-sim beers-law-lab faraday resistance-in-a-wire forces-and-motion-basics dot molecule-shapes assert build-a-molecule nitroglycerin kite scenery-phet phet-core balloons-and-static-electricity sun joist john-travoltage chipper tween.js molarity axon gravity-force-lab phetmarks wave-on-a-string phet-info gravity-and-orbits graphing-lines blast fraction-matcher build-a-fraction-deprecated fractions-intro-deprecated vibe sherpa concentration mobius friction balancing-act vegas ph-scale slater ph-scale-basics under-pressure fraction-comparison acid-base-solutions fraction-common-deprecated phet-io molecule-polarity estimation all-sims arithmetic griddle balancing-chemical-equations seasons area-builder color-vision circuit-construction-kit-basics fluid-pressure-and-flow optics-lab tasks graphing-quadratics plinko-probability states-of-matter-basics reactants-products-and-leftovers brand chronicle preface datamite molecules-and-light faradays-law protein-synthesis simula-rasa energy-forms-and-changes neuron litmus website pendulum-lab molecule-shapes-basics atomic-interactions isotopes-and-atomic-mass charges-and-fields least-squares-regression capacitor-lab-basics sugar-and-salt-solutions states-of-matter shred installer-builder blackbody-spectrum bending-light curve-fitting babel function-builder projectile-motion chains rosetta simulation-picker rutherford-scattering special-ops tandem phet-metacog hookes-law beaker gene-expression-basics making-tens calculus-grapher trig-tour yotta phet-cafepress perennial phet-app expression-exchange models-of-the-hydrogen-atom masses-and-springs)

for r in "${REPOS[@]}"
do
  REPO="phetsims/$r"

  URL=https://api.github.com/repos/$REPO/labels
  HEADERS='{
    "name": "status:on-hold",
    "color": "F0FFF0"
  }'
  curl -iH 'User-Agent: "phet"' -u "mattpen:M13t4hKurtz" -d "$HEADERS" "$URL"
done