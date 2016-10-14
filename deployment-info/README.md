
# Sim Deployment Info

## Structure
Currently all sim deployment info is broken up into chunks located in `src/`.
Using the Makefile these chunks are built into usable Markdown files and put in `doc/`
`sim_deployment.md` points to each option in the doc folder. 

## To Edit
- Only edit files in the `src/` folder, because all files in `doc/` will be overwritten the next 
time that the Makefile builds.
- Make sure that when you edit a chunk in the `src/` that you are editing all possible places. If your
change applies both to rc-phet and rc-phet-io, then you must make the change in both places.
- Once done editing, run the Makefile again to recompile the complete docs. Then push those changes to github.




