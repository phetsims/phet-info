# Best Practices for Modules

This document summarizes PhET best practices for the use of ES6 modules. 
This was originally discussed in https://github.com/phetsims/chipper/issues/873.

## Do ...

* Include a default export, placed at the end of the .js file, e.g. `export default NumberControl;`

* Group all `imports` at the top of the .js file, immediately after the overview comment block, organized à la WebStorm "Organize Imports".

* Rename on import only if you have a name collision between imports, e.g.
```js
import { Line as SceneryLine } from '../../../../scenery/js/imports.js';
import Line from '../model/Line.js';
```

* Discuss exceptions to best practices on Slack, as they are encountered.  Modify the best practices if necessary, and/or document (at the call site) why you needed to diverge from the best practices.

## Do Not ...

* Do not use property notation for imports, e.g. `import * as lib from 'lib';`

* Do not use named exports.

* Do not use the `export` keyword inline, e.g. `export function createIcon(...) {...};`. This makes it impossible to identify what the module exports without scanning the entire .js file.

* Do not rename on export, e.g. `export { MY_CONST as THE_CONST };` 

* Do not rename on import, e.g. `import { named1 as myNamed1 } from 'src/mylib';`See exception above, for name collisions.

* Do not re-export, e.g. `export { foo } from 'src/other_module';`
