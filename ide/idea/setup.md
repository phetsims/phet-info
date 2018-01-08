
# Setup Intellij IDEA for PhET Development

Note: links may be outdated for the current version of Intellij, but they can get you started down the right track.

1. Make sure that you have cloned all of the repos into a directory. First clone `perennial/`, and then use
`chipper/bin/clone-missing-repos.sh`.
2. Make a new project at the same level as you parent dir to all git repos.
3. Add you github credentials in `File > Settings > Version Control > Github`, and test your credentials with the `Test` 
    button.
4. Set up version control by adding each repo to git. This can be more automatic, because `.git` dirs are found by the system
    and you just have to 'Add Roots' in the event log. See https://www.jetbrains.com/help/idea/2017.1/using-git-integration.html.
5. `File > Project Structure > Modules` lets you exclude directories from your search path. You typically want to exclude 
`build/` and `node_modules/` for each repository, and all of `sherpa/`.
6. Set the right margin to appear after 120 characters. `File> Settings> Editor > CodeStyle` Set Default Options to 120.
7. Import the PhET code style (located in `phet-info/ide/idea/phet-idea-codestyle.xml`). 
    * On a Mac, phet-idea-codestyle.xml must be manually copied to `$HOME/Library/Preferences/IntelliJIdea[**version**]/codestyles/`. 
    Restart IDEA, then you can choose it from `Preferences > Editor > Code Style`.
    * See https://www.jetbrains.com/help/idea/2017.1/copying-code-style-settings.html.
8. Configure node. `File > Settings > Language & Frameworks > Javascript` Make sure `   ECMAScript 5.1` is selected, and 
    check `Prefer Strict mode. 
9. Configure eslint. `File > Settings > Language & Frameworks > Javascript > Code Quality Tools > Eslint`.
    * Then navigate to `Language & Frameworks > JavaScript > Code Quality Tools > ESLint`. 
    * Find your node.exe file (probably set up through the project).
    * Fill out ESLint package location (unless global, `chipper/node_modules/eslint`, you may have to `npm install` in chipper)
    * Configuration file should be `chipper/eslint/.eslintrc ` 
    * Additional Rules Dir should be `chipper/eslint/rules`
    * [Here is a picture for a mac](https://cloud.githubusercontent.com/assets/6856943/26806694/876bdad6-4a0f-11e7-9096-e734bf70be6e.png)
10. (Optional) Enable Nodejs coding assistance. `File > Settings > Language & Frameworks > Node.js and NPM`. Coding Assistance section. "Node.js Core is disabled" Enable it. This is handy if working on build tools/ node often.
11. Set up external tools for automatic import of require statement. 
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
