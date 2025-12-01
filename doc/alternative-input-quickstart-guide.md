---
title: Alternative Input - Quickstart Guide
author: Chris Malley (PixelZoom, Inc.)
---

# Alternative Input - Quickstart Guide

Get started with adding alternative input to your PhET simulation.

### Table of Contents

<!--@formatter:off-->
* **[package.json](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#packagejson)**
* **[Make a Node focusable](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#make-a-node-focusable)**
* **[Traversal Order](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#traversal-order)**
* **[Keyboard listeners](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#keyboard-listeners)**
* **[Drag using the KeyboardDragListener](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#drag-using-the-keyboarddraglistener)**
* **[Drag using AccessibleSlider for 1D Motion](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#drag-using-accessibleslider-for-1d-motion)**
* **[Hotkeys](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#hotkeys)**
* **[Scenery Events](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#scenery-events)**
* **[Focus Highlights](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#focus-highlights)**
* **[Pan and Zoom](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#pan-and-zoom)**
* **[Keyboard Shortcuts dialog](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#keyboard-shortcuts-dialog)**
* **[Toolboxes](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#toolboxes)**
* **[Pitfalls](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#pitfalls)**
* **[Not supported? Create an issue!](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#not-supported-create-an-issue)**
* **[Other Resources](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md#other-resources)**

<!--@formatter:on-->

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

## Make a Node focusable

Most common code UI components are already focusable. But you can make any Node focusable by using these options from
ParallelDOM.ts.

```ts
const myNode = new Node( {
  tagName: 'div', // creates representation in the parallel DOM
  focusable: true // makes this Node focusable
} );
```

When you make a custom Node `focusable: true`, you almost always need to use `AccessibleInteractiveOptions` or
`AccessibleDraggableOptions`. These options have important defaults for assistive technology. See
the [Core Description Quickstart Guide](https://github.com/phetsims/phet-info/blob/main/doc/core-description-quick-start-guide.md)
for more information.

## focusable vs accessibleVisible

Use `focusable: false` to pull a Node out of traversal while keeping its description in the Parallel DOM. Assistive tech can still reach it via virtual cursor or group navigation. Example: a draggable that should not take focus during an animation, but still needs to be described when its parent group is explored.

Use `accessibleVisible: false` when the Node’s accessible content should disappear entirely. This removes it from the Parallel DOM, so a screen reader cannot discover it and it will not appear in the a11y view. Example: a control that sits under a modal panel; when the modal opens, hide the underlying control so it isn’t discoverable until the modal closes.

```ts
const colorToolButton = new Node( {
  accessibleVisible: !modalOpenProperty.value
} );
```

## Disabled components

Keep disabled UI in traversal order. Screen readers announce the control and its disabled state, so
users know the feature exists and why it cannot be activated yet. Use `inputEnabled: false` (or `inputEnabledProperty`)
so Scenery adds the proper ARIA attributes automatically. If you cannot use `inputEnabled`, set the attribute directly
with `setPDOMAttribute( 'aria-disabled', false )`. Do not fake disabling by toggling `focusable` or `accessibleVisible`.
See the [Core Description Quickstart Guide](https://github.com/phetsims/phet-info/blob/main/doc/core-description-quick-start-guide.md)
for more information about description.

## Traversal Order

Traversal order (or focus order) is the order in which Nodes are visited as you press the Tab key.

Nodes are categorized as belonging to "Play Area" or "Control Area", which are two sections of the Parallel DOM. This
categorization makes them easy to find when using an assistive device.

### Step 1: Prototype the traversal order.

This can be done in collaboration with the designer, or by the developer as a strawman proposal.

The quickest path to a prototype is to follow the code pattern shown below in your ScreenView subclasses. Multiple calls
to `screenViewRootNode.addChild` are also OK, but will not provide you with a clear specification of rendering order.

```ts
// Rendering order, a single child added to the ScreenView.
const screenViewRootNode = new Node( {
  children: [
    // Put all of your Nodes here.
  ]
} );
this.addChild( screenViewRootNode );

// Traversal order, decoupled from rendering order.
screenViewRootNode.pdomOrder = [ /* ... */ ]; 
```

### Step 2: Categorize Nodes as "Play Area" or "Control Area".

Using the prototype created in Step 1 to inform the design, decide how Nodes should be categorized as either "Play Area"
or "Control Area". If Step 1 was done without the designer, this is the time to involve the designer.

Note that "Play Area" will always appear before "Control Area" in the traversal order.

### Step 3: Implement the traversal order for "Play Area" and "Control Area".

Using the design requirements from Step 2, here is the typical change that you'll make to ScreenView subclasses:

```diff
- // Traversal order, decoupled from rendering order.
- screenViewRootNode.pdomOrder = [...];
+ // Traversal order for the Play Area and Control Area, decoupled from rendering order.
+ this.pdomPlayAreaNode.pdomOrder = [ ... ];
+ this.pdomControlAreaNode.pdomOrder = [ ... ];
```

### Additional notes:

* If `pdomOrder` is not specified, the default is the order in which children are added to a Node.

* For `FlowBox` (and its subclasses) there is no need to specify traversal order. There is a good match between layout
  order and traversal order; they are typically the same. So for `FlowBox`, you can do nothing.

* For non-`FlowBox` classes, it is recommended to explicitly set `this.pdomOrder` at the end of constructor. Do not rely
  on the default ordering - it’s better to decouple rendering order and traversal order by explicitly setting
  `this.pdomOrder`. Note that most of the work here is typically done in `ScreenView` subclasses.

* If you need to remove a Node from the traversal order, you can do so with the `focusable: false` option of Node.

* See `ParallelDOM.setPDOMOrder` for more advanced features of this setter if needed.

Potential gotchas:

* `ParallelDOM.setPDOMOrder` has some interesting quirks, so be sure to read the documentation closely. Of special
  interest is the behavior of `null` in the pdomOrder, and what happens to any focuable Nodes that are not explicitly
  included when setting pdomOrder.
* Only use `this.addChild` for ScreenViews. If you set `this.children`or call `this.setChildren`, you will blow
  away `this.pdomPlayAreaNode` and `this.pdomControlAreaNode`.

## Keyboard listeners

If you have a custom Node that needs to do something when Space or Return keys are pressed, add `tagName: 'button'` to
your Node's options, then use one of these approaches:

```ts
this.addInputListener( new PressListener( {
  press: () => { /*...*/ }
} ) );

this.addInputListener( {
  click: () => { /*...*/ }
} );
```

## Keyboard drag listeners

`DragListener` does NOT handle keyboard input, so you will need to do some additional work for keyboard dragging.

Consider using `scenery-phet/SoundRichDragListener`. It combines a `DragListener` with a `KeyboardDragListener` to support
both mouse and keyboard dragging. It also includes default PhET drag and drop sounds. This is the recommended approach.

If that doesn't work for you, you can use `KeyboardDragListener` directly. The options for your `DragListener`
and `KeyboardDragListener` will typically be similar, but beware that API differences exist. Avoid duplicating
code - factor out any logic that is needed by both `DragListener` and `KeyboardDragListener`.

Your `SoundRichDragListener` will look something like this:

```ts
// pdom - dragging using the keyboard
const keyboardDragListener = new KeyboardDragListener( {
  positionProperty: widget.positionProperty,
  dragBoundsProperty: dragBoundsProperty,
  transform: modelViewTransform,
  dragSpeed: 100, // velocity - change in position per second
  shiftDragSpeed: 20 // finer-grained
} );
```

You’ll also need to add these options to your Node to make it focusable:

```
// pdom options
tagName: 'div',
focusable: true
```

## Drag using AccessibleSlider for 1D Motion

If your draggable component moves in 1 dimension consider using AccessibleSlider. AccessibleSlider is a trait that can
be mixed into a Node to add 1D motion with alternative input. AccessibleSlider will make the component much more
accessible for a screen reader user compared to KeyboardDragListener. It is very easy to use when there is a
NumberProperty driving the position. Here is an example:

```ts
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
```

AccessibleSlider will support movement with arrow keys, as well as other keys such as home/end to quickly move the
component to the limits of the range. See AccessibleSlider and its supertype AccessibleValueHandler for more options and
functionality.

## Hotkeys

Hotkeys are added with `KeyboardListener`. A KeyboardListener can be added to a Node, and will fire its callback
whenever the specified keys are pressed while the Node has focus. The keys should be defined with HotkeyData.
Create a public static field in your class that is an instance of HotkeyData. Use the HotkeyData in your keyboard
listener and in your keyboard help dialog so that commands and labels are defined in one place. HotkeyData also
supports auto-generated documentation for hotkeys.

Here is an example:

```ts

// a static somewhere in your class
public static readonly HOTKEY_DATA = new HotkeyData( {
  keys: [ 'j+0' ],
  keyboardHelpDialogLabelStringProperty: SimRepoStrings.labelForCommand,
  repoName: simNamespace.name
} );

const keyboardListener = new KeyboardListener( {
  keyStringProperties: MyClass.HOTKEY_DATA.keyStringProperties,
  fire: ( event, keysPressed, listener ) => {
    // j+0 was pressed!
  }
} );

myNode.addInputListener( keyboardListener );
```

You can also add a global Hotkey that will fire regardless of which Node has focus. As long as the target Node can
receive input events, the listener will fire. Here is an example:

```ts

// a static somewhere in your class
public static readonly HOTKEY_DATA = new HotkeyData( {
  keys: [ 'alt+r' ],
  keyboardHelpDialogLabelStringProperty: SimRepoStrings.labelForCommand,
  repoName: simNamespace.name,
  global: true // for documentation, mark this as a global hotkey
} );

const globalKeyboardListener = KeyboardListener.createGlobal( targetNode, {
  keyStringProperties: MyClass.HOTKEY_DATA.keyStringProperties,
  fire: ( event, keysPressed, listener ) => {
    // alt+r was pressed globally!
  }
} );
```

Be careful not to add hotkeys that collide with other global hotkeys defined by PhET. All used hotkeys can be reviewed
with binder documentation at https://phetsims.github.io/binder/. This list is auto-generated from HotkeyData.
Scenery will also throw an assertion at runtime though if there is an overlap.

## Scenery Events

For more custom behavior you can add input listeners with Scenery's input system that are related to alternative input.
For example, if you want to add behavior whenever a Node has focus you can add a listener like this:

```ts
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
2) Reposition the highlight if there is a transformation to the focused Node.

## Pan and Zoom

Scenery will pan to put the focused Node in the center of the viewport when focus changes and when the focused Node
moves. Try to make your focused Node the logical interactive display object. For example, if you have a draggable
component that is a child of a larger Node, make the draggable component the focused Node so that scenery can keep that
Node displayed. If you must do something else, you can use animatedPanZoomSingleton to control the panning. For example:

```ts
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

## Toolboxes

Toolboxes support alt input with a pattern described in https://github.com/phetsims/sun/blob/main/doc/ToolboxPattern.md,
and can be viewed in [Binder](https://phetsims.github.io/binder/). Basically we treat toolbox icons as buttons, and
selecting the button focuses the created tool. A simple KeyboardDragListener can support dragging on the tool, and
`GrabDragInteraction` is not needed for this
case. ([Original paper trail](https://github.com/phetsims/a11y-research/issues/166))

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
