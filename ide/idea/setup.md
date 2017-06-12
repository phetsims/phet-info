
# Setup Intellij IDEA for PhET Development

Note: links may be outdated, but they can get you started down the right track.

1. Make sure that you have cloned all of the repos into a directory. First clone chipper/ and then use 
`chipper/bin/clone-missing-repos.js`.
2. Set up version control by adding each repo to git. This is often done for you, because `.git` dirs are automatically
detected. See https://www.jetbrains.com/help/idea/2017.1/using-git-integration.html.
3. File > Project Structure > Modules lets you exclude directories from your search path. You typically want to exclude 
`build/` and `node_modules/` for each repository, and all of `sherpa/`.
4.Import the PhET code style (located in `phet-info/ide/idea/phet-idea-codestyle.xml`). 
    * On a Mac, phet-idea-codestyle.xml must be manually copied to `$HOME/Library/Preferences/IntelliJIdea[**version**]/codestyles/`. 
    Restart IDEA, then you can choose it from `Preferences > Editor > Code Style`.
    * See https://www.jetbrains.com/help/idea/2017.1/copying-code-style-settings.html.
5. Configure node. `File > Settings > Language & Frameworks > Javascript` Make sure you are using ECMA script 5. 
6. Configure eslint. `File > Settings > Language & Frameworks > Javascript > Code Quality Tools > Eslint`.
    * Then navigate to Language & Frameworks > JavaScript > Code Quality Tools > ESLint. 
    * Find your node.exe file (probably set up through the project).
    * Fill out ESLint package location (unless global, `chipper/node_modules/eslint`, you may have to `npm install` in chipper)
    * Configuration file should be `chipper/eslint/.eslintrc ` 
    * Additional Rules Dir should be `chipper/eslint/rules`
    * [Here is a picture for a mac](https://cloud.githubusercontent.com/assets/6856943/26806694/876bdad6-4a0f-11e7-9096-e734bf70be6e.png)
   
   