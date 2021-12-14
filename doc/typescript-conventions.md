## TypeScript Conventions

These are the conventions established for TypeScript use by PhET developers. This is an evolving document in an early
phase. Please bring things up for discussion to add here as you find new patterns.

### Leveraging Type Inference

From _Effective TypeScript_ (Dan Vanderkan), page 87, Item 19, "Avoid Cluttering Your Code with Inferable Types":
* Avoid writing type annotations when TypeScript can infer the same type.
* Ideally your code has type annotations in function/method signatures but not on local variables in their bodies.
* Consider using explicit annotations for object literals and function return types even when they can be inferred.  This 
will help prevent implementation errors from surfacing in user code.

It is PhET convention to provide return types when declaring methods and functions.
(Arrow functions as args are up to dev discretion.)

TypeScript has a powerful type inference system, and we recommend to leverage that type inference in the general case.
For example:

```ts
// Recommended: infers type x:number
const x = 7;

// Not recommended, the type information is redundant.
const x: number = 7;
```

However, if there is a complicated or volatile (API hasn't stabilized) expression on the right-hand side, it may be
valuable to specify the type on the left-hand side. For example:

```ts
// OK to specify the type manually in complex or volatile cases
const x: number = someComplicatedExpressionOrVolatileStatementThatHasntStabilized();
```

This same principle applies to generic type parameters. For instance, TypeScript can infer the parametric type of `new Property`
based on the value of the first parameter. For example:

```ts
// Recommended
new Property( new Laser() );

// Not recommended, type information is redundant
new Property<Laser>( new Laser() );
```

Again, in complex or volatile cases, at the developer preference, the redundant type annotations may prove useful.

### Access Modifiers

In TypeScript, the default access modifier (if unspecified) is `public`. For methods, attributes, constructors, etc. which are
intended to be public, the access modifier can be omitted. Or at the developer's discretion, `public` can be
specified.

```ts
class Clock {
  time: number; // ok 
  public age: number; // also ok
}
```

### Enumerations

Please see https://github.com/phetsims/wilder/blob/master/js/wilder/model/WilderEnumerationPatterns.ts

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
initialization statement in the constructor. For example:

```ts
class EventCounter {
  public numberOfEvents: number = 0;

  // ...
}
```

### Documentation for Class Properties

Documentation for class properties should be placed with the declaration, not the instantiation. For example:

```ts
class Person {

  // First and last name separate by a whitespace
  readonly name: string;

  constructor( name: string ) {
    this.name = name;
  }
}
```

### Multiple Exports
PhET uses babel to do transpilation, and it only operates on a single file at a time. This means that it can’t apply code transforms that depend on understanding the full type system, and we are restricted to specifying [isolatedModules](https://www.typescriptlang.org/tsconfig#isolatedModules) in tsconfig. This in turn requires that types must be exported separately from other modules. For example:

```ts
type NodeOption = ...;
class Node { ... }

export { NodeOptions };
export { Node as default };
```

When exporting multiple modules, all types should be combined into 1 `export` statement, and all non-types should be combined into 1 `export` statement. So a .ts file should have at most 2 `export` statements. For example:

```ts
type DogOptions = ...;
type CollarOptions = ...;

class Dog { ... }
class Collar { ... }

export { DogOptions, CatOptions }; 
export { Dog as default, Collar };
```

### Multiple Imports in One Expression
Multiple imports from the same file should be combined into one statement.  This helps clarify that they are related.
This does not suffer from the same `isolatedModules` constraint as exports; all modules can be imported in the same statement.

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
you have a need to explain one or more parameters, then add `@param` for _all_ parameters to the JSDoc and add explanations as needed. The
same for `@returns`.

###

Please see other notes in https://github.com/phetsims/ratio-and-proportion/issues/405
and https://github.com/phetsims/phet-info/blob/master/doc/typescript-quick-start.md 
