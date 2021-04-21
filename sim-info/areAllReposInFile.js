// Copyright 2021, University of Colorado Boulder

/**
 * usage:
 * cd root;
 * node ./phet-info/sim-info/areAllReposInFile.js
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

  for ( let i = 0; i < reposFromGithub.length; i++ ) {
    const repoInGithub = reposFromGithub[ i ];
    if ( !reposFromJSON.hasOwnProperty( repoInGithub ) ) {
      console.log( `must add ${repoInGithub} to responsible dev list` );
    }
  }

  for ( let i = 0; i < reposInJSON.length; i++ ) {
    const repoInJSON = reposInJSON[ i ];
    if ( !reposFromGithub.includes( repoInJSON ) ) {
      console.log( `must remove ${repoInJSON} from responsible dev list as it is not on github` );
    }
  }
} )();