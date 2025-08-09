---
allowed-tools: Read, Edit, MultiEdit
argument-hint: <file-path>
description: Migrate constructor from JavaScript style to TypeScript style
---

Migrate all declarations in a constructor in the file @$ARGUMENTS from JavaScript style (no class attribute declarations) to TypeScript syntax (with class attribute declarations) following these rules:

1. Add type declarations for class attributes:
   - Documentation moves with the declaration.
   - Preserve or infer private/public/protected/readonly modifiers.
   - Preserve assignment in the constructor.

2. Preserve all documentation:
   - Keep method descriptions intact

3. Example transformation:
```typescript
// Before:

class MotionAtom {

  /**
   * @param initialAtomType - initial type, aka element, for this atom
   * @param initialXPosition - x position in the model, in picometers
   * @param initialYPosition - y position in the model, in picometers
   * @param tandem
   */
  public constructor( initialAtomType: AtomType, initialXPosition: number, initialYPosition: number, tandem: Tandem ) {

    // @public (read-write) {EnumerationDeprecatedProperty.<AtomType>} - the type of atom being modeled, e.g. Argon, Neon, etc.
    this.atomTypeProperty = new EnumerationDeprecatedProperty( AtomType, initialAtomType, {
      tandem: tandem.createTandem( 'atomTypeProperty' ),
      phetioReadOnly: true
    } );
    
// After:
class MotionAtom {

  // The type of atom being modeled, e.g. Argon, Neon, etc.
  public readonly atomTypeProperty: EnumerationDeprecatedProperty<AtomType>;
  
  /**
   * @param initialAtomType - initial type, aka element, for this atom
   * @param initialXPosition - x position in the model, in picometers
   * @param initialYPosition - y position in the model, in picometers
   * @param tandem
   */
  public constructor( initialAtomType: AtomType, initialXPosition: number, initialYPosition: number, tandem: Tandem ) {

    this.atomTypeProperty = new EnumerationDeprecatedProperty( AtomType, initialAtomType, {
      tandem: tandem.createTandem( 'atomTypeProperty' ),
      phetioReadOnly: true
    } );

```

4. Apply to ALL attributes in ALL constructors in the file
5. DO NOT change any runtime behavior - only type annotations, comments, and imports. Work in 100% type space and code comments/documentation.
6. Think carefully to figure out the imports. See if the type is already imported, or if you need to import it. If you need to import it, carefully compute the import path based on the current file's location.
8. Think about the file to understand if a declaration should be readonly. If you are uncertain, err on the side of readonly.
9. Think about the file to understand if a declaration should be public, protected, or private. If you are uncertain, err on the side of private.

8. If the file has:
```
/* eslint-disable */
// @ts-nocheck
```

LEAVE IT INTACT. Do not change. Keep it.