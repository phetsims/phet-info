# Setup WebStorm and Intellij IDEA for PhET Development

*Disclaimer: Most of the PhET team uses WebStorm, but some use IDEA. If you're lucky, these instructions will work for
WebStorm and IDEA. But there may be differences between tools, or between versions. These instructions are intended to
get you pointed in the right direction. If you notice errors or a need for clarification, please update this document.*

1. Make sure that you have a checked out code base. Clone perennial manually, run `npm install`, and then `grunt sync`.
3. Make a new project in the same directory where you cloned all git repos. When asked, create a "Static Web" module for
   the same directory (if in Intellij IDEA).
4. Add your github credentials in `File > Settings > Version Control > Github`, and test your credentials with the
   `Test` button. (May need to hit "Create API Token")
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
* Here is an example command to paste into the setting:
  `build;node_modules;dist;images;sounds;mipmaps;*phet-io-elements-overrides.js;*phet-io-elements-baseline.js`
  into "Excluded Files".

7. Set the right margin to appear after 120 characters. `File> Settings> Editor > Code Style` Set Default Options to
120.
8. Import the PhET code style (located in `phet-info/ide/idea/phet-idea-codestyle.xml`).

* See https://www.jetbrains.com/help/idea/2017.1/copying-code-style-settings.html. Press the drop-down "settings"
  icon to the right of the Scheme, select "Import Scheme", and navigate to where the code style is located (noted
  above).
* On older Mac versions, phet-idea-codestyle.xml must be manually copied to $HOME/Library/Preferences/IntelliJIdea[*
  *version**]/codestyles/. Restart IDEA, then you can choose it from Preferences > Editor > Code Style.

9. Configure JavaScript level. In `File > Settings > Language & Frameworks > JavaScript`, Make sure `ECMAScript 6` is
   selected.
10. Configure eslint. In `File > Settings > Language & Frameworks > JavaScript > Code Quality Tools > ESLint`:

* Select "Manual ESLint configuration"
* Fill out ESLint package location (unless global, `perennial-alias/node_modules/eslint`). (May be filled in
  automatically)
* Configuration file: "Automatic search"
* Add command line arguments: `--flag unstable_config_lookup_from_file`. This normalizes the behavior of
  eslint.config.mjs file lookup and will be necessary until we migrate to ESLint 10.0, where the flag will no longer be
  necessary.
* "Run For Files": add a couple file extensions: `{**/*,*}.{js,ts,jsx,tsx,html,mjs,cjs}`

11. (Optional) Enable Nodejs coding assistance. `File > Settings > Language & Frameworks > Node.js and NPM`. Coding
    Assistance section. "Node.js Core is disabled" Enable it. This is handy if working on build tools/ node often.
12. We as a project prefer to use `@returns` over `@return` in jsdoc (there is even a lint rule for this), see
    https://github.com/phetsims/chipper/issues/557. To get Webstorm to auto filling `@returns` when using the
    `/**[Enter]`
    template, follow these instructions: https://youtrack.jetbrains.com/issue/WEB-7516#comment=27-611256. Basically type
    `@retur` in a jsdoc comment and then select manually `returns` from the dialog that pops up. Webstorm will remember
    you selection.
13. Further resources:

* [Here is a list of default keyboard shortcuts for windows and mac](https://resources.jetbrains.com/storage/products/intellij-idea/docs/IntelliJIDEA_ReferenceCard.pdf)
* [Learn how to use multiple cursors!](https://www.jetbrains.com/webstorm/guide/tips/multi-cursor/)

14. Configure TypeScript to use types from the server.

* Settings > Languages & Frameworks > TypeScript:
  * "use types from server" should be checked
  * Typescript package should point to `perennial-alias\node_modules\typescript`
* See https://www.jetbrains.com/help/webstorm/typescript-support.html#ws_ts_use_ts_service_checkbox

## Suggestions

These may not be required, but are settings or features that other developers have found useful for their coding style.
Use at your own risk!

* View Markdown preview horizontally split instead of vertically:
  `Languages & Frameworks > Markdown > Editor and Preview Panel Layout: Split horizontally`
* Move Editor tabs from the top to the right to maximize vertical space:
  `Editor > General > Editor Tabs > Tab placement: Right`
* Name collisions with built-in types can make adding imports difficult. The following suggestions are ways to get
  around this problem.
* [Live Templates](https://www.jetbrains.com/help/idea/using-live-templates.html#live_templates_types) are a feature
  that many devs use for quickly typing out common patterns in code. To try some out, ask a developer for some examples
  of their favorites. A set of live templates can be exported from one instance of WebStorm and imported in another.
* Many devs use [patches](https://www.jetbrains.com/help/webstorm/using-patches.html) for quickly sharing code changes
  with other developers. They are most commonly used for:
  * Sending code changes over Slack when developers are pairing together and they need to switch who is leading
  * Adding code changes to a GitHub issue for other devs to try out. Often times, you may see patches contained in a "
    details" dropdown (notated as `<details>`) since they can be very long.
* The "find" modal has a preview section that some want to see more than 100 items in it, instead of needing to open the
  Find view. Increase this number with "Settings > Advanced Settings > Maximum number of results to show in Find in
  Files/Show Usages preview"
* **External Tools** can be incredibly helpful. @samreid and @zepumph are great resources for this. They can also be
  bound to keyboard shortcuts. For example, syncing and pushing scripts.
  * Windows:
    * To add a shell script tool that runs sync:
      * Program:  C:\Program Files\Git\bin\bash.exe
      * Arguments: bin\sage run js\grunt\tasks\sync.ts --AN_OPTION_HERE
      * Working Directory: GIT_REPOS\perennial
    * To add an external tool on Windows that supports full color, do something like this:
      * Program:  C:\Program Files\Git\bin\bash.exe
      * Arguments: -c "export FORCE_COLOR=true; ./perennial/bin/sage run ./website-build/gitFlow/updateWebsiteRepos.ts
        --sync"
      * Working Directory: GIT_REPOS
  * Mac:
    * Sync
      * Program: /bin/zsh
      * Arguments: -c "source ~/.intellijprofilesr; grunt sync --checkoutMain=false"
      * Working Directory: GIT_REPOS/perennial
    * Precommit Hooks on repos with changes
      * Program: /bin/zsh
        * Arguments: -c "source ~/.intellijprofilesr; bin/sage run ../chipper/js/grunt/tasks/pre-commit.ts --changed --lint --report-media --type-check --test --absolute"
        * Working Directory: GIT_REPOS/perennial-alias
        * Output Filters: $FILE_PATH$\($LINE$\,$COLUMN$\)
* It can be helpful to see the history of a file or section of a file that you're working in. This is not only a way to
  see how a section of code came to be, but also which devs made the changes. See documentation on
  the [Show History](https://www.jetbrains.com/help/webstorm/investigate-changes.html#file-history) feature (or do
  `Right click > Git > Show History/Show History for Selection`).
* There are many PhET words that webstorm will flag incorrectly as spelling errors. You may want to preempt this by
  adding these to your local dictionary in `Editor -> Natural Languages -> Spelling`
  <details>

  * assistive
  * autoselect
  * autoselectable
  * blackman
  * bugginess
  * codap
  * eall
  * eslint
  * falsey
  * grapher
  * interoperated
  * kauzmann
  * klusendorf
  * layerable
  * lightyear
  * multilink
  * multitouch
  * operationalize
  * optionize
  * pdom
  * phet
  * phetio
  * phetmarks
  * phetsim
  * phetsims
  * phettest
  * pickability
  * pickable
  * popupable
  * proccessed
  * recursed
  * renameable
  * runnables
  * sonification
  * sonify
  * substate
  * toggler
  * translatability
  * unbuilt
  * unclamped
  * unclickable
  * undefer
  * uninstrument
  * uninstrumentation
  * uninstrumented
  * unpickable
  </details>
