# Interactive Highlights - Quickstart Guide

@author Jesse Greenberg

A quick guide for adding Interactive Highlights to your PhET Simulation.

## PreferencesModel

To add support for Interactive Highlight, add the following to your Sim.ts options:

```js
const simOptions = {
  preferencesModel: new PreferencesModel( {
    visualOptions: {
      supportsInteractiveHighlights: true
    }
  } )
}
```

Now when you run your sim, there will be a toggle switch in the Visual tab of the
Preferences dialog that will enable Interactive Highlights.

## InteractiveHighlighting.ts

Common code components will now become highlighted when a pointer is over them. But sim-specific
interactive Nodes will need to be composed with InteractiveHighlighting.ts to get this feature.
InteractiveHighlighting is a trait that adds listeners to activate the highlight from pointer input.

Here is an example of composing a Node with InteractiveHighlighting.

```js

// This class composes the InteractiveHighlighting trait.
class MyDraggableNode extends InteractiveHighlighting( Node ) {
  public constructor() {
    super();
    
    // Now presumably it adds its own input listeners to implement dragging. 
  }
}
```

## Custom Highlights

By default, highlights are rectangular and surround the Node's bounds. But the highlight can be customized.
It probably makes sense to customize both the Interactive Highlight and focus highlight. By default, Interactive
Highlights use the focus highlight, so you can set both with this setter from ParallelDOM.ts.

```js
myNode.focusHighlight = new FocusHighlightPath( focusHighlightShape );
```

If you need to set them separately, you can do that too with an additional setter from InteractiveHighlighting.ts

```js
myNode.interactiveHighlight = new FocusHighlightPath( interactiveHighlightShape );
```

See InteractiveHighlighting.ts for more documentation.