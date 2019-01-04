# PhET Software Design Patterns

This document describes software design patterns that are specific to PhET, and PhET-specific applications
of standard design patterns.

Common sections for each pattern:
- when to use
- pitfalls

## Creator

describe the problem, event forwarding, model/view creation, instance management

## Dispose

when to implement `dispose`, use of `this.disposeTypeName`, chaining to supertype `dispose`, typical order of disposal

## Enum

`Enumerator` vs `{string[]}` vs `Object.freeze`

## Mixin

vs Trait

## Model-View Controller

`Screen`, `ScreenView`, model container, `Property`, `Emitter`, Nodes

## Model-View Transform

role in MVC, examples to demystify scenery transform methods (`localToGlobalPoint`, etc.)

## Module

`require` statements and requirejs

## Observable

`Property`, `Emitter`, ... and their role in MVC

## Options and Config Parameters

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

### Required Named Parameters
If one or more of the options are required, then `options` should be renamed  to `config`. See https://github.com/phetsims/tasks/issues/930
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

what it is, why it's needed, use of `call` and `inherit`, use with Mixin and Trait

## Trait

vs Mixin
