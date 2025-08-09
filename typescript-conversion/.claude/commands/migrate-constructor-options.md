---
allowed-tools: Read, Edit, MultiEdit
argument-hint: <file-path>
description: Migrate constructor from JavaScript style to TypeScript style
---

Migrate all options parameters in constructors in the file @$ARGUMENTS from JavaScript style (no types) to PhET's optionize TypeScript pattern (with types) following these rules:

1. Rename `options` to `providedOptions`.
   - Make sure to visit every occurrence of this variable in its scope.
   - Note that there may be multiple constructors or other methods with `options`, so take care.

2. Change `merge` to `optionize`

3. Example transformation:
```typescript

// BEFORE:

import merge from '../../../../phet-core/js/merge.js';
import Image from '../../../../scenery/js/nodes/Image.js';
import RectangularPushButton from '../../../../sun/js/buttons/RectangularPushButton.js';
import pencil_png from '../../../mipmaps/pencil_png.js';
import chargesAndFields from '../../chargesAndFields.js';

class PencilButton extends RectangularPushButton {

  /**
   * @param {Tandem} tandem
   * @param {Object} [options]
   */
  constructor( tandem, options ) {
    options = merge( {
      iconWidth: 26,
      iconHeight: 20,
      tandem: tandem
    }, options );


// AFTER:

import optionize from '../../../../phet-core/js/optionize.js';
import Image from '../../../../scenery/js/nodes/Image.js';
import RectangularPushButton, { RectangularPushButtonOptions } from '../../../../sun/js/buttons/RectangularPushButton.js';
import Tandem from '../../../../tandem/js/Tandem.js';
import pencil_png from '../../../mipmaps/pencil_png.js';
import chargesAndFields from '../../chargesAndFields.js';

type SelfOptions = {
  iconWidth?: number;
  iconHeight?: number;
};

type PencilButtonOptions = SelfOptions & RectangularPushButtonOptions;

export default class PencilButton extends RectangularPushButton {

  public constructor( tandem: Tandem, providedOptions?: PencilButtonOptions ) {

    const options = optionize<PencilButtonOptions, SelfOptions, RectangularPushButtonOptions>()( {
      iconWidth: 26,
      iconHeight: 20,
      tandem: tandem
    }, providedOptions );
```

4. Apply to options parameters in ALL constructors in the file
5. DO NOT change any runtime behavior - only type annotations, comments, and imports. Work in 100% type space and code comments/documentation.
6. If there are no new options introduced for the constructor at hand, then use `type SelfOptions = EmptySelfOptions`. You can get EmptySelfOptions from `import optionize, { type EmptySelfOptions } from '../../phet-core/js/optionize.js';`
7. NOTE: The implementation of `optionize` is identical to `merge`, so you can be confident the behavior is the same. These changes are solely for type space.
8. If the parent doesn't export its own options type, you can jump to the grandparent class for its options type.
9. If `merge` is used elsewhere in the file, do not remove the import!
10. If the file has:
```
/* eslint-disable */
// @ts-nocheck
```

LEAVE IT INTACT. Do not change. Keep it.