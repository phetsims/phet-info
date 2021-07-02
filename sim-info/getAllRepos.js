// Copyright 2021, University of Colorado Boulder

/**
 * Get all repos in phetsims that are not archived, disabled, or forks. This probably won't work unless you have
 * admin privileges to read all repos.
 *
 * This is not intended to be run directly. It's used by areAllReposInFile.js.
 *
 * @author Michael Kauzmann (PhET Interactive Simulations)
 */

const buildLocal = require( '../../perennial/js/common/buildLocal' );
const https = require( 'https' );

const getSomeRepos = async pageNumber => {
  return new Promise( resolve => {

    const requestOptions = {
      host: 'api.github.com',
      path: `/orgs/phetsims/repos?per_page=100&page=${pageNumber}`,
      method: 'GET',
      auth: `${buildLocal.developerGithubUsername}:${buildLocal.developerGithubAccessToken}`,
      headers: {
        'User-Agent': 'PhET'
      }
    };

    const request = https.request( requestOptions, res => {

      let data = '';
      res.on( 'data', d => {
        data += d.toString();
      } );

      res.on( 'end', () => {
        const repoData = JSON.parse( data.toString() );
        resolve( repoData.filter( x => {
          return !x.archived && !x.disabled && !x.fork; // no repos that are archived, disabled, or actually just forks
        } ).map( x => x.name ) );
      } );
    } );

    request.on( 'error', e => { throw e; } );
    request.end();
  } );
};

/**
 * @returns {Promise.<string[]>}
 */
module.exports = async () => {
  let repos = [];

  for ( let i = 1; i < 5; i++ ) {
    repos = repos.concat( await getSomeRepos( i ) );
  }
  return repos.sort();
};
