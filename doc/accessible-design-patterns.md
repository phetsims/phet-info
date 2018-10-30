

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
  

