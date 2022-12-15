## TypeScript Conventions

These are the conventions established for TypeScript use by PhET developers. This is an evolving document in an early
phase. Please bring things up for discussion to add here as you identify new conventions. Conventions enforced by lint
or other tooling are not listed here.

### ESLint

Many of PhET's TypeScript conventions are embodied in TypeScript-specific lint rules. We use the `@typescript-eslint`
plugin to add these rules. Please see [.eslintrc](https://github.com/phetsims/chipper/blob/master/eslint/.eslintrc.js)
for details and context about conventions based on lint rules.

### Leveraging Type Inference

From _Effective TypeScript_ (Dan Vanderkam), page 87, Item 19, "Avoid Cluttering Your Code with Inferable Types":

* Avoid writing type annotations when TypeScript can infer the same type.
* Ideally your code has type annotations in function/method signatures but not on local variables in their bodies.
* Consider using explicit annotations for object literals and function return types even when they can be inferred. This
  will help prevent implementation errors from surfacing in user code.

It is PhET convention to provide return types when declaring methods and functions. This includes explicitly specifying
`void` for everything that is a method and/or part of a public API.
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

This same principle applies to generic type parameters. For instance, TypeScript can infer the parametric type
of `new Property`
based on the value of the first parameter. For example:

```ts
// Recommended
new Property( new Laser() );

// Not recommended, type information is redundant
new Property<Laser>( new Laser() );
```

Again, in complex or volatile cases, at the developer preference, the redundant type annotations may prove useful.

### Enumerations

* String literal unions are idiomatic in TypeScript.
* You can also use the string[] `as const` pattern for accessing string union literals and values at runtime.  
  This works well with `StringUnionProperty`.
* `EnumerationValue` adds rich methods on the instances. Use `EnumerationProperty` for this.
* Careful!  If you change from string literal union to `EnumerationValue`, the casing convention is different and you
  will
  break the PhET-iO API.
* Please see https://github.com/phetsims/wilder/blob/master/js/wilder/model/WilderEnumerationPatterns.ts for details and
  examples.

### Parameters should be as general as possible

This relates to Vanderkam's Item 29 "Be liberal in what you accept and strict in what you produce.". For example:

```ts
class Animal{ name='animalName';}
class Dog extends Animal{ bark(){} }
function computeHabitat( dog:Dog ){
  lookup( dog.name );
}
```

Since the `computeHabitat` method doesn't call `bark`, it may be rewritten to accept `computeHabitat( animal: Animal )`.

However, something that has to be PhET-iO instrumented should use `Property` instead of `TProperty` even if the
additional
`Property` methods are not exercised. This will help clients know that it must be a fully-instrumentable axon Property.

### Prefer TReadOnlyProperty to DerivedProperty for type annotations.

Prefer `TReadOnlyProperty` to `DerivedProperty` for type declarations,
see https://github.com/phetsims/build-a-nucleus/issues/13

```ts
class HalfLifeInformationNode extends Node {

  constructor( halfLifeNumberProperty: DerivedProperty<number,
                 [ protonCount: number, neutronCount: number, doesNuclideExist: boolean, isStable: boolean ]>,
               isStableBooleanProperty: DerivedProperty<boolean, [ protonCount: number, neutronCount: number ]> ) {
    super();
```

should be simplified as:

```ts
class HalfLifeInformationNode extends Node {

  constructor( halfLifeNumberProperty: TReadOnlyProperty<number>,
               isStableBooleanProperty: TReadOnlyProperty<boolean> ) {
    super();
```

### Options

See https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#options-typescript and
https://github.com/phetsims/wilder/blob/master/js/wilder/model/WilderOptionsPatterns.ts.

#### Use `optionize` instead of `merge`

In the vast majority of cases, `optionize` should be used instead of `merge`. This provided extra type information on
top
of the implementation of merge. While there are still some cases where `merge` is in TypeScript code, it is the
exception
and not the rule. Please bring any potential new `merge` usage in TypeScript to the attention of the devs so that it can
be discussed.

### Initialization of instance properties

Instance properties can be initialized either where they are declared, or in the constructor, or as parameter properties
in the constructor parameters. It is up to developer discretion, but please try to be consistent, and adhere to the
spirit of existing code.

```ts
// Initialized where declared
class EventCounter {
  public numberOfEvents: number = 0;

  // ...
}

// Initialized in constructor
class EventCounter {
  public numberOfEvents: number;

  constructor( ... ) {
    super( ... );
    this.numberOfEvents = 0;
    // ...
  }
}

// Initialized as parameter property in constructor
class EventCounter {

  constructor( public numberOfEvents = 0 ) {
    super( ... );
  }
}
```

#### Statics (class properties)

One-line static properties will likely be better and clearer when grouped with the instance properties declared
at the top of a class. That said, it is developer preference whether to group them or put them at the bottom of the
class definition:

```ts
class Person {

  readonly name: string;

  // here is a bit better
  static QUALITIES: [ 'height', 'age' ];

  constructor( name: string ) {
    this.name = name;
  }
  
  sayName() {
    console.log( name );
  }
  
  // or here because it is long
  static QUALITIES: [ 
    'height', 
    'age' 
  ];
}
```

#### Documentation

Documentation for instance properties should be placed with the declaration, not the instantiation. For example:

```ts
class Person {

  // First and last name, separated by a whitespace
  readonly name: string;

  constructor( name: string ) {
    this.name = name;
  }
}
```

If implementation details are needed about the instantiation value, then those should be included at the instantiation
point.

```ts
class Person {

  // First and last name, separated by a whitespace
  name: string;

  constructor() {
    
    // All new people get assigned a random name. A specific name can be assigned later if desired.
    this.name = Person.getRandomName();
  }

  // ...
}
```

The same documentation pattern applies to options. Documentation should generally be placed at the declaration, but
explanation for defaults should be described where the default values are assigned.

### Multiple Exports

PhET uses babel to do transpilation, and it only operates on a single file at a time. This means that it can’t apply
code transforms that depend on understanding the full type system, and we are restricted to
specifying [isolatedModules](https://www.typescriptlang.org/tsconfig#isolatedModules) in tsconfig. This in turn requires
that types must be exported separately from other modules. For example:

```ts
type NodeOptions = /*...*/;
type MyEnum = /*...*/;

class Node { /*...*/}

export { NodeOptions, MyEnum };
export { Node as default };
```

Exports can be done at end of the file (as shown above), or at declaration sites like so:

```ts

export type DotPlotNodeOptions = /*...*/;

export default class DotPlotNode extends Node {
  // ...
}
```

### Multiple Imports in One Expression

Multiple imports from the same file should be combined into one statement. This helps clarify that they are related.
This does not suffer from the same `isolatedModules` constraint as exports; all modules can be imported in the same
statement.

```ts
// Preferred
import BendingLightScreenView, { BendingLightScreenViewOptions } from '../../common/view/BendingLightScreenView.js';

// Not preferred
import BendingLightScreenView from '../../common/view/BendingLightScreenView.js';
import { BendingLightScreenViewOptions } from '../../common/view/BendingLightScreenView.js';
```

If this exceeds the line limit and the WebStorm formatter wants to format it on multiple lines, please use
`// eslint-disable-line single-line-import`

### Assertions

In general, assertions should be used to check run-time conditions that can't be validated by the type checker.

When converting from JS to TS, `assert` statements that checked types can and should be removed.

### JSDoc and TSDoc

It is recommended that you do not duplicate parameter and return type information in JSDoc and in Typescript types. If
you have a need to explain one or more parameters, then add `@param` for _all_ parameters to the JSDoc and add
explanations as needed. The same for `@returns`.

### Non-null assertion operator

The non-null assertion operator `!` indicates to the TypeScript compiler that a value can be treated as non-null and
non-undefined. This operator should be used judiciously. It can sometimes be preferable to write code that doesn't
require it at all (for instance, by using values that can never be `null` or `undefined`). In cases where the non-null
assertion operator is appropriate:

* Consider adding documentation that explains why the value is not expected to be null or undefined at that point.
* Add an assertion guard where necessary. Cases like `if ( this.someNumber! < 50 ) {` require an assertion guard,
  since `null < 50` evaluates to true. Cases like `something!.method` do not require a guard, since you already get a
  helpful runtime error.
* Consider factoring out a variable rather than repeating the non-null assertion operator several times on the same
  variable.

---

Please see other notes in https://github.com/phetsims/ratio-and-proportion/issues/405
and https://github.com/phetsims/phet-info/blob/master/doc/typescript-quick-start.md 
