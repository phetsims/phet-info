// Copyright 2023, University of Colorado Boulder

const buildLocal = require( '../../perennial-alias/js/common/buildLocal' );
const { Octokit } = require( 'octokit' ); // eslint-disable-line require-statement-match
const octokit = new Octokit( {
  auth: buildLocal.phetDevGitHubAccessToken
} );

// List all users for the organization
const getUsersFromGitHub = async () => { // eslint-disable-line no-unused-vars
  const result = await octokit.request( 'GET /orgs/phetsims/members', {
    org: 'phetsims',
    per_page: 100
  } );

  // console.log( result.data.length );
  const logins = result.data.map( member => member.login );
  return logins;
};

// Users that have >=1 ready for review issue as of Feb 16, 2023
// const getUsersStatic = async () => {
//   return [
//     'AgustinVallejo',
//     'amanda-phet',
//     'arouinfar',
//     'chrisklus',
//     'emily-phet',
//     'JacquiHayes',
//     'jbphet',
//     'jessegreenberg',
//     'jonathanolson',
//     'kathy-phet',
//     'Luisav1',
//     'matthew-blackman',
//     'Matthew-Moore240',
//     'mattpen',
//     'oliver-phet',
//     'pixelzoom',
//     'samreid',
//     'veillette',
//     'zepumph'
//   ];
// };

const getDevUsersStatic = async () => {
  return [
    'AgustinVallejo',
    'chrisklus',
    'jbphet',
    'jessegreenberg',
    'jonathanolson',
    'liammulh',
    'Luisav1',
    'marlitas',
    'matthew-blackman',
    'mattpen',
    'pixelzoom',
    'samreid',
    'veillette',
    'zepumph'
  ];
};

const getUsers = getDevUsersStatic();

// https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#list-users
( async () => {
  const users = await getUsers;
  const results = [];
  for ( let i = 0; i < users.length; i++ ) {
    const user = users[ i ];

    const openIssuesResult = await octokit.request( 'GET /search/issues', {
      accept: 'application/vnd.github+json',
      // q: `is:issue is:open label:status:ready-for-review assignee:${user} org:phetsims`,
      q: `is:issue is:open assignee:${user} org:phetsims`,
      per_page: 100,
      page: 1
    } );

    const readyForReviewResult = await octokit.request( 'GET /search/issues', {
      accept: 'application/vnd.github+json',
      q: `is:issue is:open label:status:ready-for-review assignee:${user} org:phetsims`,
      // q: `is:issue is:open assignee:${user} org:phetsims`,
      per_page: 100,
      page: 1
    } );

    // console.log( result.data.items.length );
    // console.log( result.data.items );
    // console.log( `${user}: ${result.data.items.length}` );
    results.push( { user: user, 'open issues': openIssuesResult.data.items.length, 'ready-for-review': readyForReviewResult.data.items.length } );
  }

  console.table( results, [ 'user', 'open issues', 'ready-for-review' ] );
} )();
