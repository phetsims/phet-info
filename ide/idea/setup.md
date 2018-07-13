
# Setup WebStorm and Intellij IDEA for PhET Development

*Disclaimer: Most of the PhET team uses WebStorm, but some use IDEA. If you're lucky, these instructions will work for WebStorm and IDEA. But there may be differences between tools, or between versions. These instructions are intended to get you pointed in the right direction.  If you notice errors or a need for clarification, please update this document.*

1. Make sure that you have cloned all of the repos into a directory. First clone `perennial/`, and then run
`perennial/bin/clone-missing-repos.sh`.                                                             
2. Run `npm install` (or if already existing, `npm prune` and `npm update`) under `chipper/` and `perennial/`
3. Make a new project at the same level as you parent dir to all git repos. When asked, create a "Static Web" module
    for the same directory (if in Intellij IDEA).
4. Add you github credentials in `File > Settings > Version Control > Github`, and test your credentials with the `Test` 
    button. (May need to hit "Create API Token")
5. Set up version control by adding each repo to git. This can be more automatic, because `.git` dirs are found by the system
    and you just have to 'Add Roots' in the event log. See https://www.jetbrains.com/help/idea/2017.1/using-git-integration.html.
6. `File > Project Structure > Modules` lets you exclude directories from your search path. You typically want to exclude 
`build/` and `node_modules/` for each repository, and all of `sherpa/`.
7. Set the right margin to appear after 120 characters. `File> Settings> Editor > CodeStyle` Set Default Options to 120.
8. Import the PhET code style (located in `phet-info/ide/idea/phet-idea-codestyle.xml`). 
    * On a Mac, phet-idea-codestyle.xml must be manually copied to `$HOME/Library/Preferences/IntelliJIdea[**version**]/codestyles/`. 
    Restart IDEA, then you can choose it from `Preferences > Editor > Code Style`.
    * See https://www.jetbrains.com/help/idea/2017.1/copying-code-style-settings.html.
    NOTE: For newer versions, you can press the drop-down "settings" icon to the right of the Scheme, select
    "Import Scheme", and navigate to where the code style is located (noted above).
9. Configure JavaScript level. In `File > Settings > Language & Frameworks > Javascript`, Make sure `ECMAScript 6` is
selected, and check `Prefer Strict mode`.
10. Configure eslint. In `File > Settings > Language & Frameworks > Javascript > Code Quality Tools > Eslint`:
    * Find your node.exe file (probably set up through the project). (May be filled in automatically)
    * Fill out ESLint package location (unless global, `chipper/node_modules/eslint`). (May be filled in automatically)
    * Configuration file should be `chipper/eslint/.eslintrc ` 
    * Additional Rules Dir should be `chipper/eslint/rules`
    * [Here is a picture for a mac](https://cloud.githubusercontent.com/assets/6856943/26806694/876bdad6-4a0f-11e7-9096-e734bf70be6e.png)
11. (Optional) Enable Nodejs coding assistance. `File > Settings > Language & Frameworks > Node.js and NPM`. Coding Assistance section. "Node.js Core is disabled" Enable it. This is handy if working on build tools/ node often.
12. Set up external tools for automatic import of require statement.
    * On Mac
        * preferences -> tools -> external tools:
        * program: grunt
        * parameters: insert-require-statement --file=$FilePath$ --name=$SelectedText$ --searchPath=/Users/samreid/github
        * working directory: /Users/samreid/github/circuit-construction-kit-dc
    * On Windows (unconfirmed if this works on Mac)
        * File -> Settings -> Tools -> External Tools . . . add new tool
        * Name it what ever you want
        * Program: `C:\Program Files\nodejs\node.exe`
        * Parameters: `C:\Users\{{USER_NAME}}\AppData\Roaming\npm\node_modules\grunt-cli\bin\grunt insert-require-statement --file=$FilePath$ --name=$SelectedText$ --searchPath={{PATH_TO_GIT_REPOS_DIR (like E:\Zepumph\Programming\PHET\git\)}}`
        * Working Directory: E:\Zepumph\Programming\PHET\git\faradays-law
13. Automatically `grunt lint-everything` on each commit
    * Preferences > Tools > External Tools, press the '+' button to add a tool with these values:
        * name: grunt-lint-everything
        * program: grunt
        * arguments: lint-everything
        * working directory: {{PATH_TO_CHECKOUT}}/perennial
    * Then in the commit changes dialog, select "After Commit" "Run Tool" "grunt-lint-everything"
14. Turn off some generally-incompatible inspections:
    * Go to File > Settings > Editor > Inspections.
    * Turn off JavaScript > General Closure compiler syntax
