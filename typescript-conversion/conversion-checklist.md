For https://github.com/phetsims/chipper/issues/1616, we would like to convert the sim to TypeScript.

- [ ] Identify what brands and feature sets are supported. Is it a phet-io sim? Does it have a stable API?
- [ ] Publish dev version before. Use `grunt dev --brands={{brands}} --message="before TypeScript conversion, see {{issue number URL}}"` option in grunt build to connect to the conversion issue.
- [ ] Create a branch
- [ ] Create a harness that will test for snapshot-comparison regressions. Record the URL and SHAs. Set up to run in `npm test`:
  - [ ] Copy the test/ folder as well as playwright.config.js to the repo. Make sure to use the correct sim name in the test script.
  - [ ] Add this to the package.json
```
  "devDependencies": {
    "grunt": <whatever version it has>,
    "@playwright/test": "^1.40.0"
  },
  "scripts": {
    "test": "playwright test && grunt type-check && grunt lint"
  },
```
- Continuation of test harness:
  - [ ] Do the necessary npm installations for playwright.
  - [ ] Run `npm test`, it will fail, but then get the correct testing hash and put it at the end of the testing script where it says `const validHashes = [ '12adf4' ];`
  - [ ] Run `npm test` a couple of times, to make sure the new hash is correct and consistent (no random layout changes from the sim)
- [ ] Use [typescript-quick-start.md](https://github.com/phetsims/phet-info/blob/cdee426ece5ea24fff45d92194ce9638b8cf1bb0/doc/typescript-quick-start.md) to familiarize yourself with the typescript conversion process.
- [ ] Rename all files as a batch and commit *just the renames*, see https://github.com/phetsims/balancing-act/issues/168#issuecomment-3146720372 (You can use `rename-js-to-ts.sh`)
- [ ] Add `// @ts-nocheck` to the top of all files, and commit (You can use `add-eslint-disable.sh`)
- [ ] **Convert to TypeScript** This is where all the work is done
- [ ] Test in wrappers as appropriate: the PhET-iO State wrapper as you go if the sim supports PhET-iO. The a11y view, etc.
- [ ] merge to main
- [ ] delete branch
- [ ] test on CT
- [ ] Publish dev version after. Use `grunt dev --brands={{brands}} --message="after TypeScript conversion, see {{issue number URL}}"`
- [ ] Compare between both versions to identify any regression due to the typescript conversion.
- [ ] If needed, schedule a QA test for regressions
- [ ] consult with the lead developer about any remaining work

@jbphet approved me to start here. He said: You're of course welcome to work on those, but please regression test thoroughly as you do.  They were both tricky sims.  SOM has lots of optimizations for fast model calculations, and EFAC has its own 2D interaction model for stacking and such, and these things are a little complicated.  Also, the behavior of the energy chunks is a bit touchy.
