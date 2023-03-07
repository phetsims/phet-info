Contributing to PhET Interactive Simulations!

Thank you so much for your desire to contribute to phetsims. Please follow these steps for contributing.

1. We use pull requests for accepting community changes into GitHub.
1. Sign the [CLA](./CLA.md) here.
2. fork the repo(s) required.
3. For common code where it applies, please do not change or commit to `dist/`, these stable built versions are updated
   less regularly.
4. use `npm config set save false` to avoid `package-log.json` files at this time.
5. Run appropriate browser unit tests and simulation tests to ensure no regressions.

Still TODO:

* We should make a pull request template.
* How do we know when people have signed the CLA?
* If things sit for a while, how to best handle merge conflicts.
* How to handle cross repo pull requests?
* Link this from all repo READMEs?