# Interactive Highlights - Quickstart Guide

@author Jesse Greenberg

A quick guide for adding Interactive Highlights to your PhET Simulation.

## PreferencesModel

To add support for Interactive Highlights, add the following to your Sim.ts options:

```js
const simOptions = {
  preferencesModel: new PreferencesModel( {
    visualOptions: {
      supportsInteractiveHighlights: true
    }
  } )
}
```

Now, when you run your sim, there will be a toggle switch in the Visual tab of the Preferences dialog to enable
Interactive Highlights.

## InteractiveHighlighting.ts

Common code components will now be highlighted when a pointer is over them. But sim-specific
interactive Nodes will need to be composed with `InteractiveHighlighting.ts` to get this feature.
`InteractiveHighlighting` is a trait that adds listeners to activate the highlight from pointer input.

Here is an example of composing a Node with InteractiveHighlighting.

```js
class MyDraggableNode extends InteractiveHighlighting( Node ) {
  public constructor() {
    super();
    
    // Now presumably it adds its own input listeners to implement dragging.
    // ... 
  }
}
```

## Custom Highlights

By default, highlights are rectangular and surround the Node's bounds. But the highlight can be customized.
It probably makes sense to set both the Interactive Highlight and focus highlight so they are the same. By default,
Interactive Highlights will use the highlight for focus, so you can set both with this setter from `ParallelDOM.ts`.

```js
myNode.focusHighlight = new FocusHighlightPath( focusHighlightShape );
```

If you need to set them separately, you can do that with an additional setter from `InteractiveHighlighting.ts`.

```js
myNode.interactiveHighlight = new FocusHighlightPath( interactiveHighlightShape );
```

See InteractiveHighlighting.ts for more documentation.

## Potential Pitfalls

Try to use default highlights or `FocusHighlightFromNode.ts` for custom highlights if possible. These will manage
styling and repositioning for you. If you use a more custom highlight Node, it is your responsibility to
reposition the highlight if the Node it surrounds resizes or moves.