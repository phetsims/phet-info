// Copyright 2021, University of Colorado Boulder

import fs from 'fs';

/**
 * List repos per developer
 *
 * Usage:
 * cd root
 * node phet-info/sim-info/printReposPerDev.mjs
 *
 * @author Sam Reid (PhET Interactive Simulations)
 */
const responsibleDevObject = JSON.parse( fs.readFileSync( './phet-info/sim-info/responsible_dev.json', 'utf8' ) );
const devs = [];
const repos = Object.keys( responsibleDevObject );
repos.forEach( repoName => {
  responsibleDevObject[ repoName ].responsibleDevs.forEach( repoDev => {
    if ( !devs.includes( repoDev ) ) {
      devs.push( repoDev );
    }
  } );
} );
devs.sort();

const devReport = dev => {
  const reposForDev = repos.filter( repo => responsibleDevObject[ repo ].responsibleDevs.includes( dev ) );
  const repoNotes = reposForDev.map( repo => `* ${repo}` ).join( '\n' );
  return '## ' + dev + '\n' + repoNotes;
};
const report = devs.sort().map( devReport ).join( '\n\n' );
console.log( report );