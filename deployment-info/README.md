
# Sim Deployment Info
Sim deployment instructions can be found in [sim_deployment.md](sim_deployment.md)

## Modifying and rebuilding the deployment docs
The sim deployment instructions are assembled from Markdown components in src/. If the instructions require changes, edit the relevant components in src/ (this may require editing multiple files), then rebuild. Don't edit anything in doc/--it will be over-written at build time. Be sure to commit any updated files in both src/ and doc/.

To rebuild the docs, simply type `make` in this directory. Markdown files are generated in doc/ for each case (dev, rc, public) x (phet, phet-io) brand.

## Dependencies
Building requires the `cat` and `make` utilities.

