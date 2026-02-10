// Copyright 2021, University of Colorado Boulder

import fs from 'fs';
import yaml from 'js-yaml';

/**
 * List repos per developer
 *
 * Usage:
 * cd root
 * sage run phet-info/sim-info/generateMarkdownOutput.mjs
 *
 * @author Michael Kauzmann (PhET Interactive Simulations)
 */
const responsibleDevObject = yaml.load( fs.readFileSync( './phet-info/sim-info/responsible_team.yaml', 'utf8' ) );

const repos = Object.keys( responsibleDevObject );
let responsibleTableString = `
## HTML5 Sim and Common Code Repos - Developer/Designer Responsibility List

NOTE: This file is generated, do not edit directly. It is created from \`responsible_team.yaml\`, see \`./generateMarkdownOutput.mjs\`.


| Simulation  | Developer | Designer | Features |
| :---------- | :------------- | :------------- | :------------- |
`;

// TODO: This will probably be out of date soon once the metadata work is completed. https://github.com/phetsims/phet-info/issues/252
// look at the repo's package.json in phet.simFeatures and note selected features for the sim.
const getFeatures = repo => {
  const features = [];
  try {
    const packageJSON = JSON.parse( fs.readFileSync( `./${repo}/package.json` ).toString() );
    if ( packageJSON.phet && packageJSON.phet.simFeatures ) {
      if ( packageJSON.phet.simFeatures.supportsSound ) {
        features.push( 'Sound' );
      }
      if ( packageJSON.phet.simFeatures.supportsInteractiveDescription ) {
        features.push( 'Interactive Description' );
      }
      if ( packageJSON.phet.simFeatures.supportsVoicing ) {
        features.push( 'Voicing' );
      }
      if ( packageJSON.phet.simFeatures.supportsInteractiveHighlights ) {
        features.push( 'Interactive Highlights' );
      }
    }
  }
  catch( e ) {

    // some repos don't have package.json, and that's okay.
  }
  return features;
};

repos.forEach( repoName => {
  const responsibleDeveloper = responsibleDevObject[ repoName ].responsibleDevs.join( ',' );
  const responsibleDesigner = responsibleDevObject[ repoName ].responsibleDesigners.join( ',' );
  const features = getFeatures( repoName ).join( '<br/>' );
  responsibleTableString += `| ${repoName} | ${responsibleDeveloper} | ${responsibleDesigner} | ${features} | \n`;
} );

fs.writeFileSync( './phet-info/sim-info/responsible_team.md', responsibleTableString );