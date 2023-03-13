// Copyright 2021, University of Colorado Boulder

// update-repos-list.js
//
//  This script creates a file in this directly called `.repos` that is
//  a newline separated list of all repos in the phetsims organization.

const axios = require( '../../perennial/node_modules/axios' );
const buildLocal = require( '../../perennial/js/common/buildLocal' );
const fs = require( 'fs' );

( async () => {
  // temporarily store the old repos for troubleshooting if problems arise
  try {
    await fs.promises.rename( '.repos', '.repos.old' );
  }
  catch( err ) {
    if ( err.code !== 'ENOENT' ) {
      console.error( err );
      throw err;
    }
  }

  // Iterate over all repos in the organization
  let currentRepos;
  let repoNames = '';
  let currentPage = 1;
  const pageSize = 100;
  do {
    currentRepos = ( await axios.get( `https://api.github.com/orgs/phetsims/repos?per_page=${pageSize}&page=${currentPage}&sort=full_name`, {
      auth: {
        username: buildLocal.developerGithubUsername,
        password: buildLocal.developerGithubAccessToken
      }
    } ) ).data;
    if ( currentRepos ) {
      const names = currentRepos.map( repo => repo.name.trim() ).filter( name =>
        name !== 'community'
      );
      repoNames += names.join( '\n' ) + '\n';
    }
    currentPage++;
  } while ( currentRepos && currentRepos.length === pageSize );

  // Save to disk
  await fs.promises.writeFile( '.repos', repoNames );

  // Clean up
  await fs.promises.unlink( '.repos.old' );
} )();

