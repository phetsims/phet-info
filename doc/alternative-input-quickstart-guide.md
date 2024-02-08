# Alternative Input - Quickstart Guide

@author Chris Malley (PixelZoom, Inc.)

Get started with adding alternative input to your PhET simulation.

## package.json

Follow these steps to add support for alternative input to a simulation.

1. In your sim's package.json, add `"supportsInteractiveDescription": true` to the `phet.supportsInteractiveDescription`
   section, like this:

```
{
   ...
   "phet": {
      "simFeatures": {
         "supportsInteractiveDescription": true,
         ...
      }
   },
   ...
}
```

2. In your sim's repository, run `grunt update`. This will generate `{{REPO}}_a11y_view.html` and
   modify `{{REPO}}_en.html`.

3. Adding `"supportsInteractiveDescription": true` will by default also enable Interactive Highlights.
   See https://github.com/phetsims/phet-info/blob/main/doc/interactive-highlights-quickstart-guide.md for more
   information about this feature.

4. Sims that support alternative input also need an accessible Preferences dialog. See
   https://github.com/phetsims/phet-info/blob/main/doc/accessible-preferences-quickstart-guide.md for information about
   this.

## Make a Node focusable

Most common code UI components are already focusable. But you can make any Node focusable by using these options from
ParallelDOM.ts.

```js
const myNode = new Node( {
  tagName: 'div', // creates representation in the parallel DOM
  focusable: true // makes this Node focusable
} );
```

## Traversal Order

Traversal order is the order in which Nodes are visited as you press the Tab key. Nodes are also categorized into "Play
Area" and "Control Area", which are two sections of the Parallel DOM. This categorization makes them easy to find
when using an assistive device.

The first step is to design the traversal order and categorization. Consult with the simulation designer to determine
the order and placement of components in your simulation. When ready, order and placement are set with the `pdomOrder`
option to Node.

If `pdomOrder` is not specified, the default is the order in which children are added to a Node.

For `FlowBox` (and its subclasses) there is no need to specify traversal order. There is a good match between layout
order and traversal order; they are typically the same. So for `FlowBox`, you can do nothing.

For non-`FlowBox` classes, it is recommended to explicitly set `this.pdomOrder` at the end of constructor. Do not rely
on the default ordering - it’s better to decouple rendering order and traversal order by explicitly setting
`this.pdomOrder`. Note that most of the work here is typically in `ScreenView` subclasses.

If you need to remove a Node from the traversal order you can do so with the `focusable` option of Node.

Use this pattern in your ScreenView constructor:

```js
this.children = [ ... ]; // add children like normal

// Put components in the Play Area and Control Area in order, and decouple traversal order from rendering order
this.pdomPlayAreaNode.pdomOrder = [ ... ];
this.pdomControlAreaNode.pdomOrder = [ ... ];
```

See `ParallelDOM.setPDOMOrder` for more advanced features of this setter if needed.

Potential gotchas:

* `ParallelDOM.setPDOMOrder` has some interesting quirks, so be sure to read the documentation closely. Of special
  interest is the behavior of `null` in the pdomOrder, and what happens to any focuable Nodes that are not explicitly
  included when setting pdomOrder.
* If you need to augment `this.pdomOrder` in a subclass, read about the pitfalls
  in https://github.com/phetsims/scenery/issues/1308.

## Keyboard listeners

If you have a custom Node that needs to do something when Space or Return keys are pressed, add `tagName: 'button'` to
your Node's options, then use one of these approaches:

```js
this.addInputListener( new PressListener( {
  press: () => { ... }
} ) );

this.addInputListener( {
  click: () => { ... }
} );
```

## Drag using the KeyboardDragListener

`DragListener` does NOT handle keyboard input. For Nodes where you’ve added a `DragListener`, you’ll need to add a
corresponding `KeyboardDragListener`. The options for your `DragListener` and `KeyboardDragListener` will typically be
similar, but beware that API differences exist. Avoid duplicating code - factor out any logic that is needed by
both `DragListener` and `KeyboardDragListener`.

Your `KeyboardDragListener` will look something like this:

```js
// pdom - dragging using the keyboard
const keyboardDragListener = new KeyboardDragListener( {
  positionProperty: widget.positionProperty,
  dragBoundsProperty: dragBoundsProperty,
  transform: modelViewTransform,
  dragVelocity: 100, // velocity - change in position per second
  shiftDragVelocity: 20 // finer-grained
} );
```

You’ll also need to add these options to your Node:

```js
// pdom options
tagName: 'div', 
focusable: true
```

## Drag using AccessibleSlider for 1D Motion

If your draggable component moves in 1 dimension consider using AccessibleSlider. AccessibleSlider is a trait that can
be mixed into a Node to add 1D motion with alternative input. AccessibleSlider will make the component much more
accessible for a screen reader user compared to KeyboardDragListener. It is very easy to use when there is a
NumberProperty driving the position. Here is an example:

```js
type SelfOptions = EmptySelfOptions;
type ParentOptions = AccessibleSliderOptions & NodeOptions;

class MyDraggable extends AccessibleSlider( Node, 0 ) {
    public constructor( altitudeProperty: TProperty<number> ) {
      const options = optionize<ParentOptions>()( {
        valueProperty: altitudeProperty,
        enabledRangeProperty: new Property( ALTITUDE_RANGE )
      }, providedOptions );
    
      super( options );
    
      // Now use altitudeProperty to position the Node
      altitudeProperty.link( altitude => {
        this.centerY = altitude;
      } );
    }
  } 
}
```

AccessibleSlider will support movement with arrow keys, as well as other keys such as home/end to quickly move the
component to the limits of the range. See AccessibleSlider and its supertype AccessibleValueHandler for more options and
functionality.

## Hotkeys

If your Node has a `KeyboardDragListener`, add hotkeys like this:

```js
const keyboardDragListener = new KeyboardDragListener( ... );
keyboardDragListener.hotkeys = [
  // Escape
  {
    keys: [ KeyboardUtils.KEY_ESCAPE ],
    callback: () => { ... }
  },
  
  // J+O
  {
    keys: [ KeyboardUtils.KEY_J, KeyboardUtils.KEY_O ],
    callback: () => { ... }
  }
];
```

If your Node does not have a `KeyboardDragListener`, add hotkeys with `KeyboardListener` like this:

```js

const keyboardListener = new KeyboardListener( {
  keys: [ 'escape', 'j+0' ],
  callback: ( event, keysPressed, listener ) => {
    if ( keysPressed === 'escape' ) {
      // escape key was pressed
    }
    else if ( keysPressed === 'j+0' ) {
      // j and 0 were pressed
    }
  },
  
  // By making this listener "global" it will fire no matter where focus is in the document as long as
  // myNode is visible and has input enabled. If this is false, callback will only fire when myNode has keyboard focus.
  global: true
} );

myNode.addInputListener( keyboardListener );
```

Be careful not to add hotkeys that collide with other global hotkeys defined by PhET such as hotkeys that pan and zoom
into the sim. We need a list of global hotkeys or a way to automatically prevent collisions but do not have that yet.
See https://github.com/phetsims/phet-info/issues/188.

## Scenery Events

For more custom behavior you can add input listeners with Scenery's input system that are related to alternative input.
For example, if you want to add behavior whenever a Node has focus you can add a listener like this:

```js
myNode.addInputListener( {
  focus: ( event: SceneryEvent ) => {
    console.log( 'Hey, I have focus!' );
  }
} );
```

See scenery/js/input/Input.js top level documentation for a list of all related alternative input events.

## Focus Highlights

By default, a focus highlight will surround the bounds of your Node. You can customize the highlight with a setter from
ParallelDOM.ts called `setFocusHighlight`. Try to use the default highlight or `HighlightFromNode.ts` for custom
highlights. If you must use something more custom, it will be your responsibility to

1) Style and scale the highlight correctly.
2) Reposition the highlight if the your focused Node moves.

## Pan and Zoom

Scenery will pan to put the focused Node in the center of the viewport when focus changes and when the focused Node
moves. Try to make your focused Node the logical interactive display object. For example, if you have a draggable
component that is a child of a larger Node, make the draggable component the focused Node so that scenery can keep that
Node displayed. If you must do something else, you can use animatedPanZoomSingleton to control the panning. For example:

```js
animatedPanZoomSingleton.listener.panToNode( myNode, false );
```

## Keyboard Shortcuts dialog

The Keyboard Shortcuts dialog is accessed by pressing the keyboard button in the navigation bar. To make this button
appear in the navigation bar, follow steps below to add content to each screen.

Each of your screens is then required to provide content for the dialog, via the
`createKeyboardHelpNode: ()=>{Node}` option to the `Screen` constructor. Instructions for creating this Node are beyond
the scope of this guide. Programming by example is recommended, by searching for "createKeyboardHelpNode". Your content
will typically consist of standard "sections" supported by common code
(e.g. `BasicActionsKeyboardHelpSection`), plus custom sections for sim-specific hotkeys. Consult with your designer
about the content language and layout.

## Pitfalls

* Beware that keyboard navigation does not work by default in Safari. You need to enable traversal in user settings.
  See [this for example](https://www.seanmcp.com/articles/tab-focus-not-working-in-safari/)

## Not supported? Create an issue!

There may be common-code UI components for which alternative input has not been implemented. And there may be PhET
design patterns for which alternative-input behavior has not been designed. Identify lack of alternative-input support,
and create GitHub issues.

## Other Resources

* [Interactive Description Technical Guide](https://github.com/phetsims/phet-info/blob/4839f03214bbba21b4621f80aea8e78a9519fb43/doc/interactive-description-technical-guide.md)
* Description of "Play Area" and "Control
  Area": https://github.com/phetsims/phet-info/blob/main/doc/interactive-description-technical-guide.md#pdom-order-for-phet-sims
