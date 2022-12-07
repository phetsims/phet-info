### TypeScript Quick Start

These are the basic steps and summary for converting a repo to TypeScript, how to use it, and summary of some workflows,
known problems, etc.

* This is an evolving project in the early phases. There will be growing pains. Discover problems, look for solutions!
* TypeScript seems like a great opportunity to increase efficiency/sanity and reduce bugs/stress. If the value it
  provides does not outweigh the costs of added complexity and compilation time, then we will abandon it. But before we
  consider that, let's give it a fair trial and see how much value it can provide.
* Please be aware of caveats listed below, as well as open issues
  in https://github.com/phetsims/chipper/issues?q=is%3Aissue+is%3Aopen+label%3Achipper%3Atypescript

### Getting Started

1. Clone missing repos by running `perennial/bin/clone-missing-repos.sh`. This ensures that you have everything.
2. Pull all repos by running `perennial/bin/pull-all.sh`. This ensures that you have the latest version of everything.
3. `npm install` in chipper. This ensures that you have the TypeScript compiler, which is called `tsc`
4. Add an alias like this to your terminal `alias tsc='node /my-path-to/chipper/node_modules/typescript/bin/tsc'`
5. Mark chipper/dist/ as excluded from your IDE. You can create that directory eagerly now, or wait until chipper/dist/
   is created by a compilation step below. Compiled code will be written to chipper/dist/.
6. Update your IDE to use the code style file from `phet-info/ide/idea/phet-idea-codestyle.xml`. You may need to
   re-import the xml file so that your IDE picks up any changes related to TypeScript. Your IDE may not stay in sync
   with what is checked into phet-info.
7. Turn on TypeScript support in WebStorm: Preferences > Languages & Frameworks > TypeScript. Make sure you are using
   your system's absolute path for `chipper/node_modules/typescript`, turn on "TypeScript language service" and "Show
   project errors". Turn off "Recompile on changes".
8. Sublime also has an officially-supported plugin.

### Converting a Repo to TypeScript

1. Add the following type declarations to the `"include"` array in tsconfig.json (
   see https://github.com/phetsims/chipper/issues/1121)

```json
"../chipper/phet-types.d.ts",
"../chipper/node_modules/@types/lodash/index.d.ts",
"../chipper/node_modules/@types/qunit/index.d.ts"
```

Congratulations!  Now the repo is TypeScript-capable. You can commit these changes if you wish.

### Transpile TypeScript

* Change directory to the build tools: `cd chipper/`
* Run the TypeScript transpiler: `node js/scripts/transpile.js --watch` which starts a process that will auto-transpile
  when files change.
* If you prefer to experiment with using WebStorm/IDEA File Watchers, please
  see https://github.com/phetsims/phet-info/blob/master/doc/typescript-webstorm-file-watcher.md

### Experiment with your new TypeScript repo

1. Open the sim in the browser via phetmarks.
2. Rename one of the files to *.ts and add code like `const x:number=7; console.log(x);` .
3. Transpile following the instructions above and run it in the browser. Did it print `7`?
4. Try creating a type error like `const x:string=7` and see what happens.

### Porting from JavaScript

1. I have found it efficient to convert a single file (or a small batch of related files) at a time. Rename the file
   from *.js to *.ts, fix any errors, wait for the watch process to compile, and run to test in the browser. As you get
   more skilled, you can convert more and more at once.
2. WebStorm provides helpful shortcuts. For constructor parameters, you can promote constructor JSDoc params to types
   via Option+Enter then "Annotate with Type from JSDoc". You can automatically promote variables to class attributes
   with Option+Enter then "Declare property [...]"
3. After all class attributes have been declared as class properties, you can mark each as `private readonly` then the
   compiler will tell you where that needs to be relaxed.
4. Try to minimize its use as much as possible, but use `// @ts-expect-error` to get past any insurmountable
   problems.  We prefer that to `// @ts-ignore` so it will tell you if there is no problem. Please also add 
   a message about why there is an error there.
5. For pro users, once you are familiar with porting files, if you want to port more than one at a time, you can use a
   command like this, but keep in mind you need to make sure they are `git mv` and not just `mv`. You could update the
   command or follow directions like https://github.com/phetsims/chipper/issues/1120#issuecomment-947090489

```
find . -name "*.js" ! -iname "*phet-io-overrides.js"  -exec bash -c 'mv "$1" "${1%.js}".ts' - '{}' \;
```

### Caveats and Notes

1. For now, please leave the phet-io-overrides.js file, strings file and namespace file as *.js. The build tools are not
   set to do those in TypeScript yet.
2. phettest and CT provide TypeScript support, but do not yet have a good user experience for showing TypeErrors etc.
   And it is not well-vetted.
3. Please make sure you are using the commit hooks, which are configured to run type checks on typescript repos.
4. Ambient type definitions are provided in chipper/phet-types.d.ts
5. Transitive dependencies are not always tracked correctly in the build system. This bug has been reported to
   TypeScript. Details in https://github.com/phetsims/chipper/issues/1067
6. Some common code repos include code outside their directory. This problem is described
   in https://github.com/phetsims/chipper/issues/1096
7. Conventions and patterns listed in https://github.com/phetsims/phet-info/blob/master/doc/typescript-conventions.md
8. For certain files, when changing JS=>TS, WebStorm will say it is a rename in the commit dialog, then show a “delete +
   create” in the history. This is not desirable. For those files, a workaround is to rename the file with no content
   changes, then change the contents in a separate commit. We no longer are using `@ts-nocheck` as part of this process
   because it wasn't worth the cost, and this doesn't prevent downstream errors by files that use your converting file
   as a dependency. This came from https://github.com/phetsims/sun/issues/732#issuecomment-995330513.
