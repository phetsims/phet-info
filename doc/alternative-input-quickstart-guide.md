# Alternative Input - Quickstart Guide

Follow these steps to add support for alternative input to a simulation.

1. In your sim's package.json, add this to the “phet” section:

```json
"simFeatures": {
  "supportsInteractiveDescription": true
},
```

2. In your sim's repository, run `grunt update`. This will generate `{{REPO}}_a11y_view.html` and modify `{{REPO}}_en.html`.

3. For `LayoutBox` (and its subclasses) there is no need to specify traversal order. There is a good match between layout order and traversal order; they are typically the same.  So for `LayoutBox`, you can do nothing.

4. For non-`LayoutBox` classes, explicitly set `this.pdomOrder` at the end of constructor. Do not rely on scenery’s
   default ordering, which corresponds to the order that children are added. It’s better to decouple rendering order and
   traversal order by explicitly setting `this.pdomOrder`. Note that most of the work here is in `ScreenView` subclasses.

5. For `ScreenView`, `this.pdomOrder` cannot be set directly. There are two approaches you can use to specify traversal order at the ScreenView level. Check with your sim designer to see which approach is appropriate.

  (a) Add Nodes to either the "Play Area" or "Control Area". Do not add Nodes directly to the ScreenView. Instead,
use this pattern in your ScreenView constructor:
      
```js
this.pdomPlayAreaNode.children = [ ... ];
this.pdomPlayAreaNode.pdomOrder = [ ... ]; // decouple traversal order from rendering order
this.pdomControlAreaNode.children = [ ... ];
this.pdomControlAreaNode.pdomOrder = [ ... ]; // decouple traversal order from rendering order
```

  (b) In many cases, "Play Area" and "Control Area" can be ignored for the purposes of alternative input. If 
that is appropriate for your sim, then do not add Nodes directly to the ScreenView. Instead, use this pattern
in your ScreenView constructor:

```js
const screenViewRootNode = new Node( {
   children: [...]
});
screenViewRootNode.pdomOrder = [...]; // decouple traversal order from rendering order
this.addChild( screenViewRootNode );
```

6. If you need to augment `this.pdomOrder` in a subclass, read about the numerous pitfalls
   in https://github.com/phetsims/scenery/issues/1308.

7. `DragListener` does NOT handle keyboard input. For Nodes where you’ve added a `DragListener`, you’ll need to add a
   corresponding `KeyboardDragListener`. The options for your `DragListener` and `KeyboardDragListener` will typically be
   similar, but beware that API differences exist. Your `KeyboardDragListener` will look something like this:

```js
// pdom - dragging using the keyboard
const keyboardDragListener = new KeyboardDragListener( {
  positionProperty: widget.positionProperty,
  dragBounds: dragBoundsProperty.value,
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

8. `PressListener` DOES handle keyboard input. For Nodes where you've added a `PressListener`, add these options to your
   Node:

```js
// pdom
tagName: 'button'
```

9. There may be common-code UI components for which alternative input has not been implemented. And there may be PhET
   design patterns for which alternative-input behavior has not been designed. Identify lack of alternative-input
   support, and create GitHub issues.

## Other Resources

* [Interactive Description Technical Guide](https://github.com/phetsims/phet-info/blob/4839f03214bbba21b4621f80aea8e78a9519fb43/doc/interactive-description-technical-guide.md)
* Description of "Play Area" and "Control Area": https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md#pdom-order-for-phet-sims
