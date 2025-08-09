---
allowed-tools: Read, Edit, MultiEdit
argument-hint: <file-path>
description: Migrate TypeScript method signatures from JSDoc to TypeScript syntax
---

Migrate all method signatures + constructor signatures in the file @$ARGUMENTS from JSDoc type annotations to TypeScript syntax following these rules:

1. Convert JSDoc method signatures to TypeScript:
   - Move type annotations from `@param {Type}` to TypeScript parameter types
   - Move `@returns {Type}` to TypeScript return type annotation
   - Move `@private`, `@public`, `@protected` to TypeScript modifiers

2. Preserve all documentation:
   - Keep method descriptions intact
   - Keep parameter descriptions (after the hyphen in `@param`)
   - Keep return value descriptions, if any

3. Clean up JSDoc:
   - Remove all `@param` tags if and if none have documentation (only type)
   - Remove `@returns` tags that have no documentation (only type)
   - Keep `@param name - description` format for documented parameters
   - Keep `@returns description` format for documented return values

4. Example transformation:
   ```typescript
   // Before:
   /**
    * Given an (initial) position, find a position with the targeted electric potential
    * @private
    * @param {Vector2} position
    * @param {number} electricPotential
    * @param {number} deltaDistance - a distance in meters
    * @returns {Vector2} finalPosition
    */
   getNextPosition( position, electricPotential, deltaDistance ) {

   // After:
   /**
    * Given an (initial) position, find a position with the targeted electric potential
    * @param position
    * @param electricPotential
    * @param deltaDistance - a distance in meters
    */
   private getNextPosition( position: Vector2, electricPotential: number, deltaDistance: number ): Vector2 {
   ```

5. Apply to all methods in the file (static and instance methods)
6. DO NOT change any runtime behavior - only type annotations, comments, and imports
7. Think carefully to figure out the imports. See if the type is already imported, or if you need to import it. If you need to import it, carefully compute the import path based on the current file's location.
8. Visit the constructors as well, but JSDOC and signature ONLY.
9. Move `@override` jsdoc to the typescript keyword like `public override myMethod(...)`
10. `constructor` should be made public, i.e. `public constructor(...)`
11. If the resultant JSDoc is blank, like
```
  /**
   */
```

Then remove it entirely.
12. If the method has no return type, then `: void` must be explictly added to the method signature.

13. If the file has:
```
/* eslint-disable */
// @ts-nocheck
```

LEAVE IT INTACT. Do not change. Keep it.