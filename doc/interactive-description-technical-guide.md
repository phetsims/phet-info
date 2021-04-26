# Interactive Description Technical Guide

### Table Of Contents

* [Prerequisites](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#prerequisites)
    * [Understand the Goal](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#understand-the-goal)
    * [Accessibility Basics](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#accessibility-basics)
    * [Assistive Technology](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#assistive-technology)
* [What does "Interactive Description" mean?](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#what-does-interactive-description-mean)
* [Understanding each technology](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#understanding-each-technology)
    * [Overall Code structure](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#overall-code-structure)
    * [Parallel DOM](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#parallel-dom)
    * [UtteranceQueue](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#utterancequeue)
* [Implementation](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#implementation)
    * [Getting started](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#getting-started)
    * [The a11y-view](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#the-a11y-view)
    * [Populating the PDOM](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#populating-the-pdom)
    * [PDOM Order for PhET Sims](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#pdom-order-for-phet-sims)
    * [Add alternative-input input listeners](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#add-alternative-input-input-listeners)
    * [Implementing Interactive Description](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#implementing-interactive-description)
    * [Interactive Alerts](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#interactive-alerts)
    * [Aria Value Text](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#aria-value-text)
    * [Handling a11y specific strings](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#handling-a11y-specific-strings)
    * [Naming Types](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#naming-types)
    * [Other misc notes for PhET Devs](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#other-misc-notes-for-phet-devs)
* [In Conclusion](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#in-conclusion)
* [Resources for further understanding](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#resources-for-further-understanding)

## Prerequisites

* Before reading this documentation, please see scenery's accessibility-related documention
  at `/scenery/doc/accessibility.html`. This includes an overview of web accessibility key features required for
  Interactive Description implementation.
* Note: "a11y" is a synonym for "accessibility".

### Understand the Goal

What features are you trying to implement? The majority of this document (as of this writing) deals with Interactive
Description, but there are many other accessibility-related features that are supported by phetsims like sound,
sonification, pan and zoom, voicing, and interactive highlights.

### Accessibility Basics

In general, PhET tries to use the same best practices as are used in traditional web applications and content.

### Assistive Technology

Assistive technology (or AT) is that tech that allows for users to interact with the PDOM and experience phetsims
without tradition mouse/touch input and visual output. The most common that PhET supports is the screen reader. Screen
readers access the HTML code directly via the "virtual cursor" this can be used to navigate content much quicker than
just using a keyboard to tab navigate.

### More info

For more information, see the "Resources for further understanding" below.

## What does "Interactive Description" mean?

Interactive Description is an accessibility feature that PhET has developed, largely tailored towards screen reader
accessibility. It has the following components (with their implementation in parens):

* State Description (PDOM)
    * Static States
    * Dynamic States
* Responsive Description
    * Object Responses (UtteranceQueue/PDOM/Both)
    * Context Responses (UtteranceQueue)
* Alternative Input:
    * keyboard (PDOM)
    * mobile (PDOM)
    * switch (PDOM)

## Understanding each technology

### Overall Code structure

* `ParallelDOM.js` is a trait that is added to `Node.js`, so `Node` is already set up with pdom-specific options to
  provide Interactive Description.

* The implementation and DAG features of the PDOM-side of scenery are handled the same way as graphical `Node`s in
  Scenery. Each `Node`  with the `ParallelDOM` trait added to its prototype has N `PDOMInstance`s based on the number of
  times it has been added to the scene graph. The PDOM elements of each `Node` are created and handled with `PDOMPeer`.
  There is a 1x1 relationship of `PDOMInstance` and `PDOMPeer`.

For more information please see `/scenery/doc/accessibility.html'`.

### Parallel DOM

The traditional renderings of PhET sims (svg, canvas, webgl) hold very little semantic data as to what is inside the
rendered graphic. They are a single, graphical element in HTML. The PDOM ( parallel DOM (Document Object Model))
pulls semantic data from the `Scenery` scene graph and adds it to a separate HTML structure that is accessible to
assistive technologies. When we say PDOM, think an HTML manifestation of the graphical `Node` content in the phetsim.

This HTML acts as just another output modality to the phet model. You can interact with it to control the simulation,
and you can get information out of it, as the PDOM is updated in real time in response to changes in the model.

### UtteranceQueue

The "Interactive" portion of "Interactive Description" is largely centered around `aria-live`. This feature of web
accessibility allows a webpage to "push" an "alert" (eager description) to a screen reader to be read immediately. There
are two types of aria-live alerts: "polite" and "assertive". Assertive will interrupt whatever is being said by the
screen reader currently. Most alerts (and the default) in the project are polite.

Every `Display` has an `UtteranceuQueue` instance that is wired to alert to aria-live elements for screen readers.
`UtteranceQueue` takes `Utterance` instances and queues them in standard ways that the accessibility team has found
works well across our supported browsers and screen readers.

In general, the way that interactive alerts work in PhET sims is like so:

```js
const massUtterance = new Utterance();

// somewhere else, like in an input listener
massUtterance.alert = getMassChangedResponse();
phet.joist.sim.utteranceQueue.addToBack( this.massUtterance )
```

There are a variety of options in `Utterance` used to hone the output of alerts. Common problems include a build up of
too many alerts, and alerts that occur with too much or too little time between it and the interaction.

## Implementation

### Getting started

When beginning PDOM work in a simulation, add `"supportsInteractiveDescription": true` to the sim's package.json under
`phet.features`. Then regenerate the lists to add the simulation to perennial/data/interactive-description list, and
generate an a11y-view HTML document to assist with development (`grunt generate-a11y-view-html`). Accessibility features
are hidden behind an `?supportsDescription` query parameter. You can elect to develop by adding this query parameter,
but it is not recommended.

### The a11y-view

The 'A11y view' is an HTML page that runs the simulation in an iframe and shows an up-to-date copy of the PDOM next to
the sim. It can be used to assist in development of accessibility features by allowing you to see the accessible labels,
descriptions, and alerts without requiring screen reader testing. This should be generated by Bayes, but it can be
generated manually with `grunt generate-a11y-view-html` in the sim repo.

### Populating the PDOM

The first thing to do is to create the PDOM content for the simulation. This are often referred to as "state
description". In general, the process looks like this:

* Understand the design for your work
* Determine where visual objects can map directly to elements in the PDOM, and provide options to them. Otherwise, you
  will need to create different Node structure to satisfy the design of the PDOM.
* Passing `tagName` will add them to the PDOM, but use all ParallelDOM options to create the structure needed. The
  options to be used most often will be `accessibleName`, and `helpText`, as almost all interactive components will have
  these. See notes below about setting accessibleName
* Make sure that the keyboard navigation order is correct for interactive elements
* Note: at this time, there is no support for automatically setting heading levels within Node structure, but if this
  would be valuable to you, please let the Interactive Description feature leads (@jessegreenberg and @zepumph) know,
  and note in https://github.com/phetsims/scenery/issues/855.

### PDOM Order for PhET Sims

PhET's design for the Parallel DOM is largely based on each screen. Within each screen, there is a _Screen Summary_,
_Play Area_, and _Control Area_. `ScreenView` has pdom "section" Nodes built into the type. Use children or `pdomOrder`
to set PDOM content into the designed sections associated with the PDOM. For example, if you had a Node that was
entirely PDOM content, and no visual content, you could add that directly to the Play Area as a child:

```js
// in a sim's ScreenView. . . 
const aNodeInThePlayArea = new Node( {
  tagName: 'p',
  innerContent: 'This is a part of the playArea'
} );
this.playAreaNode.addChild( aNodeInThePlayArea );
```

NOTE: Nodes must be connected to the scene graph for `pdomOrder` to work. Thus `pdomOrder` cannot be used in exchange
for setting a Node as a child, but can be used in addition.

Rendering priorities in the PDOM can differ from those displayed in the visual simulation. We use `Node.pdomOrder` to
help manage this discrepancy. As a PhET Developer, please use the following guide to develop the PDOM ordering in the
PDOM versus the traditional rendering order of the scene graph. Each item in the list is ranked, such that you should
start with item 1, and then if that doesn't work for your situation, try the next item down.

NOTE: This list was created with a mindset of instrumenting a simulation with Interacitve Description. If a new sim is
being created, then likely this list is irrelevant because the design process from the beginning will be focused on this
feature and visual sim development together.

1. Add alternative input to the simulation, see if order is correct based on the scene graph structure. If not. . .
2. use `setPDOMOrder` on local children, if not. . .
3. Change z-order in the scene graph structure to get the order correct, if there is not an overriding constraint from
   the visible rendering order, if not. . .
4. Discuss with the design team to inform them the order is unnatural OR we may decide another order based on
   simplifying implementation--revise desired order. if not. . .
5. use `setPDOMOrder` on descendants (can be local vars like `controlPanel.flashlight.button.label`). This is not
   recommended.

If `setPDOMOrder` is needed on Nodes that are not descendants, then likely there is a structural issue that needs to be
addressed fully, rather than hacked at by using `Node.setPDOMOrder`, although the setter will accept any `Node` in the
scene graph.

Please see `Node.setPDOMOrder` for more documentation and usage examples of `pdomOrder`.

### Add alternative-input input listeners

This step builds out input functionality to support alternative input. Many common code components already have this
support. For sim specific components, work with your designer to design the best keyboard interaction possible. Note
that this will not always map directly to the mouse/touch interaction.

PDOM input listeners are set up in the same way as general PhET listeners. See `Input.js` for full documentation. There
are specific events to subscribe to for events from the PDOM. Common code listeners, like `PressListener`, are already
set up to support events from the PDOM. If implementing a custom listener, you will need to manually support the
appropriate event (which is different depending on the primary sibling `HTMLElement`). Make sure to work with an
accessibility designer to ensure that your component is accessible for all desired features. Explaining the many
difficulties embodied in that warning is beyond the scope of this document. Here is a basic example of how to support a
custom button with PDOM support.

```js

const myButton = new Node( {
  tagName: 'button',
  innerContent: 'Press me!'
} );
this.addChild( myButton );
this.addInputListener( {

  // This is not a mouse click but rather the "click" HTML event coming directly from the button. Firing a button
  // with space or enter will also fire the "click" event on the button.
  click: () => {
    console.log( 'This button was clicked from the PDOM' );
  },

  // This is still required for mouse/touch/pen support.
  down: () => {
    console.log( 'This button was clicked' );
  }
} );
```

Also see `GrabDragInteraction.js` and `KeyboardDragListener.js` for common code keyboard-interaction input listeners.

### Implementing Interactive Description

To implement interactive description, follow these thoughts:

* When adding options to `Node`, separate pdom-specific options in their own block, labelling them with a `// pdom`
  comment.
* Understand [Accessible Name](https://developer.paciellogroup.com/blog/2017/04/what-is-an-accessible-name/)
  The short article above describes very simply and briefly the different ways an element gets an accessible name.
    * element's content: Example `<button>my button</button>`. The inner text within the button's opening and closing
      tags is the button element's accessible name.
    * `label` element: a `label` element can be associated with an interactive _input type_ (
      e.g., `input type="checkbox"`)
      that does not have inner content in order to provide the input with an accessible name. A `label` is preferred
      naming method when the sim interaction has visible text-based identifying it on screen. A `label` element can only
      be associated with _labelable elements_ like typical interactive HTML elements
      [http://w3c.github.io/html/sec-forms.html#labelable-element](http://w3c.github.io/html/sec-forms.html#labelable-element)
      . It cannot, for example, be associated with a `div` with `role="checkbox"`. When a visible text-based label does
      not exist on screen, other labeling options can be considered.
    * `aria-label`: is an aria attribute that can provide an accessible name.
    * `aria-labelledby`: aria-labelledby can be used to associate an HTML element other than the label element to
      another element. The elements do not have to be right beside eachother. In a PhET Sim one might want to associate
      a heading element with a region or group. For example, an H2 heading is associated with the Play Area region
      through an `aria-labelledby` attribute. With this association the H2's content, "Play Area", provides the region
      with an accessible name in the _Accessibility Tree_ which is accessed by assistive technology.
* This is where you are piecing together all of the individual nodes.
* For a full list of available options, see `ParallelDOM.js`.

### Interactive Alerts

* `UtteranceQueue` is a type set up to emit live event based descriptions. This is most often implemented based on model
  changes. For PDOM accessibility, the word "alerts" means aria-live support via `UtteranceQueue`.

    ```js
    import utteranceQueue from '../../utterance-queue/js/utteranceQueue.js';
    
    utteranceQueue.addToBack( 'Speak this now' ); // This will immediately sent this string to the screen reader to speak.
    
    // This is the same as wrapping a string inside an Utterance
    import Utterance from '../../utterance-queue/js/Utterance.js';
    
    utteranceQueue.addToBack( new Utterance( { alert: 'Speak this now' } ) );
    ```

* A variety of features for advanced use has been built into `Utterance`. For example it is possible to loop through,
  multiple alerts, cycling each time the `Utterance` is emitted. It is also possible to clear out stale usages of the
  same `Utterance`. For more info see `Utterance`.

#### Alerting a freely movable object

For example book in Friction, magnet in Faraday's Law, or balloon in BASE.

* Make sure that the object has the "application" aria role
* Alert updates/position on the end drag call of the listener for the object. Implementing your own alerts based on
  the `keyup`/`keydown` can work, but will likely emit too many events to UtteranceQueue. Furthermore, alerting based on
  the model when you know that user input is occurring will not alert, since most screen readers won't alert while a
  user has keys pressed.

### Aria Value Text

(aka `aria-valuetext`) is an attribute that is supported by interactive elements (like `input`). This, in correlation
with alerts, is how phetsims communicate the majority of their dynamic content. `aria-valuetext` is often preferred
because the attribute is monitored by the assistive technology, and only is read if that interactive element is focused
or being interacted with. Whereas aria-live alerts are read no matter where the virtual cursor is.

### Handling a11y specific strings

* These strings are not YET translatable, but they will be. For now make sure that all a11y-related strings are nested
  under the "a11y" object in the `*en.json` string file in your repo. See other sims with that key as examples.

### Naming Types

#### `*Describer.js`

Dynamic descriptions require a large amount of string formation based on model state. In general housing that logic in
a `*Describer.js` type is helpful and idiomatic, where `*` is the purpose this particular describer has. Try not to make
a single general describer that has too much responsibility, for example `MolarityDescriber`
in https://github.com/phetsims/molarity/issues/79

Although describers don't need to be the only place where `StringUtils.fillIn` is used for accessible descriptions, they
can cover the majority of the usages, as well as keeping track of the model and custom state needed to create these
descriptions.

In general, Describer types need a fair bit of information from the model, and sometime the view-state to fill in
description. It is cleanest to pass as much information into the constructor, limiting the number of arguments needed
for individual functions. See https://github.com/phetsims/ratio-and-proportion/issues/334.

#### `*DescriptionNode.js`

When a Node is created who's sole purpose is to provide descriptions to the PDOM, then suffix that node with
`DescriptionNode.js`. For example, see `MolarityBeakerDescriptionNode.js`. There are also cases where this is
called `*PDOMNode.js`.

#### `*AlertManager.js`

In some sims it makes sense to have a single file to in do most or all of the interfacing with `utteranceQueue`. While
it is not required to only call utteranceQueue from a single place, it can be a nice organizational tool for the
interactive description outfitting toolbox. For example `MolarityAlertManager` is the sole alerting file in the sim.

### Other misc notes for PhET Devs

* As a sim developer, it is your responsibility to make sure that each interactive element has an Accessible Name.
* Conventionally, it is preferred to specify PDOM parameters as options whenever possible, and only use the setters if
  the situation requires it. Please label PDOM specific options separately with a `// pdom` comment as a header.
* The HTML of the PDOM acts as just another input/output modality to a PhET sim's model. You can interact with it to
  control the simulation, and you can get information out of it, as the PDOM can be updated in real time in response to
  changes in the simulation.
* About aria-labelledby: In a PhET Sim one might want to associate a heading element with a region or group. For
  example, an H2 heading is associated with the Play Area region through an `aria-labelledby` attribute. With this
  association the H2's content, "Play Area", provides the region with an accessible name in the Accessibility Tree which
  is accessed by assistive technology.

## In Conclusion

Please discuss questions or problems with @jessegreenberg or @zepumph and update this document accordingly to help those
who follow in your footsteps!

### Resources for further understanding:

* [Screen Reader Support for a Complex Interactive Science Simulation](https://drive.google.com/file/d/0B44Uycdx6JGdRFpXcDJqZl9BUk0/view)
* [Description Strategies to Make an Interactive Science Simulation Accessible
  ](http://scholarworks.csun.edu/handle/10211.3/190214)

### Happy a11y development!
