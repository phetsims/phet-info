# PhET Software Design Patterns

This document describes software design patterns that are specific to PhET, and PhET-specific applications
of standard design patterns.

Common sections for each pattern:
- when to use
- pitfalls
- examples

## Dependency Injection

A standard pattern described in https://en.wikipedia.org/wiki/Dependency_injection.

SR was an advocate of this in https://github.com/phetsims/tasks/issues/952. Clarify which form of dependency injection 
(probably constructor-based injection), and some examples of where it's currently used in PhET sims.

## Dispose

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

## Drag Forwarding
(formerly known as the Creator Pattern or Model Element Creator Pattern, or Toolbox) 

TODO: describe the problem, event forwarding, model/view creation, instance management, phet-io, accessibility

Many simulations show a "Toolbox" with "tool" icons which can be dragged into the play area and returned to the toolbox. 
This can be divided into the following steps:
1. Create the icons and display them in the toolbox.
2. Add a listener on the icon.  When pressed, (a) the icon is hidden (b) optionally-a new object is created (in
the model or the view) (c) pointer events are forwarded from the toolbox item to the corresponding view object listener.
If the view object is persistent (such as a ruler), it may need to be moved to the front.  Some simulations may animate
this step.
3. The view object listener has a release listener that checks whether the item should go back into the toolbox.  In 
some simulations, the bounding boxes are checked for intersection.  In some simulations, the center of the dragged 
object must be inside the toolbox.  If the object is dropped into the toolbox, the play area object is disposed or 
hidden, and the icon is shown again.  Some simulations may animate the object going back to the toolbox.  

See implementations discussed in https://github.com/phetsims/scenery-phet/issues/214

Simulations that use SimpleDragHandler.createForwardingListener:
* Capacitor Lab Basics (Voltmeter)
* Circuit Construction Kit (Circuit elements and sensors)
* Equality Explorer (Terms)
* Fluid Pressure and Flow (Sensors)
* Masses and Springs (Ruler and timer)
* Projectile Motion (Tracer and measuring tape)

Simulations that use DragListener.createForwardingListener
* Energy Skate Park (Measuring tape)
* Fractions Suite (Pieces, fraction elements and containers)
* Wave Interference (Tools)

Interested developers: MK, DB, JO, JB, SR*, CK, MB

## Enumerations

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

## Mixins & Traits

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

### When to use Mixin and Trait
In general, composition should be favored over inheritance and inheritance should be favored over mixin. If the composition
pattern produces lots of forwarding calls, it is an indication that you should be using inheritance or mixin instead.
The mixin pattern should only be used as a substitute for multiple inheritance only if single inheritance is not desirable
or is difficult to use.

An example of PhET mixin is phet-core/Poolable. An example of a PhET trait is scenery/Paintable.

Creating and using mixins and traits will look similar. Both will have
  - A `mixInto` method that is called on the class using the mixin/trait.
  - An `initialize{{Name}}` method that will be called in the constructor of the class using the mixin/trait.
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
}

// to mix MyTrait methods into the prototype, after inherit for es5 usages
MyTrait.mixInto( MyClass );
```
</details>

Topics for continued discussion about this:
  - Concrete list of when to use mixin/trait vs inheritance
  - Pattern for using dispose with mixin/trait.
  - How to guard against shadowing (https://github.com/phetsims/phet-core/issues/54)

## Composition and Inheritance
  - Noted as a new topic during patterns discussion on 2/11/19.
  - Would be good to note PhET decisions and patterns for this here.
  - Relavant info/links:
    - https://en.wikipedia.org/wiki/Composition_over_inheritance
      - "Composition over inheritance (or composite reuse principle) in object-oriented programming (OOP) is the principle that classes should achieve polymorphic behavior and code reuse by their composition (by containing instances of other classes that implement the desired functionality) rather than inheritance from a base or parent class."
    - Chrome's optimization makes it so that sims would be faster if we used composition over inheritance.
    - Composition is generally more flexible.

## Model-View Controller

A standard pattern described in https://en.wikipedia.org/wiki/Model–view–controller

`Screen`, `ScreenView`, model container, `Property`, `Emitter`, `Nodes`

Most important pattern for new developers

## Model-View Transform

role in MVC, examples to demystify scenery transform methods (`localToGlobalPoint`, etc.)

## Module

`require` statements and requirejs

## Namespace

why we need it, convention for inner classes

Interested developers: JG, DB, CK

## Observer

A standard pattern described in https://en.wikipedia.org/wiki/Observer_pattern

`Property`, `Emitter`, ... and their role in MVC
NOTE: when this gets fleshed out, scenery input system, options callbacks should be passed the SCENERY/Event from their
input listeners.

Very important pattern for new developers


## `options` and `config` Parameters

TODO This section needs some work. The pattern is probably "configuration" for parameterizing types, which we use to 
avoid an explosion of constructor parameters. `config` and `options` are the two implementation of that pattern that 
PhET typically uses.

Use `_.extend` to overwrite defaults to options for a type like:
```js
  function MyNodeType( options ) {

    options = _.extend( {
      visible: false,
      pickable: false
    }, options );
  }
```
The above `Node` subtype has default `Node` options different from `Node`'s defaults. Fields passed in an 
object titled `options` must all be "optional." If there are some properties of the object parameter that are required,
then the parameter should be called `config`. Some elements of the `config` parameter can be optional, but each one 
must be documented accordingly. 
TODO: document how to document accordingly

We do not filter child options out before passing them up to the parent. With this in mind please be mindful of the option
naming to make sure that you don't cause collisions. See https://github.com/phetsims/tasks/issues/934.

Try to keep related options groups together, both for instantiation and `_.extends` statements. For examples, if you
have several options related to a11y, keep them together, don't interleave them with other options.

### Nesting

If using composition for your type, and you want to pass options into a composed component of the type, you can nest 
those options in a single option on your type, named according to the component you are passing the options to.

```js
  function MyNodeTypeWithHSliderInIt( options ) {

    options = _.extend( {
      visible: false,
      pickable: false,
      
      hsliderOptions: null // filled in below
    }, options );
    
    // default options to be passed into SSlider
    options.hsliderOptions = _.extend( {

      endDrag: function() { console.log( 'Drag Ended') }, 
      startDrag: function() { console.log( 'Drag Started') }
    }, options.hsliderOptions );
  
    var slider = new HSlider( new Property(), new Range(), options.hsliderOptions );
  }
```

In some cases, dependency injection is an appropriate alternative, see https://github.com/phetsims/tasks/issues/952.
In the above example, this would mean creating the HSlider externally then passing it in to the MyNodeTypeWithHSliderInIt
constructor.

### Required fields
If one or more of the fields in `option`s is required, then `options` should be renamed  to `config`. See https://github.com/phetsims/tasks/issues/930
In the `_.extend` call, the options should be commented as to whether they are required or optional.  Following the
`_.extend` call, required fields should have an assertion to verify they were provided. For example:
```js
/**
 * @param {string} name - the full name of the Person
 * @param {Object} config
 * @constructor
 */
function Person( name, config ) {
  config = _.extend( {
    height: null, // {number} @required - height in centimeters
    age: null, // {number} @required - age in years

    favoriteColor: null // {Color|null} optional - favorite color, if any
  }, config );

  assert && assert( config.height !== null, 'height is required' );
  assert && assert( config.age !== null, 'age is required' );
}
```
In some cases, it may be better to only indicate the `required` properties or only indicate the `optional` properties,
or to group them--use your judgment.

## Prototypal Inheritance

what it is, how it differs from `class`, use of `call` and `inherit`, use with Mixin and Trait

e.g. https://medium.com/javascript-scene/master-the-javascript-interview-what-s-the-difference-between-class-prototypal-inheritance-e4cd0a7562e9

## Singleton

A standard pattern described in https://en.wikipedia.org/wiki/Singleton_pattern.

Interested developers: CK, MK, SR, DB

## State Machine

Use in Games, see https://github.com/phetsims/vegas/issues/74

## Traits

see Mixin & Traits

