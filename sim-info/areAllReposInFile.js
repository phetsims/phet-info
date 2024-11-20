// Copyright 2021, University of Colorado Boulder

/**
 * Determine whether all PhET GitHub repos are represented in responsible_dev.json
 *
 * Usage:
 * cd root
 * node ./phet-info/sim-info/areAllReposInFile.js
 *
 * @author Michael Kauzmann (PhET Interactive Simulations)
 */
const getAllRepos = require( './getAllRepos' );
const fs = require( 'fs' );

( async () => {

  // {Object.<string,{responsibleDev:string[]}>} - keys are repos
  const reposFromJSON = JSON.parse( fs.readFileSync( './phet-info/sim-info/responsible_dev.json', 'utf8' ) );

  // {string[]} - repo names
  const reposInJSON = Object.keys( reposFromJSON );

  // {string[]} - all repos on github
  const reposFromGithub = await getAllRepos();

  let someDiscrepancy = false;

  for ( let i = 0; i < reposFromGithub.length; i++ ) {
    const repoInGithub = reposFromGithub[ i ];
    if ( !reposFromJSON.hasOwnProperty( repoInGithub ) ) {
      console.log( `must add ${repoInGithub} to responsible dev list` );
      someDiscrepancy = true;
    }
  }

  for ( let i = 0; i < reposInJSON.length; i++ ) {
    const repoInJSON = reposInJSON[ i ];
    if ( !reposFromGithub.includes( repoInJSON ) ) {
      console.log( `must remove ${repoInJSON} from responsible dev list as it is not on github` );
      someDiscrepancy = true;
    }
  }

  if ( !someDiscrepancy ) {
    console.log( 'No discrepancies found between responsible_dev.json and github.' );
  }
} )();