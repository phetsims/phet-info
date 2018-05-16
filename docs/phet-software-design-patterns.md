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

## Options

`_.extend`, options vs required parameters, default values, propagation to supertype (filtering), propagation to subcomponents (nesting)

## Prototypal Inheritance

what it is, why it's needed, use of `call` and `inherit`, use with Mixin and Trait

## Trait

vs Mixin
