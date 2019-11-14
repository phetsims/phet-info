# PhET Software Design Patterns

This document describes software design patterns that are specific to PhET, and PhET-specific applications
of standard design patterns.

## Table of Contents

* [Composition and Inheritance](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#composition-and-inheritance) 🚧
* [Creator](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#creator-with-drag-forwarding)
* [Dependency Injection](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#dependency-injection)
* [Dispose](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#dispose)
* [Enumeration](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#enumeration)
* [Mixin and Trait](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#mixin-and-trait)
* [Model-View Controller](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#model-view-controller) 🚧
* [Module](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#module)
* [Namespace](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#namespace)
* [Observer](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#observer) 🚧
* [Options and Config](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#options-and-config)
* [Prototypal Inheritance](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#prototypal-inheritance) 🚧
* [Singleton](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#singleton)
* [State Machine](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#state-machine)
* [Strategy](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#strategy)

## Composition and Inheritance

Author: 🚧

  - Noted as a new topic during patterns discussion on 2/11/19.
  - Would be good to note PhET decisions and patterns for this here.
  - Relavant info/links:
    - https://en.wikipedia.org/wiki/Composition_over_inheritance
      - "Composition over inheritance (or composite reuse principle) in object-oriented programming (OOP) is the principle that classes should achieve polymorphic behavior and code reuse by their composition (by containing instances of other classes that implement the desired functionality) rather than inheritance from a base or parent class."
    - Chrome's optimization makes it so that sims would be faster if we used composition over inheritance.
    - Composition is generally more flexible.
  - If what you are trying to model can easily be described by composition, you should use composition.
  - If composition produces numerous forwarding calls, it indicates that perhaps inheritance should be used instead.
    - The forwarding calls produced by composition can be beneficial though, they are explicit and protect things things
    that need to stay private.
  - It was mentioned that numerous forwarding calls can increase the memory impact, especially on types that are instantiated many many times by a simulation (like Vector2).

## Creator (with Drag Forwarding)
(formerly known as the Model Element Creator Pattern)

Author: @samreid

Simulations may allocate all of the objects during startup, or may dynamically create new instances while the simulation
is running.  In the case where the dynamically created instances are created by dragging an icon in a toolbox or panel,
there is the additional complexity of making sure the drag event that began on the icon continues on the newly created
item.  This issue was originally identified and explored in https://github.com/phetsims/scenery-phet/issues/214.

This pattern is also described in equality-explorer/doc/implementation-notes.md "Creator Pattern"

Generally speaking, the pattern for creating a new item by dragging from the control panel works like so:
1. The user drags an icon in a toolbox or control panel
2. This triggers a new model element to be created (usually positioned above the icon, so it is not occluded by touch)
3. The view receives a message from the model that a new element has been created, and the view creates the corresponding
view node.
4. The drag event is forwarded to the listener for the view node.

For disposal:
1. The item is dropped back into the toolbox or otherwise deleted/removed/erased.
2. This triggers the model to remove the model element
3. The view receives a message that the model element has been removed, and removes the corresponding view node.

A simple, working example of this pattern is implemented in scenery/examples/creator-pattern.html

Simulations that use DragListener.createForwardingListener (recommended pattern)
* Energy Skate Park (Measuring tape)
* Fractions Suite (Pieces, fraction elements and containers)
* Wave Interference (Tools)

Simulations that use SimpleDragHandler.createForwardingListener (similar to recommended pattern)
* Capacitor Lab Basics (Voltmeter)
* Circuit Construction Kit (Circuit elements and sensors)
* Equality Explorer (Terms)
* Fluid Pressure and Flow (Sensors)
* Masses and Springs (Ruler and timer)
* Projectile Motion (Tracer and measuring tape)

Deprecated solutions to this same problem:
* Bending Light uses handleForwardedStartEvent, handleForwardedDragEvent, handleForwardedEndEvent

Simulations with other strategies:
* Charges and Fields uses `hookDragHandler`, see ChargesAndSensorsPanel.js
* Balancing Act uses:

Variants or Alternate problems:
* It is possible to use the drag forwarding pattern without dynamically creating instances.  For instance,
in Wave Interference, there is only one Wave Meter Node, so dragging the icon displays the view and forwards the event
without creating a new one.
* Forces and Motion: Basics doesn't dynamically create elements.  The real elements are already in the toolbox,
hence no creation or forwarding takes place.

For discussion:
* phet-io (these listeners should be instrumented and these interactions should appear in the data stream),
  Newly created items could be assigned tandems with tandem.createGroupTandem().createNextTandem() (if they are enumerated
  like `resistor42`).
  or preassigned tandems (if they are uniquely identified, like `voltmeterA` and `voltmeterB`).
* accessibility (hasn't been designed yet)
* improving/fixing the "lookup" phase: CHECK!
* adding entries to other "Deprecated" and "Alternate" sections

## Dependency Injection

Author: @mbarlow12

Some background reading for those interested:
* https://martinfowler.com/articles/injection.html
* https://en.wikipedia.org/wiki/Dependency_injection
* https://www.jamesshore.com/Blog/Dependency-Injection-Demystified.html

SR was an advocate of this in https://github.com/phetsims/tasks/issues/952. Clarify which form of dependency injection
(probably constructor-based injection), and some examples of where it's currently used in PhET sims.

The main goal of DI is to decouple the implementation of a required object instance from where it’s used. While there are a few different ways to accomplish this, the basic idea is to provide the wrapping class with its required instance variables instead of allowing it to instantiate them itself. For example,

```js
class MyClass {
    constructor() {
        this.otherObject = new OtherObject();
    }
}
```
Here, `MyClass` is tightly coupled to the specific implementation of `OtherObject` making it rather inflexible. With DI, you instantiate the object elsewhere and add it to a class via its constructor (Constructor Injection) or through a setter (Setter Injection)

```js
class MyClass {
  constructor( otherObject ) {
    this.otherObject = otherObject;
  }
}
```

```js
class MyClass {
  _setOtherObject( otherObject ) {
    this.otherObject = otherObject;
  }

  set otherObject( otherObject ) {
    this._setOtherObject( otherObject );
  }
}
```

There are other forms of DI using interfaces or service locators, but they're not really applicable for the vast majority of PhET use cases. In JavaScript, since everything is an `Object`, you could say that any assignment to class/object properties from a constructor/method is DI since they all extend `Object`'s methods.

```js
class MyClass {
  constructor( aString, anArray, otherObject ) {
    super();
    this.aString = aString;
    this.anArray = anArray;
    this.otherObject = otherObject;
  }

  myClassToString() {
    return this.aString.toString() + this.anArray.toString() + this.otherObject.toString();
  }
}

const myClassInstance = new MyClass( 'hello', [ 'there', 'world' ], new DifferentOtherObjectImplementation() );
myClassInstance.myClassToString();
```

This takes advantage of the fact that while each argument has a `toString` method, their implementations can be wildly different (provided the implementation still returns a `string`).

-------------

We already see a lot of straightforward DI at PhET such as passing `model` or `Property` instances as constructor arguments or in our `options` and `config` objects. How PhET handles DI is largely up to the developer and we can find instances of each flavor in our codebase; however, we most commonly see dependencies passed either as constructor arguments or within our options/config objects. When deciding what approach to take, it's generally a good idea to examine the those objects for their complexity. Large, heavily nested options objects are a relatively good indicator that DI may simplify your implementation.

To start, [Molecules and Light](https://github.com/phetsims/molecules-and-light) employs setter injection in how it handles absorption of various wavelengths of light for different molecules.

In [Molecule.js](https://github.com/phetsims/molecules-and-light/blob/master/js/photon-absorption/model/Molecule.js), the constructor initializes `this.mapWavelengthToAbsorptionStrategy = {}`. Then on ln 189, we have the following method allows any object inheriting Molecule to dynamically set the necessary `PhotonAbsorptionStrategy`

```js
setPhotonAbsorptionStrategy( wavelength, strategy ) {
  this.mapWavelengthToAbsorptionStrategy[ wavelength ] = strategy;
}
```
An example of DI through the options object can be found in [Slider.js](https://github.com/phetsims/sun/blob/master/js/Slider.js). There are a series of options that allow the client to alter the appearance of the Slider’s thumb, but the client can also pass an instance of a `SliderThumb` in the options that will override the [defaults](https://github.com/phetsims/sun/blob/b4fadc867525be5577febefd3324064e6684e2f2/js/Slider.js#L70).

```js
var thumb = options.thumbNode || new SliderThumb( {

  // propagate options that are specific to SliderThumb
  size: options.thumbSize,
  fill: options.thumbFill,
  fillHighlighted: options.thumbFillHighlighted,
  stroke: options.thumbStroke,
  lineWidth: options.thumbLineWidth,
  centerLineStroke: options.thumbCenterLineStroke,
  tandem: options.tandem.createTandem( 'thumb' )
} );
```

This is useful if the requirements go beyond the provided defaults (e.g. registering a custom input listener on the thumb).

## Dispose

Author: @zepumph

Disposal is the process of freeing up memory so that it can be garbage collected. In general, JavaScript will garbage
collect. A memory leak is when an Object in the sim keeps a reference to something that should be garbage collected.
This reference inhibits garbage collection from happening. The dispose pattern helps to prevent. An instance needs to
be disposed if any code outside that Type has a reference to it. For example a Type needs to be disposed if a listener
is added to an `AXON/Emitter` that was passed into that Type's constructor. You do not need to dispose an instance if
references are only between type and its children. Because it is self contained, it can be garbage collected as a
whole. For more information about the general pattern, see https://en.wikipedia.org/wiki/Dispose_pattern

A leak often happens due to the Observer pattern. If you own the observable and ALL of its observers (and there is no
chance of outside observers being added), then you don't need to dispose. if you own only the observable or the
observers, then you need to dispose by cutting those references.

Note: when use `SCENERY/Node` that need disposal, be careful about disposing when using DAG (directed asyclic graph)
features.

[Here](https://github.com/phetsims/sun/issues/121#issuecomment-209141994) is a
helpful list of actions that likely need doing while disposing:
  1. remove observers from things (Property, Emitter, Events) that were provided by the client
  2. dispose of any subcomponents that require disposal
  3. de-register from tandem (data collection)

Once establishing that you need to dispose a type, add the `dispose` method to the prototype. This method should be
`@public` and is likely an `@override`. The `dispose` method on the prototype, when called, should completely
release this object from any references that would otherwise keep it from being garbage collected. Make sure that this
method calls its parent and mixin disposals as well. In the view a type will likely extend from `{{Node}}` and, as such,
you will call `Node.prototype.dispose.call( this );` (for es5). In general call `this` type's dispose before the
parent's call to tear down code in the opposite order of construction.

Below are a few methods to implement disposal specifics. They are listed in order of preference, and the first should be
used unless it can't, the same for the next, and so on.

----------

The preferred approach in implementing disposal for PhET code is to create a private member function in the constructor
called `this.dispose{{TypeName}}` (see [issue](https://github.com/phetsims/tasks/issues/727)), and then to call that
method from the `dispose` method (on the prototype). With disposal order in mind, the generally safest order of
disposal within `this.dispose` is to call `this.dispose{{TypeName}}` before calling for the parent. Within
`this.dispose{{TypeName}}`, the generally safest order of disposal is the opposite order of component creation.

Here is an example of using this disposal method. Note that the `Property` is unlinked before the child is removed
from the `Node`.

```js
class MyAddChildAndLinkNode extends Node{
  constructor( aNode, aProperty){

    super();

    const aNewNode = new Node();
    aNode.addChild( aNewNode );

    const aFunction = ()=>{ console.log( 'I love this Property.' )};
    aProperty.link( aFunction);

    this.disposeMyAddChildAndLinkNode = ()=>{
      aProperty.unlink( aFunction);

      // Because aNewNode has a reference back to its parent (aNode). Note there are many ways that this reference
      // could be removed.
      aNode.removeChild( aNewNode);
    }
  }

  /**
  * @override
  * @public
  */
  dispose(){
    this.disposeMyAddChildAndLinkNode();
    super.dispose();
  }
}
```


----------

If performance is an important consideration for a type, then the above pattern is less desirable because it creates a
closure for each instance. That method can be adapted, and the constructor closure removed. Instead promote any local
variables that would be needed for disposal to `@private` instance fields and move that logic directly to the `dispose`
method, like below.

```js
class MyAddChildAndLinkNode extends Node{
  constructor( aNode, aProperty){

    super();

    // @private
    this.aNode = aNode;
    this.aProperty = aProperty;

    this.aNewNode = new Node();
    this.aNode.addChild( this.aNewNode );

    this.aFunction = ()=>{ console.log( 'I love this Property.' )};
    this.aProperty.link( this.aFunction);

  }

  /**
  * @override
  * @public
  */
  dispose(){
    this.aProperty.unlink( this.aFunction);
    this.aNode.removeChild( this.aNewNode);
    super.dispose();
  }
}
```

Sometimes the above, preferred patterns won't work. For example sometimes components are conditionally created, and
therefore are only conditionally disposed. If there are these sorts of complex disposal constraints, then create an
`AXON/Emitter` to manage disposal tasks, and add a listener to the Emitter for each disposal task.

* Name the emitter like `disposeEmitter{{TypeName}}`
* Add listeners to the Emitter, recognizing that listener order is not guaranteed.
* In the `dispose` method, emit the dispose emitter, and call the parent dispose (`super.dispose()`) in the appropriate
order.

See [issue](https://github.com/phetsims/axon/issues/214) for details on the "dispose emitter" pattern.

----------

A deprecated pattern once used for disposal involves creating an array to keep track of items to dispose. Often this
array is called `disposeActions`, and is of type `{Array.<function>}`. For example see use of `this.disposeActions`
[here](https://github.com/phetsims/circuit-construction-kit-common/blob/91d44b050d79627bf0d470e3b2f1029976e6e004/js/view/CircuitElementNode.js#L71)

-------------

Here are some issues that have investigated trying to bring creation and disposal closer together:
* https://github.com/phetsims/axon/issues/84
* https://github.com/phetsims/axon/issues/93

## Enumeration

Author: @pixelzoom

This is a standard pattern described in https://en.wikipedia.org/wiki/Enumerated_type.

PhET’s preferred implementation of this pattern can be found in [Enumeration.js](https://github.com/phetsims/phet-core/blob/master/js/Enumeration.js).
Examples and coding conventions are in the comment header of that file.  See the wave-interference repository for
exemplars of Enumeration use.  Rich enumerations are not currently supported, but may be supported in the future
(see https://github.com/phetsims/phet-core/issues/50).

You’ll find a couple of other patterns commonly used in PhET code. These are good to know, but should be avoided in new
code.

(1) A set of string values.  For example, [Slider.js](https://github.com/phetsims/sun/blob/master/js/Slider.js) uses
`’horizontal’` and `’vertical’` as the values for its `orientation` option. This approach results in the duplication of
string literals throughout the code.

(2) Idiomatic JavaScript implementation, as described in [StackOverflow](https://stackoverflow.com/questions/287903/what-is-the-preferred-syntax-for-defining-enums-in-javascript).
The typical implementation associates named keys with numeric values. PhET’s implementation uses string values (to
facilitate debugging) and `Object.freeze`  to prevent unintentional modification. See for example
 [SolutionType.js](https://github.com/phetsims/acid-base-solutions/blob/master/js/common/enum/SolutionType.js).

## Mixin and Trait

Author: @jessegreenberg

Descriptions for each standard pattern can be found here:
  - Mixin: https://en.wikipedia.org/wiki/Mixin
  - Trait: https://en.wikipedia.org/wiki/Trait_(computer_programming)

More information about traits can be found here: http://scg.unibe.ch/archive/papers/Scha03aTraits.pdf

Notes on PhET's decisions regarding mixin vs trait can be found here: https://github.com/phetsims/scenery/issues/700

Summarizing the above, traits and mixins allow the code reuse benefits of multiple inheritance without using actual
multiple inheritance.

PhET's definition of mixin and trait does not perfectly align with standard definitions. By standard definition, the
differences are:
  - A trait requires methods from the class it is mixed into, a mixin doesn't.
  - A trait can be composed by combining existing traits, a mixin can't.
  - A trait can't specify or access state variables, a mixin can.

PhET defines the difference between mixin and trait as:
  - A trait can require methods and properties from the class it is mixed into, a mixin cannot.

It is OK for the type mixing in the mixin or trait to reference properties and methods defined by the mixin or trait.
However, only traits can use properties or methods from the type using the trait. Mixins cannot use anything from the
class it is mixed into.

### Shadowing
With the current pattern for mixin/trait, there is no guard against accidentally shadowing properties and methods of
the class using the mixin. Support for catching this is being investigated in https://github.com/phetsims/phet-core/issues/54.

### When to use Mixin and Trait
In general, composition should be favored over inheritance and inheritance should be favored over mixin. If the composition
pattern produces lots of forwarding calls, it is an indication that you should be using inheritance or mixin instead.
The mixin pattern should only be used as a substitute for multiple inheritance only if single inheritance is not desirable
or is difficult to use.

### Examples
An example of PhET mixin is phet-core/Poolable. An example of a PhET trait is scenery/Paintable.

Creating and using mixins and traits will look similar. Both will have
  - A `mixInto` method that is called on the class using the mixin/trait.
  - An `initialize{{Name}}` method that will be called in the constructor of the class using the mixin/trait.
  - If necessary, the mixin/trait should have a `dispose{{Name}}` method that handles disposal, to be called by the
  type using the mixin/trait when it is disposed. Method should not be named `dispose` to avoid overriding the `dispose`
  method of the mixing type.
  - The class using the mixin/trait will have `@mixes {{Name}}` annotation at the constructor.

The only difference is traits should have assertions in the `mixInto` method to verify the class and requirements.

<details><summary>Trait Example</summary>

```js
// the trait to be mixed into a type
const MyTrait = {

  /**
   * Adds MyTrait methods to the prototype.
   * @param {function} myType - must be a subtype of SuperType
   */
  mixInto: myType => {
    assert && assert( _.includes( inheritance( myType ), SuperType ), 'Only SuperType types should mix MyTrait' );

    extend( myType.prototype, {

      /**
       * This should be called in the constructor of a SuperType.
       */
      initializeMyTrait: () => {},

      /**
       * Called when disposing the type mixing in this trait
       */
      disposeMyTrait: () => {},

      //...
    } );
  }
}

// the class mixing in the trait
class MyClass extends SuperClass {

  /**
   * @mixes MyTrait
   */
  constructor() {
    super();

    // to initialize features of the trait
    this.initializeMyTrait();
  }

  /**
   * Make eligible for garbage collection.
   */
  dispose() {

    // if MyTrait requires/implements disposal
    this.disposeMyTrait();
  }
}

// to mix MyTrait methods into the prototype, after inherit for es5 usages
MyTrait.mixInto( MyClass );
```
</details>

## Model-View Controller

Author: 🚧

A standard pattern described in https://en.wikipedia.org/wiki/Model–view–controller

`Screen`, `ScreenView`, model container, `Property`, `Emitter`, `Nodes`

Most important pattern for new developers

## Model-View Transform

Author: 🚧

role in MVC, examples to demystify scenery transform methods (`localToGlobalPoint`, etc.).
When should you use `localToGlobalPoint` instead of `parentToGlobalPoint` and
`globalToParentPoint` instead of `globalToLocalPoint`?

## Module

Author: @Denz1994 

A module is a program unit that contains declarations which formulate the classes and objects in a system. Modularity is a property of a system whose modules can be compiled independently, but have connections with other modules.  A module has two core components: its interface and its implementation. JavaScript modules are useful to define a unit of code and how to register a value for the module. Additionally, modules allow  units of code to reference other units of code.

More background reading:

- Modular Programming [wiki](https://en.wikipedia.org/wiki/Modular_programming)
- Object-Oriented Programming with Applications by Grady Booch
- Effective JavaScript by David Herman

Modules operate as independent pieces of code and are used throughout the whole PhET project. Take a look at some examples in [sim code](https://github.com/phetsims/equality-explorer/blob/master/js/common/view/BoxNode.js), [common code](https://github.com/phetsims/joist/blob/master/js/HomeButton.js), and [code for build tools](https://github.com/phetsims/perennial/blob/master/js/common/build.js).

----

#### Importing Modules:

PhET relies heavily on RequireJS to support importing modules. RequireJS is flexible enough to support browser-based platforms and server sided environments, such as Node.js. RequireJS pulls inspiration from CommonJS (a popular module format) but improves on it by coding a module format that works well natively in a browser. For more information, read the RequireJS [documentation](https://requirejs.org/).

RequireJS imports are handled at top of all files and use the `require` keyword. Typically, require statements for importing would look something like this:

```js
    const Node = require( 'SCENERY/nodes/Node' );
```
where `SCENERY` is an alias or symbolic constant that represents a path to the repository where the module lives. This follows a condensed syntax compatible with CommonJS based on asycnhronous module dependency (AMD). This [article](https://requirejs.org/docs/whyamd.html) is a great resource for further reading. Note we are not using ES6 modules, but this may change in the upcoming months.

Be aware of two cases, when using `require` should be reconsidered. 

1. Some types of [circular dependencies](https://en.wikipedia.org/wiki/Circular_dependency)
2. Using conditional code to do a require call like, _if(someCondition) require('a1') else require('a2')_;

Generally circular dependencies, require a rethinking of design or a workaround. For example, if `Node.js` requires `Trail.js` and `Trail.js` requires `Node.js.` We can load both modules from the `Scenery` namespace and access them through `scenery.Node` or `scenery.Trail`. The assumption is that the modules are loaded into the namespace before they are being used. The circular dependency is documented near the require statements of both files.

Also if the same file contains two different modules with the same name, RequireJS may consider this a circular dependency. For example, both `KITE` and `NODE` have modules called `Rectangle.js`. The current solution employed involves using a specialized `// eslint-disable` as a workaround.

Additionally, you may come across conditional module declarations, such as this code snippet from [Chipper/js/common/getLicenseEntry.js](https://github.com/phetsims/chipper/blob/master/js/common/getLicenseEntry.js): 
```js
  // browser require.js-compatible definition
  if ( typeof define !== 'undefined' ) {
    define( function() {
      return getLicenseEntry;
    } );
  }

  // Node.js-compatible definition
  if ( typeof module !== 'undefined' ) {
    module.exports = getLicenseEntry;
  }
```

If you come across conditional declarations like the one above, this module is most likely utilized in both client sided and server sided code. The difference in the declaration is needed due to limitations by RequireJS. This is also referred to as a [Universal Module Definition](https://www.davidbcalhoun.com/2014/what-is-amd-commonjs-and-umd/) and is compatible with both CommonJS and RequireJS.

Lastly, there is a pattern used for PhET-io wrappers that gets away from the RequireJS overhead. This pattern involves initializing the module directly to the `window` object and calling it in from the HTML DOM using a `<script>` tag.

----

#### Module catagories:

JS doesn’t support strict typing so we categorize our module require statements into sections such as modules, strings, images, sound, phet-io, etc. This is an organizational practice for readability and is documented as such.

Specific support for catagories that need plugins follow the RequireJS API as described in its [documentation](https://requirejs.org/docs/plugins.html#api) 
```js
  // strings
  const modelString = require( 'string!GRAVITY_AND_ORBITS/model' );
```
----

#### Anatomy of a module:

The PhET codebase follows a similar pattern for module structure as outlined below:

- Top level documentation: General purpose, authorship, and copyright
- Declaration as a function using strict
- Import:  statements using `require`
- Constructor: Houses the main body of our module (attributes and elements)
- NameSpace: Register our module to avoid conflicts (see [Namespace](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#namespace) section)
- Inherit: Module dependency, methods, and statics

Putting it all together modules will usually follow this format:

```js

// Copyright 2013-2018, University of Colorado Boulder

/**
 * Example Node used for demonstrating typical module formatting in the PhET project.
 *
 * @author Denzell Barnett (PhET Interactive Simulations)
 */

// Declaration using strict mode.
define( require => {
  'use strict';

  // Imports
  const inherit = require( 'PHET_CORE/inherit' );
  const Node = require( 'SCENERY/nodes/Node' );
  const fooRepo = require( 'FOO_REPO/fooRepo' );

  // Constructor
  function FooNode( fooArgument ) {
    // ...
  }

  // Namespace registration to repository.
  fooRepo.register( 'FooNode', FooNode );

  // Inherit is a utility function for setting up prototypal inheritance
  return inherit( Node, FooNode );
} );

```

It is important to note that 'using strict' should be enforced throughout the PhET codebase. Strict mode has the unique property of limiting certain javascript functionalities that may not be backward compatible between versions. To avoid this there are three general solutions:

1. Never concatenate strict files and nonstrict files.
2. Concatenate files by wrapping their bodies in immediately invoked function expressions.
3. Write your files so that they behave the same in either mode.


## Namespace

Author: @jonathanolson

This describes the PhET-specific conventions for the pattern described by https://en.wikipedia.org/wiki/Namespace.
Namespaces allow runtime (dev tools) access to arbitrary namespaced objects. For example, if running in a simulation,
`window.phet` is available, and has a number of other namespaces below it (e.g. `window.phet.scenery`), so that while
debugging, the type `phet.scenery.Node` can be directly accessed. In other contexts, namespaces may be directly
available on `window` (e.g. built forms of dot/kite/scenery and other related utilities). This is instead of a
"global" namespace (where every object is in one namespace), which would prevent any two types in any repositories from
having the same name (name collision). In addition another "alternative" would be to not give access to runtime objects,
but this would make debugging much more difficult.

In addition, namespaces can be used as a workaround for circular dependencies. Since requireJS does not do well with
circular dependencies, two types can refer to each other through the namespace.

For our uses, each repository generally has one namespace (available via requireJS) at the top level, e.g.
`molecule-shapes/js/moleculeShapes.js` (generally camel-cased) would contain:
```js
define( require => {
  'use strict';

  const Namespace = require( 'PHET_CORE/Namespace' );

  return new Namespace( 'moleculeShapes' );
} );
```
Thus the namespace object would be available under `phet.moleculeShapes` in simulations.

To add an object to a namespace, use the `register` method, e.g.:
```js
moleculeShapes.register( 'Bond', Bond );
```

For example, now `phet.moleculeShapes.Bond` will point to the value of `Bond` above. Note that when assertions are
enabled in require.js mode that some checks will be made to ensure that almost all modules are namespaced, and that
namespaces correspond to modules (to help catch namespace errors).

There is a somewhat-unused feature to call register with dot-separated path-like values in the string portion (for
handling things like inner classes, see https://github.com/phetsims/phet-core/issues/52), however there is some
uncertainty about the usefulness. It's @jonathanolson's opinion that this can be scrapped, and if references are
desired then they can be set directly on the main type/object for the module (e.g. `Bond.Something = Something`). It is
allowed (but not required) to namespace inner classes.

Another unused feature is to nest namespaces. It should be possible to register one namespace as an object on
another namespace.

There are some cases where more information/shortcuts are put on a namespace object, e.g. `dot.js` makes `dot.v2()`
available.

Interested developers: JG, DB, CK

## Observer

Author: @pixelzoom 🚧

A standard pattern described in https://en.wikipedia.org/wiki/Observer_pattern

`Property`, `Emitter`, ... and their role in MVC
NOTE: when this gets fleshed out, scenery input system, options callbacks should be passed the SCENERY/Event from their
input listeners.

NOTE: the author of this section should include patterns/strategies in how to identify the notifying Property in 
Multilink and DerivedProperties; see comments in expressed in https://github.com/phetsims/axon/issues/259.

Very important pattern for new developers


## Options and Config

Author: @pixelzoom, @denz1994

This pattern is used for parameterizing classes and methods, which we use to avoid an explosion of parameters. `options` and `config` are the two implementations of that pattern that PhET typically uses. If all properties in the argument are optional, then the parameter should be called `options`.  If one or more properties of the argument are required, then the parameter should be called `config`. Some elements of the `config` parameter can be optional, but each one must be documented accordingly. See "Required Fields" below for documentation. 

Use `merge` to overwrite default option values. For example, this `Node` subclass has defaults that are different from `Node`'s defaults:
```js
class MyNode extends Node {
  constructor( options ) {
    options = merge( {     
      visible: false,
      pickable: false
    }, options );
    ...
    super( options );
  }
}
``` 

We do not filter child options out before passing them a parent class or subcomponent. With this in mind, please be mindful of the option naming to make sure that you don't cause name collisions. See https://github.com/phetsims/tasks/issues/934.

Try to keep related options groups together, both for instantiation and `merge` statements. For examples, if you
have several options related to a11y, keep them together, don't interleave them with other options.

### Nesting

If using composition for your class, and you want to pass options into a subcomponent, you can nest
those options in a single property, named according to the subcomponent you are passing the options to. In this example, `options.hSliderOptions` is the nested options that will be passed to `HSlider`:

```js
class MyNode extends Node {
  constructor( options ) {

    options = merge( {
      visible: false,
      pickable: false,
      hsliderOptions: {
        endDrag: function() { console.log( 'Drag Ended') },
        startDrag: function() { console.log( 'Drag Started') }
      }
    }, options );

    var slider = new HSlider( new Property(), new Range(), options.hsliderOptions );
    ...
    super( options );
  }
  ...
}
```

In some cases, dependency injection is an appropriate alternative, see https://github.com/phetsims/tasks/issues/952.
In the above example, this would mean creating the `HSlider` externally then passing it in to the `MyNode`
constructor.

### Required fields
If one or more of the fields in `option` is required, then `options` should be renamed  to `config`. See https://github.com/phetsims/tasks/issues/930
In the `merge` call, the options should be commented as to whether they are required or optional.  Following the
`merge` call, required fields should have an assertion to verify they were provided. For example:
```js
/**
 * @param {string} name - the full name of the Person
 * @param {Object} config
 * @constructor
 */
function Person( name, config ) {
  config = merge( {
    height: null, // {number} @required - height in centimeters
    age: null, // {number} @required - age in years

    favoriteColor: null // {Color|null} optional - favorite color, if any
  }, config );

  assert && assert( config.height !== null, 'height is required' );
  assert && assert( config.age !== null, 'age is required' );
}
```
In some cases, it may be better to only indicate the `required` properties or only indicate the `optional` properties,
or to group them -- use your judgment.

### Best Practices

(1) Don't modify an options object that you don't own. If you own the options object, then direct assignment to an options field is OK. If you don't own the options object, use `merge`, to assign a field value, which creates a new object that you then own.

```js
class Shelf extends Node {
  constructor( content, options ) {
    options = merge( {
      material: 'wood',
    }, options );
  }
}
```

(2) Before setting a value in an options object (with either assignment or `merge`), verify that the client did not provide a value. Use an assertion to verify. Don't silently override what the client provided.

```js
// Create two containers
this.blueContainerNode = new ContainerNode(height, width, blueContainerOptions );
this.redContainerNode = new ContainerNode(height, width, redContainerOptions ) ;

// Explicitly set the blue container's label
assert && assert( blueContainerOptions.label === undefined, 'label was not previously set' );
blueContainerOptions.label = 'Books';
```

(3) To check whether a field exists in `options` or `config`, the expressions that you have available are:

* `options.someField === undefined` - checks if `someField` does not exist as a property
* `!options.hasOwnProperty( 'someField' )` - checks if `someField` is a non-inherited property
* `!option.someField` - checks if `someField` has a falsy value. Don't use this for boolean or number fields!
  
(4) When overriding options or config using `merge`, arguments should be ordered from least to most specific.  For example:

```js
// Incorrect
class MyPanel extends Panel {
  constructor( options ) {
    options = merge( options, {
      fill: 'yellow'
      ...
    }, MyConstants.PANEL_OPTIONS );
    ...
  }
}

// Correct
class MyPanel extends Panel { 
  constructor( options ) {
    options = merge( {}, MyConstants.PANEL_OPTIONS, {
      fill: 'yellow'
      ...
    }, options);
    ...
  }
}
```

(5) Use `config` judiciously and appropriately. If your API has too many parameters, don't immediately reach for `config` as the solution. Review your API to understand _why_ it has too many parameters, and possibly redesign.


## Prototypal Inheritance

Author: 🚧

what it is, how it differs from `class`, use of `call` and `inherit`, use with Mixin and Trait

e.g. https://medium.com/javascript-scene/master-the-javascript-interview-what-s-the-difference-between-class-prototypal-inheritance-e4cd0a7562e9

## Singleton

Author: @chrisklus

This is a standard pattern described in https://en.wikipedia.org/wiki/Singleton_pattern.

When using JavaScript and a module loading system (like RequireJS), there are two patterns that we use for Singletons.

The first is to create a class and then return a single instance of the class *instead* of returning the class itself.

```js

define( require => {

  class Singleton {

    constructor( x ) {
      this.x = x;
      this.initialized = false
    }

    getX() {
      assert && assert( this.initialized, 'this should only be called after initialization' );
      return this.x;
    }

    setX( x ) {
      assert && assert( this.initialized, 'this should only be called after initialization' );
      this.x = x;
    }

    initialize( x ) {
      assert && assert( !this.initialized, 'this should only be initialized once' );
      this.initialized = true;
      this.setX( x );
    }

  };

  const singleton = new Singleton( 0 );
  return namespace.register( 'singleton', singleton );

} );
```

A class should be used whenever keeping track of state is desired. The convention for naming a singleton class file is to start with a lowercase letter since an instance of the class is imported.

If initial state information is needed, then we can use an initialize pattern like what's written above. This is preferable to the getInstance pattern because it is simpler and does not expose the contructor. Also, since a single instance is being registered, the module loading system is basically doing getInstance for us.

phetioEngine.js is an example of this pattern in PhET code.

The second pattern is to create a static object literal. These cannot be instantiated, but instead are loaded at runtime.

```js

define( require => {

  console.log( 'I\'m only going to say this once.' );

  const ExampleConstants = {

    printMessage() {
      console.log( 'I\'ll say this as many times as you\'d like.' );
    },

    CONSTANT_NUMBER_ONE: 1,
    CONSTANT_NUMBER_ONE: 2,

  };

  return namespace.register( 'ExampleConstants', ExampleConstants );
}
```

An object literal should be used when keeping track of state is not needed. If one counter variable needs to be tracked (or something very simple like that), then the dev team thinks that it could still be appropriate to use an object literal. A class should be used for anything more substantial than that. The convention for naming a singleton object literal file is to start with an uppercase letter since a singleton object literal is not an instance of a class.

Simulation constant files are a common example of this pattern in PhET code (e.g. WaveInterferenceConstants.js).

To use a singleton, simply import it to your file and invoke methods directly on it.

```js

const singleton = require( 'SIMULATION_NAME/singleton' );
const ExampleConstants = require( 'SIMULATION_NAME/ExampleConstants' );

console.log( singleton.getX() );

ExampleConstants.printMessage();

```

## State Machine

Author: @jbphet

In general, a state machine, also known as a Finite-State Machine (FSM), is an abstract machine that
can be in one and only one of a finite number of states at any one time and takes actions and changes
its state in response to inputs, aka stimuli.  In the book "Design Patterns: Elements of Reusable
Object-Oriented Software" by Gamma, Helm, Johnson, and Vlissides, the pattern is simply referred to
as "State".  In the book "Head First Design Patterns" by Freeman & Freeman, the pattern is defined
as follows:

> The State Pattern allows an object to alter its behavior when its internal state changes.  The
> object will appear to change its class.

There are tons of references on line for this pattern. Here are some that seem reasonably good:
+ Wikipedia: https://en.wikipedia.org/wiki/State_pattern
+ GeeksForGeeks: https://www.geeksforgeeks.org/state-design-pattern/
+ Game Programming Patterns: http://gameprogrammingpatterns.com/state.html

The most ubiquitous use of this pattern for PhET is in the quiz-style games found in Build an Atom,
Area Model, Expression Exchange, Area Model, and a number of other sims.  It was also used
extensively to control the behavior of the biomolecules in Gene Expression Essentials.  If you're
in search of examples, these would be good places to start.

The states which a state machine will support should be defined in an Enum.  Here is an example (this
is from the Arithmetic sim, but has been "modernized" to meet our latest standards):
```js
define( require => {
  'use strict';

  // modules
  const arithmetic = require( 'ARITHMETIC/arithmetic' );

  // @public
  const GameState = new Enumeration( [
    'SELECTING_LEVEL',
    'AWAITING_USER_INPUT',
    'DISPLAYING_CORRECT_ANSWER_FEEDBACK',
    'DISPLAYING_INCORRECT_ANSWER_FEEDBACK',
    'SHOWING_LEVEL_COMPLETED_DIALOG',
    'LEVEL_COMPLETED'
  ] );

  arithmetic.register( 'GameState', GameState );

  return GameState;

} );
``` 

There are many different possible ways to implement a state machine in code, and PhET has not
standardized on a single approach.  One method is to use the pattern described in
"Design Patterns: Elements of Reusable Object-Oriented Software", where each state of the
state machine is represented by an instance of an abstract "state" base class, and the
methods defined in this base class specify all of the stimuli that can be received by the
state machine.  A transition from one state to another is done by switching the instance of
of the state from one of these subclasses to another.  This was the approach taken in the Build
an Atom game (and several other game implementations), and the base class for all states can be
seen at [BAAGameState.js] (https://github.com/phetsims/build-an-atom/blob/master/js/game/model/BAAGameState.js).

Another approach is to use a switch statement that switches on the current state, and the code 
under each switch statement handles the incoming event.  This approach hasn't been used much in
PhET code (at least not at the time of this writing), so here is an example that was found on
line at https://24ways.org/2018/state-machines-in-user-interfaces/.

```js
function loginMachine(state, event) {
       switch (state) {
           case 'start':
               if (event === 'SUBMIT') {
                   return 'loading';
               }
               break;
           case 'loading':
               if (event === 'RESOLVE') {
                   return 'success';
               } else if (event === 'REJECT') {
                   return 'error';
               }
               break;
           case 'success':
               // Accept no further events
               break;
           case 'error':
               if (event === 'SUBMIT') {
                   return 'loading';
               }
               break;
           default:
               // This should never occur
               return undefined;
       }
   }
```

Yet another approach is to use a function table, where one axis represents the states and the 
other represents the stimuli or events that can occur.  The benefit of this approach is that
it forces the implementation to explicitly handle all combinations of states and stimuli.
There is an article with an explanation and some good diagrams at https://en.wikipedia.org/wiki/State_transition_table.  
There is a decent stack overflow article that shows an example of that here: 
https://stackoverflow.com/questions/133214/is-there-a-typical-state-machine-implementation-pattern

One of the tricky things about software-based state machines is that it is often difficult for 
someone who is tasked with maintaining the code to understand the big picture of how the state machine operates
based on examination of the source code.  Due to this, it is a strongly recommended practice for PhET
developers that the state machine be documented in diagrammatic form in either a GitHub issue, a JPG or PNG in 
the doc folder, or in the design document.  Also, there are tools such as http://asciiflow.com/ that can be useful for
creating "ascii art" representations of the state diagram.

There are some standard ways to diagram state machine behavior, so when documenting one, please
investigate UML State Diagrams.  A quick search on this turned up [a link that has a pretty good
explanation and some examples](https://www.geeksforgeeks.org/unified-modeling-language-uml-state-diagrams/).

In most cases it will likely be important that state transitions are visible within a PhET-iO
instrumented sim.  For this reason, an Axon Property should generally be used for the state value
so that it can easily be instrumented.  Setting state values via the PhET-iO API is less likely
to be supported, since it would be difficult to make the code able to handle arbitrarily state transitions.
If this were ever done, it would require thorough documentation to describe the valid 
state transitions that can be triggered via this API. 

## Strategy

Author: @jbphet

### Overview

The intent of the "Strategy" design pattern is to define a family of algorithms and encapsulate each one behind a common
interface, and then let clients used them interchangeably to vary some aspect of the clients' behavior. This pattern is
used fairly commonly in PhET code, and a reasonably good explanation can be found at 
https://en.wikipedia.org/wiki/Strategy_pattern.  There are many other decent descriptions on the web, and if you're
thinking of applying this pattern or needing to perform maintenance on an existing implementation of it, it's worth
doing some searching and reading.

In UML diagrams, the strategy pattern is usually depicted as an abstract base class or interface with multiple concrete
subclasses.  Here are a couple of examples that were live at this time of this writing:
+ https://upload.wikimedia.org/wikipedia/commons/3/39/Strategy_Pattern_in_UML.png 
+ https://cdncontribute.geeksforgeeks.org/wp-content/uploads/classinh.jpg
+ https://www.tutorialspoint.com/design_pattern/images/strategy_pattern_uml_diagram.jpg

### When to Use

This pattern is useful in situations where the behavior of an object needs to change at run time based on state
information and there is some benefit in encapsulating that behavior.  If the state information is limited and there
are not many variations in behavior, a simple `if` statement will often suffice (and is generally easier to read), for
example:
```js
step( dt ){
  if ( this.isAboveWater ){
    this.fall( dt );
  }
  else{
    this.float( dt );
  }
}
```

However, if the state and behaviors start to get more complex, a strategy pattern may help to simplify the code and/or
help to avoid duplication of code where similar behavioral changes are needed in other related classes, for instance:

```js
step( dt ){
  if ( this.isAboveWater ){
    this.fall( dt );
  }
  else if ( this.isBelowWater ) {
    this.floatTowardsSurface( dt );
  }
  else if ( this.onSurface && this.waterModel.isWindy ){
    this.bobOnSurface( dt );
  }
  else{
    this.sitCalmlyOnSurface( dt );
  }
}
```

versus:
```js
step( dt ){
  this.waterInteractionStrategy.step( dt );
}
```

In short, here are some rules of thumb for when a strategy pattern might be helpful:
+ there is complex if/switch logic that is being used to decide between different algorithms/behavior
+ there is duplication of conditional logic (especially when slightly altered) in a number of related classes/types that
is being used to implement different behavior
+ there are states in a state machine that are logically similar but have different behaviors

It should be noted that, because functions JavaScript are first-class object (meaning that they can be treated as 
objects), this pattern could be implemented using only functions if the strategy objects do not need to maintain
internal state.  

### Examples in PhET Code

One of the most effective ways to learn a pattern is to study examples of its usage.  One PhET simulation that makes
extensive use of the strategy pattern is Gene Expression Essentials.  This simulation depicts the basic process of
DNA transcriptions by showing how various biomolecules interact to transcribe and translate the information encoded in
DNA molecules into proteins needed by the cells.  The strategy pattern was used in several places in this sim, but the
most extensive use was for controlling how the biomolecules moved.  In some cases, biomolecules need to move around 
randomly. In other situations, they need to move directly to a particular location.  In other cases, biomolecules need
to appear that they are moving somewhat randomly while ultimately arriving at a destination.  This was accomplished by
having the biomolecules use a set of "motion strategies" that were switched when the motion behavior of the biomolecule
needed to change.

In this case, there is an abstract base class called `MotionStrategy` (in Java, this would probably be an interface).
A method in this class is intended to be overridden in all subclasses, and its purpose is to determine the next position
of the client element.  The code looks like this:

```js    
/**
 * get the next position given the current position, bounds, and amount of time
 * @param {Vector2} currentPosition
 * @param {Bounds2} bounds - allowed motion bounds of the controlled item, used in detecting whether the item would go
 * outside of the motion bounds.
 * @param {number} dt - delta time
 * @public
 */
getNextPosition: function( currentPosition, bounds, dt ) {
   // figure out the next position
},
```

The various concrete subclasses of the `MotionStrategy` class implement the desired movement behavior, and are switched
into place based on the state of the biomolecule.

Below is a list of some other examples of strategy pattern usage in PhET sims.  This list is not exhaustive.  It
includes the name of the base class for the strategy followed by the name of the simulation in which it is used.

+ `MotionStrategy` (neuron)
+ `FadeStrategy` (neuron)
+ `PhotonAbsorptionStrategy` (molecules-and-light)
+ `VibrationStrategy` (molecules-and-light)

## Trait

see [Mixin and Trait](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#mixin-and-trait)

