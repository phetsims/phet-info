### TypeScript Quick Start

These are the basic steps and summary for converting a repo to TypeScript, how to use it, and summary of some workflows,
known problems, etc.

### Getting Started

1. Update your codebase to support typescript features with `cd perennial; grunt sync;`
2. Mark chipper/dist/ as excluded from your IDE. You can create that directory eagerly now, or wait until chipper/dist/
   is created by a compilation step below. Compiled code will be written to chipper/dist/.
3. Update your IDE to use the code style file from `phet-info/ide/idea/phet-idea-codestyle.xml`. You may need to
   re-import the xml file so that your IDE picks up any changes related to TypeScript. Your IDE may not stay in sync
   with what is checked into phet-info.
4. Turn on TypeScript support in WebStorm: Preferences > Languages & Frameworks > TypeScript. Make sure you are using
   your system's absolute path for `perennial-alias/node_modules/typescript`, turn on "TypeScript language service"
   and "Show project errors". Turn off "Recompile on changes".
5. Sublime also has an officially-supported plugin.

### Porting from JavaScript

1. Rename the file from *.js to *.ts. This must be committed as a pure rename, without changing contents. If you change
   the content more than a small amount, git will think it is a delete and create, which will lose the history of the
   file. Use `git mv` to rename the file, or if you are using WebStorm, it will do this automatically for you. See https://github.com/phetsims/sun/issues/732#issuecomment-995330513 and https://github.com/phetsims/charges-and-fields/issues/208#issuecomment-3134618756
2. I have found it efficient to convert a single file (or a small batch of related files) at a time. Rename the file
   from *.js to *.ts, fix any errors, run `grunt type-check` and `grunt lint`, and run to test in the browser. As you
   get more skilled, you can convert more and more at once.
3. WebStorm provides helpful shortcuts. For constructor parameters, you can promote constructor JSDoc params to types
   via Option+Enter then "Annotate with Type from JSDoc". You can automatically promote variables to class attributes
   with Option+Enter then "Declare property [...]"
4. After all class attributes have been declared as class properties, you can mark each as `private readonly` then the
   compiler will tell you where that needs to be relaxed.
5. Try to minimize its use as much as possible, but use `// @ts-expect-error` to get past any insurmountable problems.
   We prefer that to `// @ts-ignore` so it will tell you if there is no problem. Please also add a message about why
   there is an error there.

### Caveats and Notes

1. Ambient type definitions are provided in perennial-alias/phet-types.d.ts and chipper/phet-types-module.d.ts
2. Conventions and patterns listed in https://github.com/phetsims/phet-info/blob/main/doc/typescript-conventions.md
3. For certain files, when changing JS=>TS, WebStorm will say it is a rename in the commit dialog, then show a “delete +
   create” in the history. This is not desirable. For those files, a workaround is to rename the file with no content
   changes, then change the contents in a separate commit. We no longer are using `@ts-nocheck` as part of this process
   because it wasn't worth the cost, and this doesn't prevent downstream errors by files that use your converting file
   as a dependency. This came from https://github.com/phetsims/sun/issues/732#issuecomment-995330513.
