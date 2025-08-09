/* eslint-disable */
// @ts-nocheck

const { defineConfig } = require( '@playwright/test' );

module.exports = defineConfig( {
  testDir: './test',
  testMatch: '**/*test.js',
  timeout: 30000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: 'list',
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true
  }
} );