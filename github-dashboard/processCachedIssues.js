// Copyright 2023, University of Colorado Boulder

/**
 * Read the open issues cached to disk, and output the number of issues assigned to each user.
 *
 * @author Sam Reid (PhET Interactive Simulations)
 * @author Agustín Vallejo (PhET Interactive Simulations)
 */

const fs = require( 'fs' );

const repos = fs.readFileSync( './repos', 'utf8' ).split( '\n' );
const users = fs.readFileSync( './users', 'utf8' ).split( '\n' );

// Fetch the open issues assigned to users in the organization, organized by repository
( () => {

  users.forEach( user => {

    let sum = 0;
    // console.log( user);
    const map = {};
    repos.forEach( repo => {

      const issues = JSON.parse( fs.readFileSync( `./repodir/${repo}`, 'utf8' ) );
      const userIssues = issues.filter( issue => {
        return issue.assignees.filter( assignee => {
          return assignee.login === user;
        } ).length > 0;
      } );

      if ( userIssues.length > 0 ) {
        map[ repo ] = userIssues.length;
      }

      sum += userIssues.length;

    } );
    console.log( user, sum, JSON.stringify( map, null, 2 ) );
  } );
} )();