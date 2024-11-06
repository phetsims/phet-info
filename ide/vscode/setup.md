# Set up of VSCode IDE for PhET Development

## Configuring ESLint

UPDATE: As of Nov 2024, these instructions are out of date. We have upgraded to ESLint 9 which uses the flat config,
and have not tested VSCode support for ESLint since then.

1. You should have installed the ESLint VSCode Extension from the marketplace.
2. Your settings.json for ESLint should contain the following (Replace `ABSOLUTE_USER_PATH` with your computer's
   absolute path):

```
    {
        "eslint.nodePath": "ABSOLUTE_USER_PATH/phetsims/perennial-alias/node_modules",
        "eslint.options": {
            "cache": true,
            "ignorePath": "ABSOLUTE_USER_PATH/phetsims/chipper/eslint/.eslintignore",
            "resolvePluginsRelativeTo": "ABSOLUTE_USER_PATH/phetsims/chipper/",
            "rulePaths": [ "ABSOLUTE_USER_PATH/phetsims/chipper/eslint/rules" ],
            "extensions": [ ".js", ".ts" ]
        },
        "eslint.workingDirectories": [ { "mode": "auto" } ]
    }
```
