### TypeScript Quick Start

These are the basic steps and summary for converting a repo to TypeScript, how to use it, and summary of some workflows,
known problems, etc.

* This is an evolving project in the early phases. There will be growing pains. Discover problems, look for solutions!
* TypeScript seems like a great opportunity to increase efficiency/sanity and reduce bugs/stress. If the value it provides
   does not outweigh the costs of added complexity and compilation time, then we will abandon it. But before we consider that,
   let's give it a fair trial and see how much value it can provide.
* Please be aware of caveats listed below, as well as open issues in https://github.com/phetsims/chipper/issues?q=is%3Aissue+is%3Aopen+label%3Achipper%3Atypescript

### Getting started
1. Clone missing repos.  This makes sure you have everything.
2. Pull everything.  This makes sure you have the latest version of everything.
3. `npm install` in chipper. This makes sure you have the TypeScript compiler, which is called `tsc`
4. Mark chipper/dist/ as excluded from your IDE.  You can create that directory eagerly now, or wait until chipper/dist/ is created by a compilation step below. Compiled code will be written to chipper/dist/.
5. Update the code style file from phet-info/ide/idea/phet-idea-codestyle.xml which was last updated October 15, 2021
6. Turn on TypeScript support in WebStorm, at one point this was Languages & Frameworks -> TypeScript -> check TypeScript language services.
Sublime also has an officially supported plugin.

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
1. Install typescript with the same version as listed in chipper/package.json. You can do this globally via `npm install -g typescript@4.4.2`.
`tsc` is a program that comes bundled with the npm module `typescript`. Alternatively, you can set an
alias like `alias tsc = node /path/chipper/node_modules/typescript/bin/tsc`, which would make sure you are always using
the same version of typescript as in chipper.
2. Start a watch process by `cd chipper/tsconfig/all` and `tsc -b --watch`.  This will will watch for any file changes
and auto-recompile
3. I have not yet experimented with having the IDE do the builds, but maybe that will be more efficient.

### Process Changes
1. TypeScript sims need to be compiled before generating their API using `grunt generate-phet-io-api`
2. New sims need to be tracked in chipper/tsconfig/all/tsconfig.json

### Porting from JavaScript
1. I have found it efficient to convert a single file (or a small batch of related files) at a time.  Rename the file
from *.js to *.ts, fix any errors, wait for the watch process to compile, and run to test in the browser.  As you get
more skilled, you can convert more and more at once.
2. WebStorm provides helpful shortcuts.  For constructor parameters, you can promote constructor JSDoc params to types
via Option+Enter then "Annotate with Type from JSDoc".  You can automatically promote variables to class attributes with
Option+Enter then "Declare property [...]"
3. After all class attributes have been declared as class properties, you can mark each as `private readonly` then the
compiler will tell you where that needs to be relaxed.
4. Try to minimize their use as much as possible, but use `any` and `// @ts-ignore` to get past any insurmountable problems.
5. For pro users, once you are familiar with porting files, if you want to port more than one at a time, you can
use a command like this, but keep in mind you need to make sure they are `git mv` and not just `mv`.  You could update the command
or follow directions like https://github.com/phetsims/chipper/issues/1120#issuecomment-947090489
```
find . -name "*.js" ! -iname "*phet-io-overrides.js"  -exec bash -c 'mv "$1" "${1%.js}".ts' - '{}' \;
```

### Caveats and Notes
1. For now, please leave the phet-io-overrides.js file, strings file and namespace file as *.js.  The build tools are not set to do those in TypeScript yet.
2. Please do not convert common code to TypeScript until that phase is approved by the team.  Some common code repos have a "typescript" branch
for investigation in the meantime.
3. phettest and CT provide TypeScript support, but do not yet have a good user experience for showing TypeErrors etc.
And it is not well-vetted.
4. Please make sure you are using the commit hooks, which are configured to run type checks on typescript repos.
5. Ambient type definitions are provided in chipper/phet-types.d.ts
6. Transitive dependencies are not always tracked correctly in the build system.  This bug has been reported to TypeScript. Details in https://github.com/phetsims/chipper/issues/1067
7. Some common code repos include code outside their directory.  This problem is described in https://github.com/phetsims/chipper/issues/1096
8. Gravity and Orbits, Bending Light, and Circuit Construction Kit Common have been written in TypeScript, and are all
at approximately equal levels, and can be used for reference. For instance, see how these sims have a d.ts file for strings.
However, please do not use any reference of code marked with
`@ts-ignore` or `any`.  Those markers mean (a) I wasn't sure what to do, (b) common code is not ready to support it yet or (c) I haven't
taken the time to properly type it yet.  I also recommend avoiding `!` non-null coercion if you can help it.
