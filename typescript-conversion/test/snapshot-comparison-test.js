/* eslint-disable */
// @ts-nocheck
const { test, expect } = require( '@playwright/test' );

test( 'snapshot comparison hash check', async ( { page } ) => {
  // Set up console listener before navigating
  const consolePromise = new Promise( ( resolve ) => {
    page.on( 'console', msg => {
      const text = msg.text();
      // Look for the specific console log pattern
      if ( text.includes( 'Creating td for sim "states-of-matter"' ) && text.includes( 'hash=' ) ) {
        // Extract the short hash from the console log
        const hashMatch = text.match( /hash=([a-f0-9]+),/ );
        if ( hashMatch ) {
          resolve( hashMatch[ 1 ] );
        }
      }
    } );
  } );

  // Navigate to the snapshot comparison page
  await page.goto( 'http://localhost/aqua/html/snapshot-comparison.html?repos=states-of-matter&logHash' );

  // Wait up to 5 seconds for the console log
  const hash = await Promise.race( [
    consolePromise,
    new Promise( ( _, reject ) => setTimeout( () => reject( new Error( 'Timeout waiting for hash' ) ), 5000 ) )
  ] );

  // Check if the hash matches the expected values
  const validHashes = [ '210c3b' ];
  expect( validHashes ).toContain( hash );
} );