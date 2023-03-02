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
   the `Test` button. (May need to hit "Create API Token")
5. Set up version control by adding each repo to git. This can be more automatic, because `.git` dirs are found by the
   system and you just have to 'Add Roots' in the event log.
   See https://www.jetbrains.com/help/idea/2017.1/using-git-integration.html. You can confirm that all repos are
   registered with git in     
   Preferences -> Version Control -> Directory Mappings
6. `File > Settings > Directories` (or `File > Project Structure > Modules` if in Intellij IDEA) lets you exclude
   directories from your search path. Here are the folders you most likely want to exclude:
    * `build/`, `node_modules/`, `images/`, `sounds/`, `mipmaps/` for each repository,
    * `sherpa/`.
    * `dist/`,
    * `babel/` (not all devs like doing this, up to you)
    * Here is an example command to paste into the
      setting: `build;node_modules;dist;images;sounds;mipmaps;*phet-io-elements-overrides.js;*phet-io-elements-baseline.js`
      into "Excluded Files".
7. Set the right margin to appear after 120 characters. `File> Settings> Editor > Code Style` Set Default Options to
    120.
8. Import the PhET code style (located in `phet-info/ide/idea/phet-idea-codestyle.xml`).
    * See https://www.jetbrains.com/help/idea/2017.1/copying-code-style-settings.html. Press the drop-down "settings"
      icon to the right of the Scheme, select "Import Scheme", and navigate to where the code style is located (noted
      above).
    * On older Mac versions, phet-idea-codestyle.xml must be manually copied to
      $HOME/Library/Preferences/IntelliJIdea[**version**]/codestyles/. Restart IDEA, then you can choose it from
      Preferences > Editor > Code Style.
9. Configure JavaScript level. In `File > Settings > Language & Frameworks > JavaScript`, Make sure `ECMAScript 6` is
   selected.
10. Configure eslint. In `File > Settings > Language & Frameworks > JavaScript > Code Quality Tools > ESLint`:
    * Select "Manual ESLint configuration"
    * Fill out ESLint package location (unless global, `chipper/node_modules/eslint`). (May be filled in automatically)
    * Configuration file: "Automatic search"
    * "Additional Rules Dir" should be `chipper/eslint/rules`
    * "Extra eslint options" needs to have `--resolve-plugins-relative-to=../chipper/`
    * "Run For Files": add a couple file extensions: `{**/*,*}.{js,ts,jsx,tsx,html,mjs,cjs}`
    * [Here is a picture for a Windows](https://user-images.githubusercontent.com/6396244/157985259-def3f3f5-891f-4916-9276-c3ec7c15d1d8.png)
11. (Optional) Enable Nodejs coding assistance. `File > Settings > Language & Frameworks > Node.js and NPM`. Coding
    Assistance section. "Node.js Core is disabled" Enable it. This is handy if working on build tools/ node often.
12. We as a project prefer to use `@returns` over `@return` in jsdoc (there is even a lint rule for this), see
    https://github.com/phetsims/chipper/issues/557. To get Webstorm to auto filling `@returns` when using
    the `/**[Enter]`
    template, follow these instructions: https://youtrack.jetbrains.com/issue/WEB-7516#comment=27-611256. Basically type
    `@retur` in a jsdoc comment and then select manually `returns` from the dialog that pops up. Webstorm will remember
    you selection.
13. Further resources:
    * [Here is a list of default keyboard shortcuts for windows and mac](https://resources.jetbrains.com/storage/products/intellij-idea/docs/IntelliJIDEA_ReferenceCard.pdf)
    * [Learn how to use multiple cursors!](https://www.jetbrains.com/webstorm/guide/tips/multi-cursor/)

## Suggestions

These may not be required, but are settings or features that other developers have found useful for their coding style.
Use at your own risk!

* View Markdown preview horizontally split instead of
  vertically: `Languages & Frameworks > Markdown > Editor and Preview Panel Layout: Split horizontally`
* Move Editor tabs from the top to the right to maximize vertical
  space: `Editor > General > Editor Tabs > Tab placement: Right`
* Name collisions with built-in types can make adding imports difficult. The following suggestions are ways to get
  around this problem.
    * Using "Code completion->Basic" (ctrl+space from default MacOS bindings) will only work if you are already
      importing from scenery imports.
    * A way around this is to auto-import a class with a name that is non built-in type to get scenery imports.js in
      your file automatically. Then you can auto import the file with a built-in type name and delete the first one.
* [Live Templates](https://www.jetbrains.com/help/idea/using-live-templates.html#live_templates_types) are a feature
  that many devs use for quickly typing out common patterns in code. To try some out, ask a developer for some examples
  of their favorites. A set of live templates can be exported from one instance of WebStorm and imported in another.
* Many devs use [patches](https://www.jetbrains.com/help/webstorm/using-patches.html) for quickly sharing code changes
  with other developers. They are most commonly used for:
    * Sending code changes over Slack when developers are pairing together and they need to switch who is leading
    * Adding code changes to a GitHub issue for other devs to try out. Often times, you may see patches contained
      in a "details" dropdown (notated as `<details>`) since they can be very long.
* It can be helpful to see the history of a file or section of a file that you're working in. This is not
  only a way to see how a section of code came to be, but also which devs made the changes. See documentation on
  the [Show History](https://www.jetbrains.com/help/webstorm/investigate-changes.html#file-history) feature (or
  do `Right click > Git > Show History/Show History for Selection`).
