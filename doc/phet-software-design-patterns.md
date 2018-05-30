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

vs `{string[]}`, `Object.freeze`

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
TODO: explain propagation to supertype (filtering), 

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


## Prototypal Inheritance

what it is, why it's needed, use of `call` and `inherit`, use with Mixin and Trait

## Trait

vs Mixin
