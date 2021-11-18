## TypeScript Conventions

These are the conventions established for TypeScript use by PhET developers. This is an evolving document in an early
phase. Please bring things up for discussion to add here as you find new patterns.

### Leveraging Type Inference

See Item 19 "Avoid Cluttering Your Code with Inferable Types" in Vanderkam, which recommends (page 87):
* Avoid writing type annotations when TypeScript can infer the same type
* Ideally your code has type annotations in function/method signatures but not on local variables in their bodies
* Consider using explicit annotations for object literals and function return types even when they can be inferred.  This 
will help prevent implementation errors from surfacing in user code.
* It is PhET convention to provide return types to methods that are part of an interface and function declarations
(arrow functions as args are up to dev discretion).

TypeScript has a powerful type inference system, and we recommend to leverage that type inference in the general case.
For example:

```ts
// Recommended: infers type x:number
const x = 7;

// Not recommended, the type information is redundant.
const x: number = 7;
```

However, if there is a complicated or volatile (api hasn't stabilized) expression on the right-hand side, it may be
valuable on rare occasions to specify the type manually:

```ts
// OK to specify the type manually in complex or volatile cases
const x: number = someComplicatedExpressionOrVolatileStatementThatHasntStabilized();
```

This same principle applies to type parameters. For instance, TypeScript can infer the parametric type of `new Property`
based on the value of the first parameter.

```ts
// Recommended
new Property( new Laser() );

// Not recommended, type information is redundant
new Property<Laser>( new Laser() );
```

Again, in complex or volatile cases, at the developer preference, the redundant type annotations may prove useful.

### Access Modifiers

In TypeScript, the default visibility (if unspecified) is `public`. For methods, attributes, constructors, etc which are
intended to be public, the visibility modifier can be omitted. Or at the developer's discretion, `public` can be
specified.

```ts
class Clock {
  time: number; // ok 
  public age: number; // also ok
}
```

### Enumerations

Please see https://github.com/phetsims/wilder/blob/master/js/wilder/model/WilderEnumerationsTypescriptTestModel.ts

### Options and Config

Please see https://github.com/phetsims/wilder/blob/master/js/wilder/model/WilderOptionsTypescriptTestModel.ts

### Syntax in Type Declarations

We prefer to follow the TypeScript handbook and put semicolon delimiters in type declarations:

```ts
type Cat = {
  person: Person; // note the semicolons
  age: number;
}
```

### Initialization of Class Properties

When possible, it is preferable to initialize properties where they are declared and thus avoid an explicit
initialization statement in the constructor.

```ts
class EventCounter {
  public numberOfEvents: number = 0;

  // ...
}
```

### Documentation for Class Properties

Documentation for class properties should be placed with the declaration, not the instantiation. See, for
example https://github.com/phetsims/geometric-optics/blob/03e5637eb16600dd329e20f32fafc3ab99922c8a/js/common/model/GeometricOpticsModel.ts

```ts
class Person {

  // First and last name separate by a whitespace
  readonly name: string;

  constructor( name: string ) {
    this.name = name;
  }
}
```

### Multiple Exports in One Expression
Multiple exports should be combined into one expression.  This is advantageous for the same reason we often prefer
to have one return statement from functions.

```ts
// Recommended
export { CircuitElementViewType as default, CircuitElementViewTypeValues };

// Not recommended
export default CircuitElementViewType;
export { CircuitElementViewTypeValues };
```

### Multiple Imports in One Expression
Multiple imports from the same file should be combined into one expression.  This helps clarify that they are related.

```ts
// Preferred
import BendingLightScreenView, { BendingLightScreenViewOptions } from '../../common/view/BendingLightScreenView.js';

// Not preferred
import BendingLightScreenView from '../../common/view/BendingLightScreenView.js';
import { BendingLightScreenViewOptions } from '../../common/view/BendingLightScreenView.js';
```
If this exceeds the line limit and the WebStorm formatter wants to format it on multiple lines, please use
`// eslint-disable-line single-line-import`


### JSDoc and TSDoc

It is recommended that you do not duplicate parameter and return type information in JSDoc and in Typescript types. If
you have a need to explain one or more parameter, then add all parameters to the jsdoc and explain what you need. The
same for `@returns`.

###

Please see other notes in https://github.com/phetsims/ratio-and-proportion/issues/405
and https://github.com/phetsims/phet-info/blob/master/doc/typescript-quick-start.md 
