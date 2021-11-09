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

However, if there is a complicated or volatile (api hasn't stabilized) expression on the right hand side, it may be valuable on rare occasions to 
specify the type manually:

```ts
// OK to specify the type manually in complex or volatile cases
const x: number = someComplicatedExpressionOrVolatileStatementThatHasntStabilized();
```

This same principle applies to type parameters.  For instance, TypeScript can infer the parametric type of `new Property`
based on the value of the first parameter.

```ts
// Recommended
new Property(new Laser());

// Not recommended, type information is redundant
new Property<Laser>(new Laser());
```

Again, in complex or volatile cases, at the developer preference, the redundant type annotations may prove useful.