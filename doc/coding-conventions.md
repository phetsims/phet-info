# PhET Coding Conventions

## Table of Contents

* [JavaScript](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#javaScript)
* [Documentation](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#documentation)
* [TypeScript](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#typeScript)
  * [Access Modifiers](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#access-modifiers)
  * [ESLint](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#eslint)
  * [Philosophy](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#philosophy)
  * [Leveraging Type Inference](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#leveraging-type-inference)
  * [Enumerations](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#enumerations)
  * [Parameter Types](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#parameter-types)
  * [Prefer TReadOnlyProperty to DerivedProperty for type annotations](https://github.com/phetsims/phet-info/edit/main/doc/coding-conventions.md#prefer-treadonlyproperty-to-derivedproperty-for-type-annotations)
  * [Options](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#options)
  * [Instance Properties](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#instance-properties)
  * [Class Properties (static)](https://github.com/phetsims/phet-info/edit/main/doc/coding-conventions.md#class-properties-static)
  * [Multiple Exports](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#multiple-exports)
  * [Multiple Imports](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#multiple-imports)
  * [Assertions](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#assertions)
  * [JSDoc and TSDoc](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#jsdoc-and-tsdoc)
  * [Non-null assertion operator](https://github.com/phetsims/phet-info/edit/main/doc/coding-conventions.md#non-null-assertion-operator)
  * [Leverage Excess Property Checking](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#leverage-excess-property-checking)
  * [Read vs Write APIs](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#read-vs-write-apis)
* [Further Reading](https://github.com/phetsims/phet-info/blob/main/doc/coding-conventions.md#further-reading)

## JavaScript
- [ ] Is the code formatted according to PhET conventions?
  See [phet-idea-code-style.xml](https://github.com/phetsims/phet-info/blob/main/ide/idea/phet-idea-codestyle.xml) for
  IntelliJ IDEA code style.

- [ ] Is the code structured in a way that follows [PhET Software Design Patterns](https://github.com/phetsims/phet-info/blob/main/doc/phet-software-design-patterns.md)?

- [ ] Similarly, look through other convention files to check that the code complies with relevant conventions. See the [documentation folder](https://github.com/phetsims/phet-info/blob/main/doc).

- [ ] Names (types, variables, properties, Properties, functions,...) should be sufficiently descriptive and specific,
  and should avoid non-standard abbreviations. For example:

  ```ts
  const numPart = 100;            // incorrect
  const numberOfParticles = 100;  // correct
  const width = 150;              // incorrect
  const beakerWidth = 150;        // correct
  ```

- [ ] For constructors, use parameters for things that don’t have a default. Use options for things that have a default
  value. This improves readability at the call site, especially when the number of parameters is large. It also
  eliminates order dependency that is required by using parameters.

  For example, this constructor uses parameters for everything. At the call site, the semantics of the arguments are
  difficult to determine without consulting the constructor.

  ```ts
  class BallNode extends Node {

    /**
     * @param {Ball} ball - model element
     * @param {Property.<boolean>} visibleProperty - is the ball visible?
     * @param {Color|string} fill - fill color
     * @param {Color|string} stroke - stroke color
     * @param {number} lineWidth - width of the stroke
     */
    constructor( ball, visibleProperty, fill, stroke, lineWidth ){
      // ...
    }
  }

  // Call site
  const ballNode = new BallNode( ball, visibleProperty, 'blue', 'black', 2 );
  ```
  Here’s the same constructor with an appropriate use of options. The call site is easier to read, and the order of
  options is flexible.

  ```ts
  class BallNode extends Node {

    /**
     * @param {Ball} ball - model element
     * @param {Property.<boolean>} visibleProperty - is the ball visible?
     * @param {Object} [options]
     */
    constructor( ball, visibleProperty, options ) {

      options = merge( {
        fill: 'white',  // {Color|string} fill color
        stroke: 'black', // {Color|string} stroke color
        lineWidth: 1 // {number} width of the stroke
      }, options );

      // ...
    }
  }

  // Call site
  const ballNode = new BallNode( ball, visibleProperty, {
    fill: 'blue',
    stroke: 'black',
    lineWidth: 2
  } );
  ```

- [ ] When options are passed through one constructor to another, use the `optionize` pattern. See more [here](https://github.com/phetsims/phet-info/blob/main/doc/phet-software-design-patterns.md#options-typescript).

- [ ] If references are needed to the enclosing object, such as for a closure, `self` should be defined, but it should
  only be used in closures. The `self` variable should not be defined unless it is needed in a closure. Example:

  ```ts
  const self = this;
  someProperty.link( function(){
    self.doSomething();
  } );
  this.doSomethingElse();
  ```

- [ ] Generally, lines should not exceed 120 columns. Break up long statements, expressions, or comments into multiple
  lines to optimize readability. It is OK for require statements or other structured patterns to exceed 120 columns. Use
  your judgment!

- [ ] Functions should be invoked using the dot operator rather than the bracket operator. For more details, please
  see https://github.com/phetsims/gravity-and-orbits/issues/9. For example:
  ```ts
  // avoid
  this[ isFaceSmile ? 'smile' : 'frown' ]();

  // OK
  isFaceSmile ? this.smile() : this.frown();

  // OK
  if ( isFaceSmile ) {
    this.smile();
  }
  else {
    this.frown();
  }
  ```

- [ ] It is not uncommon to use conditional shorthand and short circuiting for invocation. Use parentheses to maximize
  readability.

  ```ts
  ( expression ) && statement;
  ( expression ) ? statement1 : statement2;
  ( foo && bar ) ? fooBar() : fooCat();
  ( foo && bar ) && fooBar();
  ( foo && !(bar && fooBar)) && nowIAmConfused();
  this.fill = ( foo && bar ) ? 'red' : 'blue';
  ```

  If the expression is only one item, the parentheses can be omitted. This is the most common use case.

  ```ts
  assert && assert( happy, 'Why aren\'t you happy?' );
  happy && smile();
  const thoughts = happy ? 'I am happy' : 'I am not happy :(';
  ```

- [ ] Naming for Property values:  All `AXON/Property` instances should be declared with the suffix `Property`. For
  example, if a visible property is added, it should have the name `visibleProperty` instead of simply `visible`. This
  will help to avoid confusion with non-Property definitions. Identify violations by searching for regular expression "=
  new .*Property".

- [ ] Properties should use type-specific subclasses where appropriate (e.g. BooleanProperty, NumberProperty,
  StringProperty) or provide documentation as to why they are not.

- [ ] Are `Validator` validation options (`valueType`, `validValues`, etc...) utilized? These are supported in a number
  of core types like `Emitter` and `Property`. Is their presence or lack thereof properly documented?

- [ ] Files should be named like `CapitalizedCamelCasing.js` when returning a constructor, or `lowerCaseCamelCasing.js`
  when returning a non-constructor function or singleton. When returning a constructor or singleton, the constructor
  name should match the filename. Where singletons are treated like classes with static attributes (like
  SimulaRasaConstants or SimulaRasaColors), uppercase should be used.

- [ ] Assertions should be used appropriately and consistently. Type checking should not just be done in code comments.
  Use `Array.isArray` to type check an array.

- [ ] If you need to namespace an inner class, use `{{namespace}}.register`, and include a comment about why the inner
  class needs to be namespaced. Use the form `'{{outerClassname}}.{{innerClassname}}'` for the key. For example:

  ```ts
  import myNamespace from '...';

  class SlotMachineNode extends Node {
    constructor( ... ) {
      this.leverNode = new LeverNode(...);
      ...
    }
   ...
  }

  myNamespace.register( 'SlotMachineNode', SlotMachineNode );

  class LeverNode extends Node {
   ...
  }

  // It was useful to be able to instantiate this in the console for testing, and we may need to do so in the future.
  myNamespace.register( 'SlotMachineNode.LeverNode', LeverNode );

  return SlotMachineNode;
  ```

- [ ] Putting unused parameters in callbacks is up to developer discretion, as long they are correct wrt to the actual
  callback signature.

  For example, both of these are acceptable:

  ```ts
  Multilink.multilink(
    [ styleProperty, activeProperty, colorProperty ],
    ( style, active, color ) => {
      // some algorithm that uses style and active
    } );
  
  Multilink.multilink(
    [ styleProperty, activeProperty, colorProperty ],
    ( style, active ) => {
      // some algorithm that uses style and active
    } );
  ```

  This is not acceptable, because the 3rd parameter is incorrect.

  ```ts
  Multilink.multilink(
    [ styleProperty, activeProperty, colorProperty ],
    ( style, active, lineWidth ) => {
      // some algorithm that uses style and active
    } );
  ```

- [ ] ES5 getters/setters defined in sims should be used judiciously when a Property exists, only when the benefit of
  conciseness outweighs the potential loss of readability. If ES5 getters/setters exist, try to not mix usage of them
  with Property access.

- [ ] The model and view code should be written such that it makes no assumptions about the animation frame rate this it
  will encounter. The default max dt (delta time) value is defined in `Screen.js`, and smaller values should be used if
  the default is too large. There is no minimum value for dt, which implies that there is no maximum supported frame
  rate. The sim should be able to handle this. For an example of a problem that resulted from assuming that a max rate
  of 60 FPS would be the norm, please see [this GitHub issue](https://github.com/phetsims/states-of-matter/issues/354).

- [ ] The PhET pattern for Enumerations should typically be deeply immutable. Mutable instances most likely shouldn't be
  Enumerations. If you see a mutable enumeration value that isn't a bug, that's interesting and let the developers know!

## Documentation

This section deals with PhET documentation conventions. You do not need to exhaustively check every item in this
section, nor do you necessarily need to check these items one at a time. The goal is to determine whether the code
generally meets PhET standards.

- [ ] All classes, methods and properties are documented.

- [ ] Documentation at the top of source-code files should provide an overview of purpose, responsibilities, and (where
  useful)
  examples of API use. If the file contains a subclass definition, it should indicate what functionality it adds to the
  superclass.

- [ ] The HTML5/CSS3/JavaScript source code must be reasonably well documented. This is difficult to specify precisely,
  but the idea is that someone who is moderately experienced with HTML5/CSS3/JavaScript can quickly understand the
  general function of the source code as well as the overall flow of the code by reading through the comments. For an
  example of the type of documentation that is required, please see the example-sim repository.

- [ ] Differentiate between `Property` and "property" in comments. They are different things. `Property` is a type in
  AXON; property is any value associated with a JavaScript object. Often "field" can be used in exchange for "property"
  which can help with clarity. Search for "property" to identify violations.

- [ ] Classes that mix in traits or mixin should use the `@mixes MyType` annotation.

- [ ] Line comments should generally be preceded by a blank line. For example:

  ```ts
  // Randomly choose an existing crystal to possibly bond to
  const crystal = this.crystals.get( _.random( this.crystals.length - 1 ) );

  // Find a good configuration to have the particles move toward
  const targetConfiguration = this.getTargetConfiguration( crystal );
  ```

- [ ] When documenting conditionals (if/else statements), follow these guidelines:

  1. Comments above the first `if` in a conditional should be about the entire conditional, not just the if block.
  2. Comments should not break up sections of the conditional.
  3. If a comment is needed to describe a single block of the conditional, then add that comment just inside the block (
     no space between the `if`/`else if`/`else` and the comment), with a space below it as to not be confused with a
     comment about logic below.

    ```ts

    // Comment about the reason to split on peppers were pickled.
    if( peterPiperPickedAJarOfPickledPeppers ){
      // if we want to explain what this `if` statement is about

      peterAlsoHasBrine();
    }
    else {

      // documentation about why we have no peppers. This is about the next line of code, and not the "else as a whole block."
      peterHasNoPeppers();
    }
    ```

- [ ] Line comments should have whitespace between the `//` and the first letter of the line comment. See the preceding
  example.


- [ ] Do the `@author` annotations seem correct?


## TypeScript

These are the conventions established for TypeScript use by PhET developers. This is an evolving document in an early
phase. Please bring things up for discussion to add here as you identify new conventions. Conventions enforced by lint
or other tooling are not listed here.

### Access Modifiers

This section deals with PhET conventions for TypeScript access modifiers (`public`, `protected`, `private`), and additional modifiers like `readonly`. Instead of relying on JSDoc annotations to document visibility, you can leverage TypeScript’s built-in features. You may still use TSDoc/JSDoc comments to document details of your API or annotate more specialized visibility scenarios (e.g. “scenery-internal”).

TypeScript provides first-class support for visibility and access through its access modifiers. As part of PhET conventions, here is how you can map those modifiers to the intended usage:

- **`public`**  
  Anything that is part of your *public API*—callers outside the class should be free to access or invoke it.

- **`protected`**  
  Intended *only* for derived (sub) classes. External callers should not access or modify these members.

- **`private`**  
  Members that should not be used outside of the containing class.

Additionally, TypeScript provides several other useful modifiers for refining your API:

- **`readonly`**  
  Indicates that a property is set once (typically in the constructor) and should not be reassigned later.

  ```ts
  class SomeModel {
    public readonly id: string;
    constructor( id: string ) {
      this.id = id;
    }
    // Attempting to reassign id outside of constructor will cause a TypeScript error
  }
  ```

### ESLint

Many of PhET's TypeScript conventions are embodied in TypeScript-specific lint rules. We use the `@typescript-eslint`
plugin to add these rules and augment with our own under the phet plugin. Please see [perennial/eslint](https://github.com/phetsims/perennial/blob/main/js/eslint/)
for details and context about conventions based on lint rules.

### Philosophy

Familiarize yourself with the TypeScript Design
Goals: https://github.com/Microsoft/TypeScript/wiki/TypeScript-Design-Goals. An important one that is often forgotten is
the following:

- "\[the goal is not to\] Apply a sound or "provably correct" type system. Instead, strike a balance between correctness
  and productivity."

TypeScript should work for us and the project, instead of the other way around.

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
  will break the PhET-iO API.
* Please see https://github.com/phetsims/wilder/blob/main/js/wilder/model/WilderEnumerationPatterns.ts for details and
  examples.

### Parameter Types

Parameter types should be as general as possible.

This relates to Vanderkam's Item 29 "Be liberal in what you accept and strict in what you produce.". For example:

```ts
class Animal {name = 'animalName';}

class Dog extends Animal {bark() {}}

function computeHabitat( dog: Dog ) {
  lookup( dog.name );
}
```

Since the `computeHabitat` method doesn't call `bark`, it may be rewritten to accept `computeHabitat( animal: Animal )`.

However, something that has to be PhET-iO instrumented should use `Property` instead of `TProperty` even if the
additional
`Property` methods are not exercised. This will help clients know that it must be a fully-instrumentable axon Property.

### Prefer TReadOnlyProperty to DerivedProperty for type annotations

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

See https://github.com/phetsims/phet-info/blob/main/doc/phet-software-design-patterns.md#options-typescript and
https://github.com/phetsims/wilder/blob/main/js/wilder/model/WilderOptionsPatterns.ts.

**Use `optionize` instead of `merge`.** In the vast majority of cases, `optionize` should be used instead of `merge`.
This provided extra type information on
top of the implementation of merge. While there are still some cases where `merge` is in TypeScript code, it is the
exception and not the rule. Please bring any potential new `merge` usage in TypeScript to the attention of the devs so
that it can be discussed.

### Instance Properties

Instance properties can be initialized either where they are declared, or in the constructor, or as parameter properties
in the constructor parameters. It is up to developer discretion, but please try to be consistent, and adhere to the
spirit of existing code. In addition, please keep potential future PhET-iO instrumentation in mind. Initializing where
declaration occurs may result in refactoring when it comes time to pass Tandems to those objects
(see [example issue](https://github.com/phetsims/keplers-laws/issues/103)).

```ts
// Initialized where declared
class EventCounter {
  public numberOfEvents: number = 0;
  public numberOfEventsProperty: TProperty<number> = new NumberProperty( 0 );

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

The same documentation pattern applies to class properties (statics) and options. Documentation should generally be placed
at the declaration, but explanation for defaults should be described where the default values are assigned.

### Class Properties (static)

One-line static properties will likely be better and clearer when grouped with the instance properties declared at the
top of a class. That said, it is developer preference whether to group them or put them at the bottom of the class
definition:

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
export default Node;
```

Exports can be done at end of the file (as shown above), or at declaration sites like so:

```ts

export type DotPlotNodeOptions = /*...*/;

export default class DotPlotNode extends Node {
  // ...
}
```

### Multiple Imports

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

### Leverage Excess Property Checking

TypeScript is structurally typed, but has a feature called _excess property checking_ that can, in some situations, guard
against typos or any form of incorrect object keys. Excess property checking identifies when an object literal is
compatible with a target type and disallows properties that are not known in that type. For example:

```ts
type Person = {
  age?: number;
  name: string;
};

const p: Person = {
  name: 'John',
  agee: 42 // Hooray, it caught a typo
};

const otherThing = {
  name: 'John',
  agee: 42
};

const p2: Person = otherThing; // Missed opportunity, did not catch my typo. 
```

Leveraging excess property checking can help us catch potential bugs in the form of typos or incorrect object keys at
compile time, enhancing the robustness of our code and reducing the likelihood of runtime errors.

### Read vs Write APIs

When designing an API, you will often encounter the need to make a field read-only in the public API, while
making it writeable in the private/protected API.  This section shows some patterns for accomplishing that 
for Property fields, but the concept can extend to other types of fields.  Other patterns are certainly possible,
and the pattern used is up to the developer.

**Anti-pattern**:  A single reference is provided that is writeable in the public API, with documentation saying
"don't write to this", or an implicit hope that no one will write to it. _Do not do this._

```ts
class MyClass {

  // Do not modify! Only MyClass should write to positionProperty.
  public readonly positionProperty: Property<Vector2>;

  public constructor() {
     this. positionProperty = new Vector2Property( ... );
  }

  public reset(): void {
    this.positionProperty.reset();
  }
}
```

**Pattern 1**: This pattern uses two fields that are references to the same Property instance. The `public` reference is read-only for getting the value.
The `private` reference is for setting and resetting the instance internal to the class. Use `protected` here if it is appropriate for subclasses to 
modify the Property. The convention is for the private/protected field name to begin with an underscore (`_positionProperty`).

```ts
class MyClass {

  public readonly positionProperty: TReadOnlyProperty<Vector2>;
  private readonly _positionProperty: Property<Vector2>;

  public constructor() {
     this. _positionProperty = new Vector2Property( ... );
     this. positionProperty = this.positionProperty;
  }

  public reset(): void {
    this._positionProperty.reset();
  }
}
```

**Pattern 2**: Provide public read-only access to the Property value (but not the Property) via an ES5 getter.

```ts
class MyClass {

  private readonly positionProperty: Property<Vector2>;

  public constructor() {
     this. positionProperty = new Vector2Property( ... );
  }

  public reset(): void {
    this.positionProperty.reset();
  }

  get position(): Vector2 {
    return this.positionProperty.value;
  }
}
```

**Pattern 3**: A variation of Pattern 2, this pattern provides public read-only access to the Property (not just the Property value) via an ES5 getter.
Note that the field name must begin with an underscore (`_positionProperty`) so that it does not conflict with the ES5 getter name.

```ts
class MyClass {
  private readonly _positionProperty: Property<Vector2>;

  public constructor() {
    this._positionProperty = new Vector2Property(...);
  }

  public get positionProperty(): TReadOnlyProperty<Vector2> {
    return this._positionProperty;
  }

  public reset(): void {
    this._positionProperty.reset();
  }
}
```

## Further Reading

* [PhET Software Design Patterns](https://github.com/phetsims/phet-info/blob/main/doc/phet-software-design-patterns.md)
* Item 11 "Distinguish Excess Property Checking from Type Checking" in [Effective Typescript](https://effectivetypescript.com) by Dan Vanderkam.
* Notes in https://github.com/phetsims/ratio-and-proportion/issues/405
* Notes in https://github.com/phetsims/phet-info/blob/main/doc/typescript-quick-start.md 
