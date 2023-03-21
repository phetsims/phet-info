// Copyright 2023, University of Colorado Boulder

/**
 * This script interacts with the GitHub API to fetch organization members, repositories, and open issues
 * for the 'phetsims' organization. For users and repos, they are output to console where they can be saved to file manually.
 * Issues are outputted to ./repodir.
 * Key functionalities:
 * * Get the list of organization members (getUsersFromGitHub)
 * * Get the list of repositories (getReposFromGitHub)
 * * Fetch open issues assigned to organization members, organized by repository (getAssignedIssuesByRepo)
 * Usage: Run the script with Node.js. Optionally, set downloadNewData to true to download updated user and repo data.
 *
 * @author Sam Reid (PhET Interactive Simulations)
 * @author Agustín Vallejo (PhET Interactive Simulations)
 */

const buildLocal = require( '../../perennial-alias/js/common/buildLocal' );
const { Octokit } = require( 'octokit' ); // eslint-disable-line require-statement-match
const octokit = new Octokit( {
  auth: buildLocal.phetDevGitHubAccessToken
} );
const fs = require( 'fs' );

// List all users for the organization
const getUsersFromGitHub = async () => {
  const result = await octokit.request( 'GET /orgs/phetsims/members', {
    org: 'phetsims',
    per_page: 100
  } );

  // console.log( result.data.length );
  const logins = result.data.map( member => member.login );
  return logins;
};

// Fetch the list of repositories in the organization
const getReposFromGitHub = async () => {
  const fetchRepos = async page => {
    const result = await octokit.request( 'GET /orgs/phetsims/repos', {
      org: 'phetsims',
      per_page: 100,
      page: page
    } );

    return result;
  };

  let allRepos = [];
  let currentPage = 1;
  let fetchedRepos;

  do {
    fetchedRepos = await fetchRepos( currentPage );
    allRepos = allRepos.concat( fetchedRepos.data );
    currentPage += 1;
  } while ( fetchedRepos.data.length === 100 );

  const repoNames = allRepos.map( repo => repo.name );
  return repoNames;
};

const repos = fs.readFileSync( './repos', 'utf8' ).split( '\n' );
// const users = fs.readFileSync( './users', 'utf8' ).split( '\n' );

// Fetch the open issues assigned to users in the organization, organized by repository
const getAssignedIssuesByRepo = async () => {

  const fetchIssues = async ( repo, page ) => {
    const issues = await octokit.request( 'GET /search/issues', {
      q: `repo:phetsims/${repo} is:issue is:open`,
      per_page: 100,
      page: page
    } );

    return issues;
  };

  for ( const repo of repos ) {
    let repoIssues = [];
    let currentPage = 1;
    let fetchedIssues;

    do {
      fetchedIssues = await fetchIssues( repo, currentPage );
      repoIssues = repoIssues.concat( fetchedIssues.data.items );
      currentPage += 1;
    } while ( fetchedIssues.data.items.length === 100 );
    try {
      fs.mkdirSync( './repodir' );
    }
    catch( e ) {
      console.log( e );
    }
    fs.writeFileSync( `./repodir/${repo}`, JSON.stringify( repoIssues, null, 2 ) );

    // exit();

    // Exit from the node process
    // process.exit( 0 );
  }
};

( async () => {
  const downloadNewData = false;
  if ( downloadNewData ) {
    const users = await getUsersFromGitHub();
    console.log( users );

    const repos = await getReposFromGitHub();
    console.log( repos.length, repos.join( '\n' ) );
  }

  await getAssignedIssuesByRepo();
} )();
