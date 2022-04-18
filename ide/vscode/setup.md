# Set up of VSCode IDE for PhET Development
## Configuring ESLint
1. You should have installed the ESLint VSCode Extension from the marketplace.
2. Your settings.json for ESLint should contain the following (Replace `ABSOLUTE_USER_PATH` with your computer's absolute path):
```
    {
        "eslint.nodePath": "ABSOLUTE_USER_PATH/phetsims/chipper/node_modules",
        "eslint.options": {
            "cache": true,
            "ignorePath": "ABSOLUTE_USER_PATH/phetsims/chipper/eslint/.eslintignore",
            "resolvePluginsRelativeTo": "ABSOLUTE_USER_PATH/phetsims/chipper/",
            "rulePaths": [ "ABSOLUTE_USER_PATH/phetsims/chipper/eslint/rules" ],
            "extensions": [ ".js", ".ts" ],
            "baseConfig": {
                "extends": [ "ABSOLUTE_USER_PATH/phetsims/chipper/eslint/format_eslintrc.js" ]
            }
        },
        "eslint.workingDirectories": [ { "mode": "auto" } ]
    }
```
