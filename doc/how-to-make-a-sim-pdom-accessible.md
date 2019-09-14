

# How to Make a Sim PDOM Accessible

## Understand the Goal
  * What features are you trying to implement? The majority of this document (as of this writing) deals with PDOM descriptions.

## Accessibility Basics  

### Web
Assistive technology accesses an [Accessibility Tree](https://developers.google.com/web/fundamentals/accessibility/semantics-builtin/the-accessibility-tree) 
in order to get then information that it can pass along to users of assistive technology. For web pages and web 
applications, the Document Object Model (DOM) is what provides the Accessibility Tree with the information that users need.

In general, PhET tries to use the same best practices as are used in traditional web applications and content.

### Assistive Technology
Assistive technology (or AT) is that tech that allows for users to interact with the PDOM and experience phetsims without
tradition mouse/touch input and visual output. The most common that PhET supports is the screen reader. Screen readers
access the HTML code directly via the "virtual cursor" this can be used to navigate content much quicker than just using
a keyboard to tab navigate.

### More info

For more information, see the "Resources for further understanding" below.

## Understanding the PDOM
The traditional renderings of PhET sims (svg, canvas, webgl) hold very little semantic data as to what is inside the
rendered graphic. They are a single, graphical element in HTML. The PDOM ( parallel DOM (Document Object Model))
pulls semantic data from the `Scenery` scene graph and adds it to a separate HTML structure that is accessible to
assistive technologies. When we say PDOM, think an HTML manifestation of the graphical `Node` content in the phetsim.

This HTML acts as just another output modality to the phet model. You can interact with it to control the simulation, 
and you can get information out of it, as the PDOM is updated in real time in response to changes in the model.

## Overall Code structure
Note: a11y is a synonym for accessibility.

* `Accessibility.js` is a trait that is added to `Node.js`, so `Node` is already set up with a11y specific
options to provide PDOM descriptions.

* The DAG features of the a11y side of Scenery are handled the same way as graphical `Node`s in Scenery. Each `Node` 
with the `Accessibility` trait added to its prototype has N `AccessibleInstance`s based on the number of times it has been added
to the scene graph. The PDOM elements of each `Node` are created and handled with `AccessiblePeer`. There is a 1x1
relationship of `AccessibleInstance` and `AccessiblePeer`.

## Basic Example - adding a11y features to a `Node`
The primary to add a `Node` to the PDOM is through options passed through to `Node.js`. First off, each
`Node` that wants content in the PDOM will need an HTML element in the PDOM to represent it. To do this, use the
`tagName` option:
```js
var a11yNode = new Node( {
  tagName: 'p'
} );
```
The above code snippet will create a node that is a `<p>` tag in the PDOM. To give content to this `<p>`, use the
`innerContent` option.

```js
a11yNode.innerContent = 'I am a p tag in the PDOM!';
```

Just like other Node options, you can pass them into an options object, `mutate` call, and by using getters/setters.
Now the PDOM will look like:
```html
<p>I am a p tag in the PDOM</p>
```

## PDOM Representation for a single Node
Each Node can have more than one `HTMLElement` in the PDOM. Up to four `HTMLElements` can be used as needed to display
the Node appropriately in the PDOM. 
  * The "primary sibling" is controlled via the `tagName` option, and is the main `HTMLElement` for the `Node`. If this 
  `Node` has accessible listeners added to it, this element is where those listeners are added.  
  *  The "label sibling" and "description sibling" are there as siblings to the primary in the PDOM. They are flexible 
  and can be used for any content. In general though, they are named as they are because PhET often has a label and 
  description next to an interactive element. This pattern is seen throughout PhET PDOM code. 
  * Each sibling can only be one `HTMLElement`.
  * The "container" is the fourth element, and can optionally be added to contain all of the siblings.

## Keyboard Navigation

Keyboard navigation is gained by making the primary sibling an interactive `HTMLElement`. Any visible, interactive element
in the PDOM will be tab navigable, and its corresponding `Node` in the sim will highlight. You can toggle the focusability
of a Node with the `focsuable` option.

### Focus Highlight

There are a number of options to alter the focus highlight, see usages in the project of `focusHighlight` option for 
those patterns. You can also set a `groupFocusHighlight` to highlight a container.

### Input Listeners
PDOM input listeners are set up in the same way as general PhET listeners. See `Input.js` for full documentation. 
There are specific events to subscribe to for events from the PDOM. Common code listeners, like `PressListener`, are 
already set up to support events from the PDOM. If implementing a custom listener, you will need to manually support 
the appropriate event (which is different depending on the primary sibling `HTMLElement`). Make sure to work with an 
accessibility designer to ensure that your component is accessible for all desired features. Explaining the many 
difficulties embodied in that warning is beyond the scope of this document. Here is a basic example of how to support 
a custom button with PDOM support.

```js

const myButton = new Node( {  
 tagName: 'button',
 innerContent: 'Press me!' 
} );
this.addChild( myButton);
this.addInputListener( {

    // This is not a mouse click but rather the "click" HTML event coming directly from the button. Firing a button
    // with space or enter will also fire the "click" event on the button.
    click: ()=>{
      console.log( 'This button was clicked from the PDOM' );
    },

    // This is still required for mouse/touch/pen support. 
    down: ()=>{
      console.log( 'This button was clicked' );
    }
});
```

## Descriptions

"Descriptions" is a vague word. For the purposes of this document. It refers to the feature set that provides screen 
 reader support for PhET sims. This includes everything in the PDOM, as well as aria-live alerts via the `UtteranceQueue`.


### Implementing Descriptions
To implement PDOM descriptions, follow these thoughts:
  * When adding options to `Node`, separate accessibility specific options in their own block, labelling them 
  with an `// a11y` comment.
  * Understand [Accessible Name](https://developer.paciellogroup.com/blog/2017/04/what-is-an-accessible-name/)
  The short article above describes very simply and briefly the different ways an element gets an accessible name.
      * element's content: Example `<button>my button</button>`. The inner text within the button's opening and 
      closing tags is the button element's accessible name.
      * `label` element: a `label` element can be associated with an interactive _input type_ (e.g., `input type="checkbox"`) 
      that does not have inner content in order to provide the input with an accessible name. A `label` is preferred naming 
      method when the sim interaction has visible text-based identifying it on screen. A `label` element can only be associated 
      with _labelable elements_ like typical interactive HTML elements 
      [http://w3c.github.io/html/sec-forms.html#labelable-element](http://w3c.github.io/html/sec-forms.html#labelable-element). 
      It cannot, for example, be associated with a `div` with `role="checkbox"`. When a visible text-based label does not exist on screen, 
      other labeling options can be considered. 
      * `aria-label`: is an aria attribute that can provide an accessible name.
      * `aria-labelledby`: aria-labelledby can be used to associate an HTML element other than the label element to another element. 
      The elements do not have to be right beside eachother. In a PhET Sim one might want to associate a heading element with a region or group. 
      For example, an H2 heading is associated with the Play Area region through an `aria-labelledby` attribute. With this association 
      the H2's content, "Play Area", provides the region with an accessible name in the _Accessibility Tree_ which is 
      accessed by assistive technology.
  * This is where you are piecing together all of the individual nodes.
  * For a full list of available options, see `Accessibility.js`. 

### Interactive Alerts
  * `UtteranceQueue` is a type set up to emit live descriptions on demand. This is most often implemented based on model
  changes. For PDOM accessibility, the word "alerts" means aria-live support via `UtteranceQueue`.
  
  ```js
    const utteranceQueue = require( 'SCENERY_PHET/accessibility/utteranceQueue' );
    utteranceQueue.addToBack( 'Speak this now'); // This will immediately sent this string to the screen reader to speak.

    // This is the same as wrapping a string inside an Utterance
    const Utterance = require( 'SCENERY_PHET/accessibility/Utterance' );
    utteranceQueue.addToBack( new Utterance( { alert: 'Speak this now' } ) ); 
  ```
  * A variety of features for advanced use has been built into `Utterance`. For example it is possible to loop through,
  multiple alerts, cycling each time the `Utterance` is emitted. It is also possible to clear out stale usages of the 
  same `Utterance`. For more info see `Utterance`.
  
### Aria Value Text
(aka `aria-valuetext`) is an attribute that is supported by interactive elements (like `input`). This in correlation with 
alerts is how phetsims communicate the majority of their dynamic content. `aria-valuetext` is often preferred
because the attribute is monitored by the assistive technology, and only is read if that interactive element is focused 
or being interacted with. Whereas aria-live alerts are read no matter where the virtual cursor is. 

## Handling a11y specific strings
  * These strings are not YET translatable, but they will be, so please treat usages as similarly to strings of 
  the `strings!` plugin as possible so that it is easier to transfer them over to translatable strings, think means:
    * Name a11y strings without `String` at the end of the key
    * declare all a11y strings at the top of the file (like their own module)
    * have `var`s that end in `String` when declaring strings
    * string keys should hold an object with a "`value`" key that stores the a11y string.
  * Create an `{{SIM}}A11yStrings.js` file.

## In Conclusion

Please discuss questions or problems with @jessegreenberg or @zepumph and update this document accordingly
to help those who follow in your footsteps!

### Resources for further understanding:
* [Screen Reader Support for a Complex Interactive Science Simulation](https://drive.google.com/file/d/0B44Uycdx6JGdRFpXcDJqZl9BUk0/view)
* [Description Strategies to Make an Interactive Science Simulation Accessible
](http://scholarworks.csun.edu/handle/10211.3/190214)


### Happy a11y development!
