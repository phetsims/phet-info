# Alternative Input - Quick Start Guide

Follow these steps to add support for alternative input to a simulation.

1. In package.json, add this to the “phet” section:

```json
"simFeatures": {
  "supportsInteractiveDescription": true
},
```

2. Run `grunt update` to generate `{{REPO}}_a11y_view.html` and modify `{{REPO}}_en.html`.

3. For non-`LayoutBox` parent Nodes, explicitly set `this.pdomOrder` at the end of constructor. Do not rely on scenery’s
   default ordering, which corresponds to the order that children are added. It’s better to decouple rendering order and
   traversal order by explicitly setting `this.pdomOrder`. Note that most of the work here is in `ScreenView` subclasses.

4. For `LayoutBox` Nodes do nothing. There is a good match between layout order and traversal order; they are typically the same.

5. If you need to augment `this.pdomOrder` in a subclass, read about the numerous pitfalls
   in https://github.com/phetsims/scenery/issues/1308.

6. `DragListener` does NOT handle keyboard input. For Nodes where you’ve added a `DragListener`, you’ll need to add a
   corresponding `KeyboardDragListener`. The options for the `DragListener` and `KeyboardDragListener` will typically be
   similar, but beware that API differences exist. Your `KeyboardDragListener` should look something like this:

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

7. `PressListener` DOES handle keyboard input. For Nodes where you've added a `PressListener`, add these options to your
   Node:

```js
// pdom
tagName: 'button'
```

8. There may be common-code UI components for which alternative input has not been implemented. And there may be PhET
   design patterns for which alternative-input behavior has not been designed. Identify lack of alternative-input
   support, and create GitHub issues.
