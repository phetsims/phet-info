# PhET Software Design Patterns

This document describes software design patterns that are specific to PhET, and PhET-specific applications
of standard design patterns.

Common sections for each pattern:
- when to use
- pitfalls
- examples

## Creator

describe the problem, event forwarding, model/view creation, instance management

See implementations discussed in https://github.com/phetsims/scenery-phet/issues/214

Interested developers: MK, DB, JO, JB, SR, CK, MB

## Dependency Injection

A standard pattern described in https://en.wikipedia.org/wiki/Dependency_injection.

SR was an advocate of this in https://github.com/phetsims/tasks/issues/952. Clarify which form of dependency injection (probably constructor-based injection), and some examples of where it's currently used in PhET sims.

## Dispose

Disposal is the process of freeing up memory so that it can be garbage collected. In javascript disposal can be trickier
than in other languages because it isn't as explicit. A type needs to be disposed if it has any references to undisposed 
code outside of its type. For example you need to dispose if you add a listener to an `Emitter` that was passed into 
the constructor. You do not need to dispose if a type only effects that type and its children, because it is 
self contained and can be garbage collected as a whole. For more information about the general pattern, see https://en.wikipedia.org/wiki/Dispose_pattern

[Here](https://github.com/phetsims/sun/issues/121#issuecomment-209141994) is a 
helpful list of actions that likely need doing while disposing:
  1. remove observers from things (Property, Emitter, Events) that were provided by the client
  2. dispose of any subcomponents that require disposal
  3. de-register from tandem (data collection)

Once establishing that you need to dispose a type, add the `dispose` method to the prototype. This method should be 
`@public` is likely an `@override`. The `dispose` method on the prototype, when called, should completely
release this object from any references that would otherwise keep it from being garbage collected. Make sure that this
method calls its parent and mixin disposals as well. In the view a type will likely extend from `{{Node}}` and, as such, 
you will call `Node.prototype.dispose.call( this );` (for es5). We call "this" type's dispose before the parent's call 
because we tear down code in the opposite order of construction. 

----------

The preferred approach in implementing disposal for PhET code is to create a private member function in the constructor 
called `this.dispose{{TypeName}}` (see [issue](https://github.com/phetsims/tasks/issues/727)), and then to call that 
from the `dispose` method. With disposal order in mind, the 
safest order of disposal within `this.dispose` is to call `this.dispose{{TypeName}}` before calling for the parent. Within
`this.dispose{{TypeName}}`, the safes order of disposal is the opposite order of component creation.

Take the following type:

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

Note that the `Property` is unlinked before the child is removed from the `Node`.

----------

If performance is an important consideration for a type, then the above pattern can be adapted, and the 
constructor closure removed. Instead promote any local vars that would be needed for disposal to `@private` 
instance fields and move that logic to the `dispose`, like below.

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

Sometimes the above preferred patterns won't work. For example sometimes things are conditionally created, and 
therefore are only conditionally disposed. If there are these sorts of complex disposal constraints, then create an 
emitter to manage disposal tasks, and add a listener to the emitter for each disposal task. Here is a list to follow:

* Name the emitter like `disposeEmitter{{TypeName}}`
* Add listeners to the emitter, recognizing that disposal should usually happen in reverse order of construction
* In the `dispose` method, emit the dispose emitter, and call the parent dispose (`super.dispose()`) in the appropriate 
order.

See [issue](https://github.com/phetsims/axon/issues/214) for details on the "dispose emitter" pattern.

----------

A deprecated pattern once used for disposal involves creating an array to keep track of items to dispose. Often this 
array is called `disposeActions`, and is of type `{Array.<function>}`. For example see use of `this.disposeActions` 
[here](https://github.com/phetsims/circuit-construction-kit-common/blob/91d44b050d79627bf0d470e3b2f1029976e6e004/js/view/CircuitElementNode.js#L71)

Here are some issues that have investigated trying to bring creation and disposal closer together:
* https://github.com/phetsims/axon/issues/84
* https://github.com/phetsims/axon/issues/93

## Enumerations

This is a standard pattern described in https://en.wikipedia.org/wiki/Enumerated_type.

PhET’s preferred implementation of this pattern can be found in [Enumeration.js](https://github.com/phetsims/phet-core/blob/master/js/Enumeration.js).  Examples and coding conventions are in the comment header of that file.  See the wave-interference repository for exemplars of Enumeration use.  Rich enumerations are not currently supported, but may be supported in the future (see https://github.com/phetsims/phet-core/issues/50).

You’ll find a couple of other patterns commonly used in PhET code. These are good to know, but should be avoided in new code.

(1) A set of string values.  For example, [Slider.js](https://github.com/phetsims/sun/blob/master/js/Slider.js) uses `’horizontal’` and `’vertical’` as the values for its `orientation` option. This approach results in the duplication of string literals throughout the code.

(2) Idiomatic JavaScript implementation, as described in [StackOverflow](https://stackoverflow.com/questions/287903/what-is-the-preferred-syntax-for-defining-enums-in-javascript).  The typical implementation associates named keys with numeric values. PhET’s implementation uses string values (to facilitate debugging) and `Object.freeze`  to prevent unintentional modification. See for example [SolutionType.js](https://github.com/phetsims/acid-base-solutions/blob/master/js/common/enum/SolutionType.js).

## Mixins & Traits

Descriptions for each standard pattern can be found here:
  - Mixin: https://en.wikipedia.org/wiki/Mixin
  - Trait: https://en.wikipedia.org/wiki/Trait_(computer_programming)

More information about traits can be found here: http://scg.unibe.ch/archive/papers/Scha03aTraits.pdf

Notes on PhET's decisions regarding mixin vs trait can be found here: https://github.com/phetsims/scenery/issues/700

Summarizing the above, traits and mixins are similar in that both allow code injection and reuise for a class without requiring inheritance. The difference between mixin/trait and inheritance is that a class can receive all the methods and features of the mixin/trait without the semantics of "being a kind of" the mixin/trait.

PhET's definition of mixin and trait does not perfectly align with standard definitions. By standard definition, the differences are:
  - A trait requires methods from the class it is mixed into, a mixin doesn't.
  - A trait can be composed by combining existing traits, a mixin can't.
  - A trait can't specify or access state variables, a mixin can.

PhET defines the difference between mixin and trait as:
  - A trait can require methods and properties from the class it is mixed into, a mixin cannot.

An example of PhET mixin is phet-core/Poolable. An example of a PhET trait is scenery/Paintable.

Creating and using mixins and traits will look similar. Both will have
  - A `mixInto` method that is called on the class using the mixin/trait.
  - An `initialize{{Name}}` method that will be called in the constructor of the class using the mixin/trait.
  - The class using the mixin/trait will have `@mixes {{Name}}` annotation at the constructor.

The only difference is traits should have assertions in the `mixInto` method to verify the class and requirements.

<details><summary>Trait Example</summary>
  
```js
// the trait to be mixed into a class
const MyTrait = {

  /**
   * Adds MyTrait methods to the prototype.
   * @param {SuperClass} myClass
   */
  mixInto: myClass => {
    assert && assert( _.includes( inheritance( myClass ), SuperClass ), 'Only SuperClass classes should mix MyTrait' );

    extend( myClass.prototype, {

      /**
       * This should be called in the constructor of a SuperClass.
       */
      initializeSomeTrait: () => {},

      //...
    } );
  }
}

// the class mixing in the trait
class MyClass extends SuperClass {

  /**
   * @mixes SomeTrait
   */
  constructor() {
    super();

    // to initialize features of the trait
    this.initializeSomeTrait();
  }
}

// to mix SomeTrait methods into the prototype
SomeTrait.mixInto( MyClass );
```
</details>

Questions for the discussion on 2/4/19:
  - Poolable is our only usage of a mixin, but it is described as a trait. Should it be changed to a mixin?
  - Do we need the above code example, or are references sufficient?
  - This example is in es6, none of our traits/mixins use es6.

Interested developers: CM, CK, JG, MK, MB, DB
JG volunteered to do this one for 2/4/19.

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
NOTE: when this gets flushed out, scenery input system, options callbacks should be passed the SCENERY/Event from their input listeners.

Very important pattern for new developers


## `options` and `config` Parameters

TODO This section needs some work. The pattern is probably "configurtion" for parameterizing types, which we use to avoid an explosion of constructor parameters. `config` and `options` are the two implementation of that pattern that PhET typically uses.

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

