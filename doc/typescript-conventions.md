## TypeScript Conventions

These are the conventions established for TypeScript use by PhET developers. This is an evolving document in an early
phase. Please bring things up for discussion to add here as you find new patterns.

### Leveraging Type Inference

TypeScript has a powerful type inference system, and we recommend to leverage that type inference in the general case.
For example:

```ts
// Recommended: infers type x:number
const x = 7;

// Not recommended, the type information is redundant.
const x: number = 7;
```

However, if there is a complicated or volatile (api hasn't stabilized) expression on the right hand side, it may be
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

### Visibility Annotations

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