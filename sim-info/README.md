Sim Info
=========

## Responsible Lists

[responsible_dev.json](./responsible_dev.json) is the central location for all responsible actors for a repo. Every repo
should have a responsibleDev, someone in charge of maintaining the code/files inside that repo. This file should be
maintained manually.

[responsible_dev.md](./responsible_dev.md) is a generated markdown file of the json data. see [./generateMarkdownOutput.mjs](./generateMarkdownOutput.mjs)

------------------

To print out a list, by developer, of all repos a dev is responsible for:

```bash
cd phet-info/../
node phet-info/sim-info/printReposPerDev.mjs
```

----------------------


To test to make sure the list is in sync with github:

1. Make sure that you have appropriate credentials in your build local
2. Have perennial and phet-info checked out
3. Run:

```bash
cd phet-info/../
node phet-info/sim-info/areAllReposInFile.js
```

With output that looks like:

```
must add faraday to responsible dev list
must add seasons to responsible dev list
must add skiffle to responsible dev list
must add geometric-optics to responsible dev list
must remove installer-builder from responsible dev list as it is not on github
must remove phet-overview from responsible dev list as it is not on github
```