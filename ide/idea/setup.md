# Setup WebStorm and Intellij IDEA for PhET Development

*Disclaimer: Most of the PhET team uses WebStorm, but some use IDEA. If you're lucky, these instructions will work for
WebStorm and IDEA. But there may be differences between tools, or between versions. These instructions are intended to
get you pointed in the right direction. If you notice errors or a need for clarification, please update this document.*

1. Make sure that you have cloned all of the repos into a directory. First clone `perennial/`, and then run
   `perennial/bin/clone-missing-repos.sh`.
2. Run `npm install` (or if already existing, `npm prune` and `npm update`) under `chipper/` and `perennial/`
3. Make a new project in the same directory where you cloned all git repos. When asked, create a "Static Web" module for
   the same directory (if in Intellij IDEA).
4. Add your github credentials in `File > Settings > Version Control > Github`, and test your credentials with
   the `Test`
   button. (May need to hit "Create API Token")
5. Set up version control by adding each repo to git. This can be more automatic, because `.git` dirs are found by the
   system and you just have to 'Add Roots' in the event log.
   See https://www.jetbrains.com/help/idea/2017.1/using-git-integration.html.
6. `File > Project Structure > Modules` lets you exclude directories from your search path. You typically want to
   exclude
   `build/` and `node_modules/` for each repository, and all of `sherpa/`.
7. Set the right margin to appear after 120 characters. `File> Settings> Editor > CodeStyle` Set Default Options to 120.
8. Import the PhET code style (located in `phet-info/ide/idea/phet-idea-codestyle.xml`).
    * On a Mac, phet-idea-codestyle.xml must be manually copied
      to `$HOME/Library/Preferences/IntelliJIdea[**version**]/codestyles/`. Restart IDEA, then you can choose it
      from `Preferences > Editor > Code Style`.
    * See https://www.jetbrains.com/help/idea/2017.1/copying-code-style-settings.html. NOTE: For newer versions, you can
      press the drop-down "settings" icon to the right of the Scheme, select
      "Import Scheme", and navigate to where the code style is located (noted above).
9. Configure JavaScript level. In `File > Settings > Language & Frameworks > Javascript`, Make sure `ECMAScript 6` is
   selected, and check `Prefer Strict mode`.
10. Configure eslint. In `File > Settings > Language & Frameworks > Javascript > Code Quality Tools > Eslint`:
    * Select "Manual ESLint configuration"
    * Fill out ESLint package location (unless global, `chipper/node_modules/eslint`). (May be filled in automatically)
    * Configuration file: "Automatic search"
    * "Additional Rules Dir" should be `chipper/eslint/rules`
    * "Extra eslint options" needs to have `--resolve-plugins-relative-to=../chipper/`
    * [Here is a picture for a Windows](https://user-images.githubusercontent.com/6396244/157985259-def3f3f5-891f-4916-9276-c3ec7c15d1d8.png)
11. (Optional) Enable Nodejs coding assistance. `File > Settings > Language & Frameworks > Node.js and NPM`. Coding
    Assistance section. "Node.js Core is disabled" Enable it. This is handy if working on build tools/ node often.
12. Some inspections don't mesh well with the way our code base is setup, we can turn them off:
    * Go to File > Settings > Editor > Inspections.
    * When using `@extends` with `inherit` calls, you can get the entire constructor flagged with the warning:
      "Cyclic inheritance involving {TYPE}" -- Turn it off with JavaScript > General Closure compiler syntax.
13. We as a project prefer to use `@returns` over `@return` in jsdoc (there is even a lint rule for this), see
    https://github.com/phetsims/chipper/issues/557. To get Webstorm to auto fillin `@returns` when using
    the `/**[Enter]`
    template, follow these instructions: https://youtrack.jetbrains.com/issue/WEB-7516#comment=27-611256. Basically type
    `@retur` in a jsdoc comment and then select manually `returns` from the dialog that pops up. Webstorm will remember
    you selection.
14. Further resources:
    * [Here is a list of default keyboard shortcuts for windows and mac](https://resources.jetbrains.com/storage/products/intellij-idea/docs/IntelliJIDEA_ReferenceCard.pdf)
    * [Learn how to use multiple cursors!](https://www.jetbrains.com/webstorm/guide/tips/multi-cursor/)

## Preferences

These may not be required, but are settings that other developers have found useful for their coding style. Use at your
own risk!

* View Markdown preview horizontally split instead of
  vertically: `Languages & Frameworks > Markdown > Editor and Preview Panel Layout: Split horizontally`
* Move Editor tabs from the top to the right to maximize vertical
  space: `Editor > General > Editor Tabs > Tab placement: Right`
