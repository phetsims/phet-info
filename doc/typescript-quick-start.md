### TypeScript Quick Start

These are the basic steps and summary for converting a repo to TypeScript, how to use it, and summary of some workflows,
known problems, etc.
Please be aware of open issues in https://github.com/phetsims/chipper/issues?q=is%3Aissue+is%3Aopen+label%3Achipper%3Atypescript

### Getting started
1. Clone missing repos.  This makes sure you have everything.
2. Pull everything.  This makes sure you have the latest version of everything.
3. `npm install` in chipper. This makes sure you have the TypeScript compiler, which is called `tsc`

### Converting a Repo to TypeScript
1. Go to package.json and add `"typescript": true` in the phet section.  That enables the TypeScript step in the build tools.
2. `grunt update`.  This updates the html to point to the built code, which will be compiled to chipper/dist

Congratulations!  Now the repo is typescript-capable.

### Experiment with your new TypeScript repo
1. Compile the source and its dependencies via `grunt output-js-project`.  This compiles the sim and its dependencies to chipper/dist.
It uses "Project References" (tsc --build) to trace the dependencies.
The compiler is also configured for incremental compilation.  This means subsequent compiles will be much faster than the first compile.
2. Open the sim in the browser via phetmarks
3. Convert one of the files to *.ts and add code like `const x:number=7; console.log(x);` .
4. Compile via `grunt output-js-project` and run it in the browser.  Did it print `7`?
5. Try creating a type error like `const x:string=7` and see what happens.

### Toward more efficient iteration
1. Install tsc globally (with the same version as chipper/package.json), or set an alias like `alias tsc = node /path/chipper/node_modules/typescript/bin/tsc`.  The latter will make sure you always have right version of typescript.
2. In your sim repo, run `tsc --build --watch`.  This will watch for any changes in the project or its dependecies and auto-recompile
3. I have not yet experimented with having the IDE do the builds, but maybe that will be more efficient.

### Caveats
1. For now, please leave the phet-io-overrides.js file, strings file and namespace file as *.js.  The build tools are not set to do those in TypeScript yet.
2. This is an evolving project in the early phases.  There will be growing pains. Discover problems, look for solutions!
3. Please do not convert common code to TypeScript until we have safe RC SHAs for Fourier and Density.  If you want to leverage generics in Property, you can use
the axon typescript branch, but do not commit any code to master that depends on it.  You could work in a typescript branch for now.
4. We may one day abandon TypeScript, but before we consider that, let's make sure to give it a fair trial and see how
much value it can provide.
5. phettest and CT provide TypeScript support, but do not yet have a good user experience for showing TypeErrors etc.
And it is not well-vetted.
6. Please make sure you are using the commit hooks.  That will help us prevent from committing type errors.
7. We currently have "strict" turned off.  This can be enabled on a repo-by-repo basis.  It may be difficult to get 100%
strict coverage for our legacy code, but it should be enabled for new simulations.  You can see all of the options by
tracing through the tsconfig files.
9. Ambient type definitions are provided in chipper/phet-types.d.ts