## Coding Conventions

- [ ] Is the code formatted according to PhET conventions?
  See [phet-idea-code-style.xml](https://github.com/phetsims/phet-info/blob/master/ide/idea/phet-idea-codestyle.xml) for
  IntelliJ IDEA code style.

- [ ] Names (types, variables, properties, Properties, functions,...) should be sufficiently descriptive and specific,
  and should avoid non-standard abbreviations. For example:

  ```js
  const numPart = 100;            // incorrect
  const numberOfParticles = 100;  // correct
  const width = 150;              // incorrect
  const beakerWidth = 150;        // correct
  ```

- [ ] Verify
  that [Best Practices for Modules](https://github.com/phetsims/phet-info/blob/master/doc/best-practices-for-modules.md)
  are followed.

- [ ] For constructors, use parameters for things that don’t have a default. Use options for things that have a default
  value. This improves readability at the call site, especially when the number of parameters is large. It also
  eliminates order dependency that is required by using parameters.

  For example, this constructor uses parameters for everything. At the call site, the semantics of the arguments are
  difficult to determine without consulting the constructor.

  ```js
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

  ```js
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

- [ ] When options are passed through one constructor to another, a "nested options" pattern should be used. This helps
  to avoid duplicating option names and/or accidentally overwriting options for different components that use the same
  option names. Make sure to use PHET_CORE/merge instead of `_.extend` or `_.merge`. `merge` will automatically recurse
  to keys named `*Options` and extend those as well.

  Example:
  ```js
  class ParticleBoxNode extends Node {

    /**
     * @param {ParticleBox} particleBox - model element
     * @param {Property.<boolean>} visibleProperty - are the box and its contents visible?
     * @param {Object} [options]
     */
    constructor( particleBox, visibleProperty, options ) {

      options = merge( {
        fill: 'white',  // {Color|string} fill color
        stroke: 'black', // {Color|string} stroke color
        lineWidth: 1, // {number} width of the stroke
        particleNodeOptions: {
          fill: 'red',
          stroke: 'gray',
          lineWidth: 0.5
        },
      }, options );

      // add particle
      this.addChild( new ParticleNode( particleBox.particle, options.particleNodeOptions ) );
      ...
    }
  }
  ```

  A possible exception to this guideline is when the constructor API is improved by hiding the implementation details,
  i.e. not revealing that a sub-component exists. In that case, it may make sense to use new top-level options. This is
  left to developer and reviewer discretion.

  For more information on the history and thought process around the "nested options" pattern, please
  see https://github.com/phetsims/tasks/issues/730.

- [ ] If references are needed to the enclosing object, such as for a closure, `self` should be defined, but it should
  only be used in closures. The `self` variable should not be defined unless it is needed in a closure. Example:

  ```js
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
  ```js
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

  ```js
  ( expression ) && statement;
  ( expression ) ? statement1 : statement2;
  ( foo && bar ) ? fooBar() : fooCat();
  ( foo && bar ) && fooBar();
  ( foo && !(bar && fooBar)) && nowIAmConfused();
  this.fill = ( foo && bar ) ? 'red' : 'blue';
  ```

  If the expression is only one item, the parentheses can be omitted. This is the most common use case.

  ```js
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

  ```js
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

  ```js
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

  ```js
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

### Documentation

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

  ```js
  // Randomly choose an existing crystal to possibly bond to
  const crystal = this.crystals.get( _.random( this.crystals.length - 1 ) );

  // Find a good configuration to have the particles move toward
  const targetConfiguration = this.getTargetConfiguration( crystal );
  ```

- [ ] When documenting conditionals (if/else statements), follow these guidelines:

  1. Comments above the first `if` in a conditional should be about the entire conditional, not just the if block.
  2. Comments should not break up sections of the conditional.
  3. If a comment is needed to describe a single block of the conditional, then add that comment just inside the
     block (no space between the `if`/`else if`/`else` and the comment), with a space below it as to not be confused
     with a comment about logic below.

    ```js

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

- [ ] Constructor and function documentation. Parameter types and names should be clearly specified for each constructor
  and function using `@param` annotations. The description for each parameter should follow a hyphen. Primitive types
  should use lower case. For example:

  ```js
  /**
   * The PhetDeveloper is responsible for creating code for simulations and documenting their code thoroughly.
   */
  class PhetDeveloper {

    /**
     * @param {string} name - full name
     * @param {number} age - age, in years
     * @param {boolean} isEmployee - whether this developer is an employee of CU
     * @param {function} callback - called immediate after coffee is consumed
     * @param {Property.<number>} hoursProperty - cumulative hours worked
     * @param {string[]} friendNames - names of friends
     * @param {Object} [options]
     */
    constructor( name, age, isEmployee, callback, hoursProperty, friendNames, options ) {
      ...
    }

    ...
  }
  ```

- [ ] For most functions, the same form as above should be used, with a `@returns` annotation which identifies the
  return type and the meaning of the returned value. Functions should also document any side effects. For extremely
  simple functions that are just a few lines of simple code, an abbreviated line-comment can be used, for
  example: `// Computes {Number} distance based on {Foo} foo.`


- [ ] Abstract methods should be annotated with `@abstract` and should typically throw an Error. For example:

  ```js
  /**
   * Updates this node.
   * @abstract
   * @protected
   */
  update()
  {
    throw new Error( 'update must be implemented by subclass' );
  }
  ```

#### Type Expressions

This section deals with PhET conventions for type expressions. You do not need to exhaustively check every item in this
section, nor do you necessarily need to check these items one at a time. The goal is to determine whether the code
generally meets PhET standards.

- [ ] Type expressions should conform approximately
  to [Google Closure Compiler](https://github.com/google/closure-compiler/wiki/Annotating-JavaScript-for-the-Closure-Compiler)
  syntax. PhET stretches the syntax in many cases (beyond the scope of this document to describe).

- [ ] Prefer the most basic/restrictive type expression when defining APIs. For example, if a client only needs to know
  that a parameter is `{Node}`, don’t describe the parameter as `{Rectangle}`.

- [ ] All method parameters should have type expressions. For example `@param {number} width`.

- [ ] In sim-specific code, options and fields should have type expressions when their type is not obvious from the
  context. “Obvious” typically means that the value type is clearly shown in the righthand-side of the definition.
  E.g. `const width = 42` clear shows that `width` is `{number}`. E.g. `const checkbox = new Checkbox(…)` clearly shows
  that `checkbox` is `{Checkbox}`. If the type is obvious from the context, the developer may still provide a type
  expression at his/her discretion. Examples:

  ```js
  // @public {GameState} the current state of the game
  this.gameState = this.computeGameState();

  // @public (read-only) the width of the container
  this.containerWidth = 150;

  // @private the checkbox used to show particles
  this.particlesVisibleCheckbox = new Checkbox(...);
  ```

- [ ] In common code repositories all options and fields should have type expressions, regardless of their visibility,
  and regardless whether their type is obvious from the context. If the same examples from above appeared in common
  code:

  ```js
  // @public {GameState} the current state of the game
  this.gameState = this.computeGameState();

  // @public (read-only) {number} the width of the container
  this.containerWidth = 150;

  // @private {Checkbox} the checkbox used to show particles
  this.particlesVisibleCheckbox = new Checkbox(...);
  ```

- [ ] Type expressions for `EnumerationDeprecated` values should be annotated as instances of that
  EnumerationDeprecated, see examples in https://github.com/phetsims/phet-core/blob/master/js/EnumerationDeprecated.js
  for more.
  ```js
  /**
   * @param {LeftOrRight} - whichHand
   */
   function getHand( whichHand ){
     if( whichHand === LeftOrRight.LEFT ){
       return new LeftHand();
     }
     else if( whichHand === LeftOrRight.RIGHT ){
       return new RightHand();
     }
    }
  ```

- [ ] Type expressions for functions have a variety of possibilities, increasing in complexity depending on the case. In
  general note that `{function}` is not enough information. Here are some better options:

  1. The most basic option it to use Google Closure Type syntax, for more info
     see https://github.com/google/closure-compiler/wiki/Types-in-the-Closure-Type-System. This specifies the
     param/return types, but nothing more. Here are some examples:

  * `@param {function()} noParamsAndNoReturnValue`
  * `@param {function(number)} giveMeNumberAndReturnNothing`
  * `@param {function(number, number):Vector2} getVector2`
  * `@param {function(new:Node)} createNode - a function that takes the Node constructor`

  2. When needing to be a bit more specific, add a name to parameters of the function. Sometimes this is all that is
     needed for clarity on what the param does:

  * `@param {function(model:MyModel, length:number, name:string): Node} getLengthNode`
  * `@param {function(aSelfExplanatoryNameForAString:string): Node} getStringNode`

  3. If (2) isn't enough, use English to explain the parameters and return values. This is easy because they are
     named, and can be easily mentioned:

  * `@param {function(model:MyModel, length:number, name:string): Node} getLengthNode - returns the length Node that you have always wanted, name is the name of the source of your aspirations, length is a special number according to the following 24 criteria. . .`

  4. If needing more complexity, or using jsdoc rendering tools (like PhET-iO documentation does), you must use a
     JSDoc compatible format, not (2) or (3), and you may need to use the more complicated solution. See JSDoc docs
     for more info. Here is an example of a named callback:
      ```js
      /**
       * @name mySpecialCallback
       * Converts a string to a number
       * @param {string}
       * @returns {number}
       */
      /**
       * @param {mySpecialCallback} callback
      */
      x = function( callback) { callback( 'still chocolate' ) };
      ```

- [ ] Type expressions for anonymous Objects have a variety of possibilities, increasing in complexity depending on the
  case.
  1. When the documentation is close by, then {Object} is still acceptable. This mainly applies to options and similar
     patterns:

  * `@param {Object} [options] // this is great because of the extend call 5 lines down`

  2. When using an `Object` with specific properties, name them and their types like so:

  * `@param {name:string, address:{street:string}, returnNode:function(number):Node, [shoeSize:number]} personalData // note that shoeSize is optional here`

  3. When you need a bit more explanation, keep the same type expression as (2), but feel free to outline specifics in
     English after the param name.
      ```
      @ param {name:string, address:{street:string}, returnNode:function(number):Node, [shoeSize:number]} personalData - use english after to explain pieces of this
          (if needed, outline properties on their own lines)
          name is something
          address is something else
          returnNode does this thing
      ```
  4. Not all objects have named keys like (2) and (3). Here is how to document dictionary-like `Object`s, where each
     key is some type, and the value is another type. For key value pairs use this:

  * `{Object.<string, number>}` Where keys are strings, and values are numbers.
  * `{Object.<phetioID:string, count:number>}` - naming each of these can help identify them too. Feel free to explain
    in English after the type expression if needed.

  5. If things are too complicated for the above cases, use a `*Def.js` file (especially is used in more than one
     file), or a `@typedef` declaration right above the jsdoc that uses the typedef.

- [ ] Look for cases where the use of type expressions involving Property subclasses are incorrect. Because of the
  structure of the `Property` class hierarchy, specifying type-specific Properties (`{BooleanProperty}`
  , `{NumberProperty}`,...) may be incorrect, because it precludes values of type `{DerivedProperty}`
  and `{DynamicProperty}`. Similarly, use of `{DerivedProperty}` and `{DynamicProperty}` precludes values of (
  e.g.) `{BooleanProperty}`. Especially in common code, using `{Property.<TYPE>}` is typically correct, unless some
  specific feature of the `Property` subclass is required. For example, `{Property.<boolean>}` instead
  of `{BooleanProperty}`.

#### Visibility Annotations

This section deals with PhET conventions for visibility annotations. You do not need to exhaustively check every item in
this section, nor do you necessarily need to check these items one at a time. The goal is to determine whether the code
generally meets PhET standards.

Because JavaScript lacks visibility modifiers (public, protected, private), PhET uses JSdoc visibility annotations to
document the intent of the programmer, and define the public API. Visibility annotations are required for anything that
JavaScript makes public. Information about these annotations can be found here. (Note that other documentation systems
like the Google Closure Compiler use slightly different syntax in some cases. Where there are differences, JSDoc is
authoritative. For example, use `Array.<Object>` or `Object[]` instead of `Array<Object>`). PhET guidelines for
visibility annotations are as follows:

- [ ] Use `@public` for anything that is intended to be part of the public API.
- [ ] Use `@protected` for anything that is intended for use by subtypes.
- [ ] Use `@private` for anything that is NOT intended to be part of the public or protected API.
- [ ] Put qualifiers in parenthesis after the annotation, for example:
  * To qualify that something is read-only, use `@public (read-only)`. This indicates that the given Property (AND its
    value) should not be changed by outside code (e.g. a Property should not have its value changed)
  * To qualify that something is public to a specific repository, use (for example) `@public (scenery-internal)`
  * For something made public solely for a11y, use `@public (a11y)`
  * For something made public solely for phet-io, use `@public (phet-io)`
  * Separate multiple qualifiers with commas. For example: `@public (scenery-internal, read-only)`
- [ ] For JSDoc-style comments, the annotation should appear in context like this:

  ```js
  /**
   * Creates the icon for the "Energy" screen, a cartoonish bar graph.
   * @returns {Node}
   * @public
   */
  ```

- [ ] For Line comments, the annotation can appear like this:

  ```js
  // @public {function(listener:function)} - Adds a listener
  addListener: function( listener ) { /*...*/ }
  ```

- [ ] Verify that every JavaScript property and function has a visibility annotation. Here are some helpful regular
  expressions to search for these declarations as PhET uses them.
  * Regex for property assignment like `x.y = something`: `[\w]+\.[\w]+\s=`
  * Regex for function declarations: `[\w]+: function\(`

- [ ] For private fields, a preceding underscore should generally *not* be used in the variable name. For example,
  for a private variable that represents the background, the name ```background``` is preferred over ```_background```.
  An exception is when trying to avoid a collision with and ES5 getter/setter.
