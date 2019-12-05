

## Design Patterns for Accessibility

This document describes software design patterns that are specific to adding and implementing accessibility features to 
PhET Sims. 

Common sections for each pattern:
- when to use
- pitfalls
- best practices

### Alerts

#### Alerting a freely movable object
  For example book in Friction, magnet in Faraday's Law, or balloon in BASE.
  
  * Make sure that the object has the "application" aria role
  * Alert updates/position on the end drag call of the listener for the object. Implementing your own alerts based on 
  the `keyup`/`keydown` can work, but will likely emit too many events to UtteranceQueue. Furthermore, alerting based on
  the model when you know that user input is occurring will not alert, since most screen readers won't alert while a user
  has keys pressed.
  

### Naming Types

#### `*Describer.js`

Dynamic descriptions require a large amount of string formation based on model state. In general housing that logic
in a `*Describer.js` type is helpful and idiomatic, where `*` is the purpose this particular describer has. Try not to 
make a single general describer that has too much responsibility, for example `MolarityDescriber` in https://github.com/phetsims/molarity/issues/79

Although describers don't need to be the only place where `StringUtils.fillIn` is used for accessible descriptions, 
they can cover the majority of the usages, as well as keeping track of the model and custom state needed to create these
descriptions.

#### `*DescriptionNode.js`

When a Node is created who's sole purpose is to provide descriptions to the PDOM, then suffix that node with 
`DescriptionNode.js`. For example, see `MolarityBeakerDescriptionNode.js`.

#### `*AlertManager.js`

In some sims it makes sense to have a single file to in do most or all of the interfacing with `utteranceQueue`.
While it is not required to only call utteranceQueue from a single place, it can be a nice organizational tool for the 
interactive descriptions outfitting toolbox. For example `MolarityAlertManager` is the sole alerting file in the sim.