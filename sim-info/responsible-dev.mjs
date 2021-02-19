// Copyright 2021, University of Colorado Boulder

import fs from 'fs'; // eslint-disable-line

/**
 * List repos per developer
 * cd root
 * node phet-info/sim-info/responsible-dev.mjs
 *
 * @author Sam Reid (PhET Interactive Simulations)
 */
const entries = JSON.parse( fs.readFileSync( './phet-info/sim-info/responsible_dev.json', 'utf8' ) );
const devs = [];
entries.forEach( entry => {
  entry.responsibleDevs.forEach( repoDev => {
    if ( !devs.includes( repoDev ) ) {
      devs.push( repoDev );
    }
  } );
} );
devs.sort();

const devReport = dev => {
  const repos = entries.filter( entry => entry.responsibleDevs.includes( dev ) ).map( entry => entry.repo );
  const repoNotes = repos.map( repo => `* ${repo}` ).join( '\n' );
  return '## '+dev + '\n' + repoNotes;
};
const report = devs.sort().map( devReport ).join( '\n\n' );
console.log( report );