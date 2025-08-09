For https://github.com/phetsims/chipper/issues/1616, we would like to convert the sim to TypeScript.

- [ ] Publish dev version before. Use `--message="before TypeScript conversion, see {{issue number URL}}"` option in grunt build to connect to the conversion issue.
- [ ] Create a branch
- [ ] Create a harness that will test for snapshot-comparison regressions. Record the URL and SHAs. Set up to run in `npm test`
- [ ] Use typescript-quick-start.md to familiarize yourself with the typescript conversion process.
- [ ] Rename all files as a batch and commit *just the renames*, see https://github.com/phetsims/balancing-act/issues/168#issuecomment-3146720372
- [ ] Add `// @ts-nocheck` to the top of all files, and commit
- [ ] **Convert to TypeScript** This is where all the work is done
- [ ] Test in wrappers as appropriate: the PhET-iO State wrapper as you go if the sim supports PhET-iO. The a11y view, etc.
- [ ] merge to main
- [ ] delete branch
- [ ] test on CT
- [ ] Publish dev version after. Use `--message="after TypeScript conversion, see {{issue number URL}}"`
- [ ] Compare between both versions to identify any regression due to the typescript conversion.
- [ ] If needed, schedule a QA test for regressions
- [ ] consult with the lead developer about any remaining work

@jbphet approved me to start here. He said: You're of course welcome to work on those, but please regression test thoroughly as you do.  They were both tricky sims.  SOM has lots of optimizations for fast model calculations, and EFAC has its own 2D interaction model for stacking and such, and these things are a little complicated.  Also, the behavior of the energy chunks is a bit touchy.