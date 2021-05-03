// Copyright 2021, University of Colorado Boulder

import fs from 'fs'; // eslint-disable-line

/**
 * List repos per developer
 *
 * Usage:
 * cd root
 * node phet-info/sim-info/generateMarkdownOutput.mjs
 *
 * @author Michael Kauzmann (PhET Interactive Simulations)
 */
const responsibleDevObject = JSON.parse( fs.readFileSync( './phet-info/sim-info/responsible_dev.json', 'utf8' ) );
const devs = [];
const repos = Object.keys( responsibleDevObject );
let responsibleTableString = `
## HTML5 Sim and Common Code Repos - Developer/Designer Responsibility List

NOTE: This file is generated, do not edit directly. It is created from \`responsible_dev.json\`, see \`./generateMarkdownOutput.mjs\`.


| Simulation  | Developer | Designer |
| :---------- | :------------- | :------------- |
`;

repos.forEach( repoName => {
  const responsibleDeveloper = responsibleDevObject[ repoName ].responsibleDevs.join( ',' )
  const responsibleDesigner = responsibleDevObject[ repoName ].responsibleDesigners.join( ',' )
  responsibleTableString += `| ${repoName} | ${responsibleDeveloper} | ${responsibleDesigner} | \n`;
} );

fs.writeFileSync( './phet-info/sim-info/responsible_dev.md', responsibleTableString );
