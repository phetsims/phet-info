// Copyright 2021, University of Colorado Boulder

/**
 * This script is used to compare epic labelled issues with those on the spreadsheet.
 * Usage:
 *
 * Step 1: get the list of hyperlinked issues in the PhET Project Overview Spreadsheet (PPOS)
 * - Go to the spreadsheet (https://docs.google.com/spreadsheets/d/133PIbF9fyA5QYVwCdEkGiMmt0vrQxq1qMCk_zzwkPEI/)
 * - Menu -> Tools -> Script Editor
 * - Go to "getAllLinks.gs" and press "run", it will likely require you to give permission to the script to access the spreadsheet
 * - Copy the output of the single "Info" console output: a list of URLs linked in the sim
 *
 * Step 2: run this script:
 * - Paste the list of URLs as the value below of "linksInSpreadsheet"
 * - Make sure you have the appropriate github credentials in your buildLocal.json file.
 * - Run this file with `node` on the command line, it will print out the github issues that are labelled with epic but
 *    not in the spreadsheet.
 *
 *
 * @author Michael Kauzmann (PhET Interactive Simulations)
 */

const _ = require( '../../perennial/node_modules/lodash' );
const buildLocal = require( '../../perennial/js/common/buildLocal' );
const https = require( 'https' );

const linksInSpreadsheet = [];

function compareIssues( fromSpreadSheet, fromGithub ) {
  console.log( _.difference( fromGithub, fromSpreadSheet ) );
}

// NOTE: This only loads 100 epic issues.

const requestOptions = {
  host: 'api.github.com',
  path: '/search/issues?q=is%3Aopen+is%3Aissue+user%3Aphetsims+label%3Atype%3Aepic&per_page=100&page=1',
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
    const issueData = JSON.parse( data.toString() );
    if ( issueData.total_count > 100 ) {
      console.error( 'more issues than this is set up to track, talk to zepumph' );
    }

    const issueURLs = issueData.items.map( issue => issue.html_url );

    compareIssues( linksInSpreadsheet, issueURLs );
  } );
} );

request.on( 'error', e => {
  throw e;
} );

request.end();