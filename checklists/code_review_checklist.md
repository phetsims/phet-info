*NOTE! Prior to doing a code review, copy this checklist to a GitHub issue for the repository being reviewed. Delete the Table of Contents section, since the links will be incorrect.*

*Please mark failed items with* ❌

PhET code-review checklist
=============

## Table of Contents
* [Build and Run Check](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#build-and-run-checks)
* [Memory Leaks](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#memory-leaks)
* [Performance](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#performance)
* [Usability](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#usability)
* [Internationalization](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#internationalization)
* [Repository Structure](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#repository-structure)
* [Coding Conventions](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#coding-conventions)
  * [Type Expressions](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#type-expressions)
  * [Visibility Annotations](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#visibility-annotations)
* [Math Libraries](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#math-libraries)
* [IE11](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#ie11)
* [Organization, Readability, and Maintainability](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#organization-readability-and-maintainability)
* [PhET-iO](https://github.com/phetsims/phet-info/blob/master/checklists/code_review_checklist.md#phet-io)

## **Build and Run Checks**

- [ ] Does the sim build without warnings or errors?
- [ ] Does the html file size seem reasonable, compared to other similar sims?
- [ ] Does the sim start up? (requirejs and built versions)
- [ ] Does the sim experience any assertion failures? (run with query parameter `ea`)
- [ ] Does the sim pass a scenery fuzz test? (run with query parameters `fuzz&ea`)
- [ ] Does linting with "sim_es6_eslintrc_review.js" reveal any problems that should be fixed? (change eslintConfig in package.json and run `grunt lint`)

## **Memory Leaks**

- [ ] Does a heap comparison using Chrome Developer Tools indicate a memory leak? (Describing this process is beyond the scope of this document.) Test on a version built using `grunt --minify.mangle=false`. There should be a GitHub issue showing the results of testing done by the primary developer.
- [ ] For each common-code component (sun, scenery-phet, vegas, …) that opaquely registers observers or listeners, is
there a call to that component’s `dispose` function, or is it obvious why it isn't necessary, or is there documentation
about why `dispose` isn't called?  An example of why no call to `dispose` is needed is if the component is used in
a screen view that would never be removed from the scene graph.
- [ ] Are there leaks due to registering observers or listeners? The following guidelines should be followed unless
there it is obviously no need to unlink, or documentation (in-line or in the implementation nodes)added about why
following them is not necessary.  Examples of when an unlink is not needed is if the property never 
	- [ ] AXON: `Property.link` is accompanied by `Property.unlink`.
	- [ ] AXON: Creation of `DerivedProperty` is accompanied by `dispose`.
	- [ ] AXON: Creation of `Multilink` is accompanied by `dispose`.
	- [ ] AXON: `Events.on` is accompanied by `Events.off`.
	- [ ] AXON: `Emitter.addListener` is accompanied by `Emitter.removeListener`.
	- [ ] SCENERY: `Node.on` is accompanied by `Node.off`
	- [ ] TANDEM: PhET-iO instrumented `PhetioObject` instances should be disposed.
- [ ] Do all types that require a `dispose` function have one? This should expose a public `dispose` function that calls `this.disposeMyType()`, where `disposeMyType` is a private function declared in the constructor.  `MyType` should exactly match the filename.
- [ ] PhET-iO instantiates different objects and wires up listeners that are not present in the PhET-branded simulation.  It needs to be tested separately for memory leaks.  To help isolate the nature of the memory leak, this test should be run separately from the PhET brand memory leak test.  Test with the "console" and "studio" wrappers (easily accessed from phetmarks)

## **Performance**

- [ ] Does the sim perform as desired across the range of supported platforms? (eg, not too slow on slow platforms, not too fast on fast platforms)
- [ ] If the sim uses WebGL, does it have a fallback? Does the fallback perform reasonably well? (run with query parameter `webgl=false`)

## **Usability**

- [ ] Are UI components sufficiently responsive? (especially continuous UI components, such as sliders)
- [ ] Are pointer areas optimized, especially for touch? (run with query parameter `showPointerAreas`)
- [ ] Do pointer areas overlap? (run with query parameter `showPointerAreas`) Some overlap may be OK depending on the z-ordering (if the frontmost object is supposed to occlude touch/mouse areas)

## **Internationalization**
- [ ] Are there any strings that are not being internationalized? (run with query parameter `stringTest=x`, you should see nothing but 'x' strings)
- [ ] Does the sim layout gracefully handle internationalized strings that are twice as long as the English strings? (run with query parameter `stringTest=double`)
- [ ] Does the sim layout gracefully handle internationalized strings that are exceptionally long? (run with query parameter `stringTest=long`)
- [ ] Does the sim layout gracefully handle internationalized strings that are shorter than the English strings? (run with query parameter `stringTest=X`)
- [ ] Does the sim stay on the sim page (doesn't redirect to an external page) when running with the query parameter 
`stringTest=xss`? This test passes if sim does not redirect, OK if sim crashes or fails to fully start. Only test on one 
desktop platform.  For PhET-iO sims, additionally test `?stringTest=xss` in Studio to make sure i18n strings didn't leak 
to phetioDocumentation, see https://github.com/phetsims/phet-io/issues/1377
- [ ] Use named placeholders (e.g. `"{{value}} {{units}}"`) instead of numbered placeholders (e.g. `"{0} {1}"`).
- [ ] Make sure the string keys are all perfect - they are difficult to change after 1.0.0 is published. Guidelines for string keys are:
  
  (1) Strings keys should generally match their values. E.g.:
  
  ```js
  "helloWorld": {
    value: "Hello World!"
  },
  "quadraticTerms": {
    value: "Quadratic Terms"
  }
  ```
  
  (2) If a string key would be exceptionally long, use a key name that is an abbreviated form of the string value, or that captures the purpose/essence of the value. E.g.:
  
  ```js
  // key is abbreviated
  "iWentToTheStore": {
    value: "I went to the store to get milk, eggs, butter, and sugar."
  },
  
  // key is based on purpose
  "describeTheScreen": {
    value: "The Play Area is a small room. The Control Panel has buttons, a checkbox, and radio buttons to change conditions in the room."
  }
  ```
  (3) If string key names would collide, use your judgment to disambiguate. E.g.:
  
  ```js
  "simplifyTitle": {
     value: "Simplify!"
  },
  "simplifyCheckbox": {
     value: "simplify"
  }
  ```
  
  (4) String keys for screen names should have the general form `"screen.{{screenName}}"`. E.g.:
  
  ```js
    "screen.explore": {
      "value": "Explore"
    },
  ```
  
  (5) String patterns that contain placeholders (e.g. `"My name is {{first}} {{last}}"`) should use keys that are unlikely to conflict with strings that might be needed in the future.  For example, for `"{{price}}"` consider using key `"pricePattern"` instead of `"price"`, if you think there might be a future need for a `"price"` string.

## **Repository Structure**

- [ ] Are all required files and directories present?
For a sim repository named “my-repo”, the general structure should look like this (where assets/, sound/ or images/ may be omitted if the sim doesn’t have those types of assets).

  ```js
     my-repo/
        assets/
           license.json
        doc/
           images/
                 *see annotation
           model.md
           implementation-notes.md
        images/
           license.json
        js/
           (see section below)
        sound/
        dependencies.json
        .gitignore
        my-repo_en.html
        my-repo-strings_en.json
        Gruntfile.js
        LICENSE
        package.json
        README.md
  ```
  *Any images used in model.md or implementation-notes.md should be added here. Images specific to aiding with documentation do not need their own license.

- [ ] Is the js/ directory properly structured?
  All JavaScript source should be in the js/ directory. There should be a subdirectory for each screen (this also applies for single-screen sims, where the subdirectory matches the repo name).  For a multi-screen sim, code shared by 2 or more screens should be in a js/common/ subdirectory. Model and view code should be in model/ and view/ subdirectories for each screen and common/.  For example, for a sim with screens “Introduction” and “Lab”, the general directory structure should look like this:
  
  ```js
     my-repo/
        js/
           common/
              model/
              view/
           introduction/
              model/
              view/
           lab/
              model/
              view/
           my-repo-config.js
           my-repo-main.js
           myRepo.js
   ```

- [ ] Do filenames use an appropriate prefix? Some filenames may be prefixed with the repository name, e.g. `MolarityConstants.js` in molarity.  If the repository name is long, the developer may choose to abbreviate the repository name, e.g. `EEConstants.js` in expression-exchange. If the abbreviation is already used by another respository, then the full name must be used. For example, if the "EE" abbreviation is already used by expression-exchange, then it should not be used in equality-explorer.  Whichever convention is used, it should be used consistently within a repository - don't mix abbreviations and full names.
- [ ] Is there a file in assets/ for every resource file in sound/ and images/? Note that there is *not necessarily* a 1:1 correspondence between asset and resource files; for example, several related images may be in the same .ai file. Check license.json for possible documentation of why some reesources might not have a corresponding asset file.
- [ ] Was the README.md generated by `grunt published-README` or `grunt unpublished-README`?
- [ ] Does package.json refer to any dependencies that are not used by the sim?
- [ ] Is the sim's -config.js up-to-date (generated by `grunt generate-config`)
- [ ] Is the LICENSE file correct? (Generally GPL v3 for sims and MIT for common code, see [this thread](https://github.com/phetsims/tasks/issues/875#issuecomment-312168646) for additional information).
- [ ] Does .gitignore match the one in simula-rasa?
- [ ] Does a GitHub issue exist for tracking credits, to ensure that they are correct before publication?
- [ ] In GitHub, verify that all non-release branches have an associated issue that describes their purpose.
- [ ] Are there any GitHub branches that are no longer needed and should be deleted?
- [ ] Does `model.md` adequately describe the model, in terms appropriate for teachers?
- [ ] Does `implementation-notes.md` adequately describe the implementation, with an overview that will be useful to future maintainers?
- [ ] Are sim-specific query parameters (if any) identified and documented in one .js file in js/common/ or js/ (if there is no common/)? The .js file should be named `{{REPO}}QueryParameters.js`, for example ArithmeticQueryParameters.js for the aritmetic repository.

## **Coding Conventions**

- [ ] Is the code formatted according to PhET conventions? See [phet-idea-code-style.xml](https://github.com/phetsims/phet-info/blob/master/ide/idea/phet-idea-codestyle.xml) for IntelliJ IDEA code style.
- [ ] Are copyright headers present and up to date? Run `grunt update-copyright-dates`.
- [ ] Names (types, variables, properties, functions,...) should be sufficiently descriptive and specific, and should avoid non-standard abbreviations. For example:
  
  ```js
  const numPart = 100;            // incorrect
  const numberOfParticles = 100;  // correct
  
  const width = 150;              // incorrect
  const beakerWidth = 150;        // correct
  ```

- [ ] Require statements should be organized into blocks, with the code modules first, followed by plugins (strings, images, sound, ifphetio - any order ok for plugins).  For modules, the variable name should match the file name. Example below.
  
  ```js
  // modules
  const inherit = require( 'PHET_CORE/inherit' );
  const Line = require( 'SCENERY/nodes/Line' );
  const Rectangle = require( 'SCENERY/nodes/Rectangle' );
  
  // strings
  const kineticString = require( 'string!ENERGY/energy.kinetic' );
  const potentialString = require( 'string!ENERGY/energy.potential' );
  const thermalString = require( 'string!ENERGY/energy.thermal' );
  
  // images
  const energyImage = require( 'image!ENERGY/energy.png' );
  
  // sound
  const kineticAudio = require( 'sound!ENERGY/energy' );
  ```

- [ ] Do the `@author` annotations seem correct?

- [ ] Are all constructors marked with `@constructor`?  That will make them easier to search and review.  This is not necessary for ES6 constructors.

- [ ] For constructors, use parameters for things that don’t have a default. Use options for things that have a default value.  This improves readability at the call site, especially when the number of parameters is large.  It also eliminates order dependency that is required by using parameters.

  For example, this constructor uses parameters for everything. At the call site, the semantics of the arguments are difficult to determine without consulting the constructor.
  
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
  Here’s the same constructor with an appropriate use of options. The call site is easier  to read, and the order of options is flexible.
  
  ```js
  class BallNode extends Node {
  
    /**
     * @param {Ball} ball - model element
     * @param {Property.<boolean>} visibleProperty - is the ball visible?
     * @param {Object} [options]
     */
    constructor( ball, visibleProperty, options ) {
  
      options = _.extend( {
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

- [ ] When options are passed through one constructor to another, a "nested options" pattern should be used.  This helps to avoid duplicating option names and/or accidentally overwriting options for different components that use the same option names.

  Example:
  ```js
  class ParticleBoxNode extends Node {
  
    /**
     * @param {ParticleBox} particleBox - model element
     * @param {Property.<boolean>} visibleProperty - are the box and its contents visible?
     * @param {Object} [options]
     */
    constructor( particleBox, visibleProperty, options ) {
  
      options = _.extend( {
        fill: 'white',  // {Color|string} fill color
        stroke: 'black', // {Color|string} stroke color
        lineWidth: 1, // {number} width of the stroke
        particleNodeOptions: null, // {*} to be filled in with defaults below
      }, options );
  
      options.particleNodeOptions = _.extend( {
        fill: 'red',
        stroke: 'gray',
        lineWidth: 0.5
      }, options.particleNodeOptions );
  
      // add particle
      this.addChild( new ParticleNode( particleBox.particle, options.particleNodeOptions ) );
      ...
    }
  }
  ```
  
  A possible exception to this guideline is when the constructor API is improved by hiding the implementation details, i.e. not revealing that a sub-component exists. In that case, it may make sense to use new top-level options.  This is left to developer and reviewer discretion.
  
  For more information on the history and thought process around the "nested options" pattern, please see https://github.com/phetsims/tasks/issues/730.

- [ ] Constructor and function documentation.  Parameter types and names should be clearly specified for each constructor and function using `@param` annotations.  The description for each parameter should follow a hyphen.  Primitive types should use lower case. For example:

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

- [ ] For most functions, the same form as above should be used, with a `@returns` annotation which identifies the return type and the meaning of the returned value.  Functions should also document any side effects.  For extremely simple functions that are just a few lines of simple code, an abbreviated line-comment can be used, for example: `// Computes {Number} distance based on {Foo} foo.`

- [ ] If references are needed to the enclosing object, such as for a closure, `self` should be defined, but it should only be used in closures.  The `self` variable should not be defined unless it is needed in a closure.  Example:
  
  ```js
  const self = this;
  someProperty.link( function(){
    self.doSomething();
  } );
  this.doSomethingElse();
  ```

- [ ] Generally, lines should not exceed 120 columns. Break up long statements, expressions, or comments into multiple
lines to optimize readability.  It is OK for require statements or other structured patterns to exceed 120 columns.
Use your judgment!

- [ ] Use `class` and `extends` for defining classes and implementing inheritance. `PHET_CORE/inherit` was a pre-ES6 implementation of inheritance that is specific to PhET and has been supplanted by `class` and `extends`. `inherit` should
not be used in new code.

- [ ] Functions should be invoked using the dot operator rather than the bracket operator.  For more details, please see https://github.com/phetsims/gravity-and-orbits/issues/9. For example:
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

- [ ] It is not uncommon to use conditional shorthand and short circuiting for invocation. Use parentheses to maximize readability.

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

- [ ] Naming for Property values:  All `AXON/Property` instances should be declared with the suffix `Property`.  For example, if a visible property is added, it should have the name `visibleProperty` instead of simply `visible`.  This will help to avoid confusion with non-Property definitions.

- [ ] Properties should use type-specific subclasses where appropriate (.e.g BooleanProperty, NumberProperty, StringProperty) or provide documentation as to why they are not.

- [ ] Are Property value validation options (`valueType`, `validValues`, etc...) utilized? Is their presence or lack thereof properly documented?

- [ ] Line comments should generally be preceded by a blank line.  For example:

  ```js
  // Randomly choose an existing crystal to possibly bond to
  const crystal = this.crystals.get( _.random( this.crystals.length - 1 ) );
  
  // Find a good configuration to have the particles move toward
  const targetConfiguration = this.getTargetConfiguration( crystal );
  ```

- [ ] Line comments should have whitespace between the `//` and the first letter of the line comment.  See the preceding example.

- [ ] Differentiate between `Property` and "property" in comments. They are different things. `Property` is a type in AXON; property is any value associated with a JavaScript object. Often "field" can be used in exchange for "property" which can help with clarity.

- [ ] Files should be named like `CapitalizedCamelCasing.js` when returning a constructor, or `lowerCaseCamelCasing.js` when returning a non-constructor function or singleton.  When returning a constructor or singleton, the constructor name should match the filename.

- [ ] Every type, method and property should be documented.

- [ ] The HTML5/CSS3/JavaScript source code must be reasonably well documented.  This is difficult to specify precisely, but the idea is that someone who is moderately experienced with HTML5/CSS3/JavaScript can quickly understand the general function of the source code as well as the overall flow of the code by reading through the comments.  For an example of the type of documentation that is required, please see the example-sim repository.

- [ ] Assertions should be used appropriately and consistently. Type checking should not just be done in code comments. Use `Array.isArray` to type check an array.

- [ ] Abstract methods (normally implemented with an error) should be marked with `@abstract` jsdoc.

- [ ] If you need to namespace an inner class, use `{{namespace}}.register`, and include a comment about why the inner class needs to be namespaced. For example:
  
  ```js
  const myNamespace = require(...);
  
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

### Type Expressions

- [ ] Type expressions should conform approximately to [Google Closure Compiler](https://github.com/google/closure-compiler/wiki/Annotating-JavaScript-for-the-Closure-Compiler) syntax.  PhET stretches the syntax in many cases (beyond the scope of this document to describe).

- [ ] Prefer the most basic/restrictive type expression when defining APIs.  For example, if a client only needs to know that a parameter is `{Node}`, don’t describe the parameter as `{Rectangle}`.

- [ ] All method parameters should have type expressions. For example `@param {number} width`.

- [ ] In sim-specific code, options and fields should have type expressions when their type is not obvious from the context.  “Obvious” typically means that the value type is clearly shown in the righthand-side of the definition. E.g. `const width = 42` clear shows that `width` is `{number}`. E.g. `const checkbox = new Checkbox(…)` clearly shows that `checkbox` is `{Checkbox}`.   If the type is obvious from the context, the developer may still provide a type expression at his/her discretion.  Examples:

  ```js
  // @public {GameState} the current state of the game
  this.gameState = this.computeGameState();
  
  // @public (read-only) the width of the container
  this.containerWidth = 150;
  
  // @private the checkbox used to show particles
  this.particlesVisibleCheckbox = new Checkbox(...);
  ```

- [ ] In common code repositories all options and fields should have type expressions, regardless of  their visibility, and regardless whether their type is obvious from the context. If the same examples from above appeared in common code:
  
  ```js
  // @public {GameState} the current state of the game
  this.gameState = this.computeGameState();
  
  // @public (read-only) {number} the width of the container
  this.containerWidth = 150;
  
  // @private {Checkbox} the checkbox used to show particles
  this.particlesVisibleCheckbox = new Checkbox(...);
  ```

- [ ] Type expressions for Enumeration values should be annotated as instances of that Enumeration, see examples in https://github.com/phetsims/phet-core/blob/master/js/Enumeration.js for more.
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
  
- [ ] Look for cases where the use of type expressions involving Property subclasses are incorrect.  Because of the structure of the `Property` class hierarchy, specifying type-specific Properties (`{BooleanProperty}`, `{NumberProperty}`,...) may be incorrect, because it precludes values of type `{DerivedProperty}` and `{DynamicProperty}`.   Similarly, use of `{DerivedProperty}` and `{DynamicProperty}` precludes values of (e.g.) `{BooleanProperty}`. Especially in common code, using `{Property,<TYPE>}` is typically correct, unless some specific feature of the `Property` subclass is required.  For example, `{Property.<boolean>}` instead of `{BooleanProperty}`.

### Visibility Annotations
Because JavaScript lacks visibility modifiers (public, protected, private), PhET uses JSdoc visibility annotations to document the intent of the programmer, and define the public API. Visibility annotations are required for anything that JavaScript makes public. Information about these annotations can be found here. (Note that other documentation systems like the Google Closure Compiler use slightly different syntax in some cases. Where there are differences, JSDoc is authoritative. For example, use `Array.<Object>` or `Object[]` instead of `Array<Object>`). PhET guidelines for visibility annotations are as follows:

- [ ] Use `@public` for anything that is intended to be part of the public API.
- [ ] Use `@protected` for anything that is intended for use by subtypes.
- [ ] Use `@private` for anything that is NOT intended to be part of the public or protected API.
- [ ] Put qualifiers in parenthesis after the annotation, for example:
  - [ ] To qualify that something is read-only, use `@public (read-only)`. This indicates that the given property (AND its value) should not be changed by outside code (e.g. a Property should not have its value changed)
  - [ ] To qualify that something is public to a specific repository, use (for example) `@public (scenery-internal)`
  - [ ] For something made public solely for a11y, use `@public (a11y)`
  - [ ] For something made public solely for phet-io, use `@public (phet-io)`
  - [ ] Separate multiple qualifiers with commas. For example: `@public (scenery-internal, read-only)`
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
  // @public Adds a {function} listener
  addListener: function( listener ) { /*...*/ }
  ```

- [ ] Verify that every JavaScript property and function has a visibility annotation. Here are some helpful regular expressions to search for these declarations as PhET uses them.
  * Regex for property assignment like `x.y = something`: `[\w]+\.[\w]+\s=`
  * Regex for function declarations: `[\w]+: function\(`

## **Math Libraries**

- [ ] `DOT/Util.toFixed` or `DOT/Util.toFixedNumber` should be used instead of `toFixed`. JavaScript's `toFixed` is notoriously buggy. Behavior differs depending on browser, because the spec doesn't specify whether to round or floor.

## IE11
- [ ] No usage of `Number.parseInt()`
- [ ] No usage of `Array.prototype.find`

## **Organization, Readability, and Maintainability**

- [ ] Does the organization and structure of the code make sense? Do the model and view contain types that you would expect (or guess!) by looking at the sim? Do the names of things correspond to the names that you see in the user interface?
- [ ] Are appropriate design patterns used? See [phet-software-design-patterns.md](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md).  If new or inappropriate patterns are identified, create an issue.
- [ ] Is inheritance used where appropriate? Does the type hierarchy make sense?
- [ ] Is there any unnecessary coupling? (e.g., by passing large objects to constructors, or exposing unnecessary properties/functions)
- [ ] Is there too much unnecessary decoupling? (e.g. by passing all of the properties of an object independently instead of passing the object itself)?
- [ ] Are the source files reasonable in size? Scrutinize large files with too many responsibilities - can responsibilities be broken into smaller delegates?
- [ ] Are any significant chunks of code duplicated? This will be checked manually as well as with https://github.com/danielstjules/jsinspect or `grunt find-duplicates`
- [ ] Is there anything that should be generalized and migrated to common code?
- [ ] Are there any `TODO` or `FIXME` comments in the code?  They should be addressed or promoted to GitHub issues.
- [ ] Are there any [magic numbers](https://en.wikipedia.org/wiki/Magic_number_(programming)) that should be factored out as constants and documented?
- [ ] Are there any constants that are duplicated in multiple files that should be factored out into a `{{REPO}}Constants.js` file?
- [ ] Is [PhetColorScheme](https://github.com/phetsims/scenery-phet/blob/master/js/PhetColorScheme.js) used where appropriate? Verify that the sim is not inventing/creating its own colors for things that have been standardized in `PhetColorScheme`.  Identify any colors that might be worth adding to `PhetColorScheme`.
- [ ] Does the implementation rely on any specific constant values that are likely to change in the future? Identify constants that might be changed in the future. (Use your judgement about which constants are likely candidates.) Does changing the values of these constants break the sim? For example, see https://github.com/phetsims/plinko-probability/issues/84.
- [ ] Are all dependent properties modeled as `DerivedProperty` instead of `Property`?
- [ ] All dynamics should be called from Sim.step(dt), do not use window.setTimeout or window.setInterval.  This will help support Legends of Learning and PhET-iO.

## **Accessibility**
- [ ] Does the sim pass an accessibility fuzz test? (run with query parameters `fuzzBoard&ea`)
- [ ] Run the accessible HTML through an [HTML validator](https://validator.w3.org/nu/#textarea), does the HTML pass?
- [ ] Are accessibility features integrated well into the code. They should be added in a maintainable way, even if that requires upfront refactoring.
- [ ] Are accessible design patterns used, see [accessible-design-patterns.md](https://github.com/phetsims/phet-info/blob/master/doc/accessible-design-patterns.md)
- [ ] Does resetting the simulation also reset the entire PDOM?
- [ ] Is `Node.accessibleOrder` used appropriately to maintain visual and PDOM layout balance?

## **PhET-iO**

- [ ] If the simulation is supposed to be instrumented for PhET-iO, please see [How to Instrument a PhET Simulation for PhET-iO](https://github.com/phetsims/phet-io/blob/master/doc/how-to-instrument-a-phet-simulation-for-phet-io.md)
for the PhET-iO development process.
