# Interactive Highlights - Quickstart Guide

@author Jesse Greenberg

A quick guide for adding Interactive Highlights to your PhET Simulation.

Interactive Highlights are highlights that surround interactive components on mouse and touch input. Interactive
Highlights can benefit many users, and are particularly helpful for users with low vision who need a little extra
visual boldness to identify the interactive components in the sim.

When a sim supports Interactive Highlights, a toggle switch will be available in the Visual tab of the Preferences
dialog to enable the feature. When enabled, moving a mouse or finger over an interactive component will display a
visual highlight around that component. When the pointer leaves the component the highlight will disappear.

You can use query parameter flag `interactiveHighlightsInitiallyEnabled` to have Interactive Highlights enabled
when the sim loads.

## package.json

By default, Interactive Highlights are enabled when the sim supports Interactive Description (or alternative input).
To enable both Interactive Description and Interactive Highlights, have the following in the sim's package.json

```json
{
  "phet": {
    "simFeatures": {
      "supportsInteractiveDescription": true
    }
  }
}
```

If you want to enable or disable Interactive Highlights separately from `supportsInteractiveDescription`, you can
do so with

```json
{
  "phet": {
    "simFeatures": {
      "supportsInteractiveHighlights": false
    }
  }
}
```

`supportsInteractiveHighlights` will always override the default from `supportsInteractiveDescription`.

After modifying package.json, run `grunt update`.

When Interactive Highlights are supported, there will be a toggle switch in the Visual tab of the Preferences dialog to
enable the feature.

## InteractiveHighlighting.ts

Common code components will now be highlighted when a pointer moves over them. But sim-specific
interactive Nodes will need to be composed with `InteractiveHighlighting.ts` to get this feature.
`InteractiveHighlighting` is a trait that adds listeners to a Node that activate highlights from pointer input.

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

## InteractiveHighlightingNode.ts

If the trait pattern is inconvenient (or you prefer not to use traits in general) you can extend or instantiate an
InteractiveHighlightingNode which will accomplish the same thing.

```js
class MyCompositeNode extends Node {
  public constructor() {
    super();

    // InteractiveHighlightingNode is a Node composed with InteractiveHighlighting so you don't have to create your
    // own sublcass for the trait pattern.
    const subcomponentNode = new InteractiveHighlightingNode();
    
    // Now add your own listeners to subcomponentNode.
  }
}
```

## Custom Highlights

By default, highlights are rectangular and surround the Node's bounds. But the highlight can be customized. By default,
Interactive Highlights will use the same highlight as the focus highlight, so you can set both at once with this setter
from `ParallelDOM.ts`.

```js
myNode.focusHighlight = new FocusHighlightPath( focusHighlightShape );
```

If the Interactive Highlight needs to look different than the focus highlight, you can do that with an additional
setter from `InteractiveHighlighting.ts`.

```js
myNode.interactiveHighlight = new FocusHighlightPath( interactiveHighlightShape );
```

See InteractiveHighlighting.ts for more documentation.

## Disabling Interactive Highlights

The highlights for Interactive Highlights are activated on mouse and touch input. If you need to prevent highlights
from activating (for an icon or instance of a Node that is not interactive) you can set `pickable: false` on the Node.

If you don't want to use `pickable`, you can also disable Interactive Highlights for a Node with setter/option in
InteractiveHighlighting.ts

```js
myNode.interactiveHighlightEnabled = false
```

## Disposal
InteractiveHighlighting adds listeners to the Node to activate it on mouse/touch input. Remember to dispose the Node
composed with InteractiveHighlighting if you need to.

## Potential Pitfalls

Try to use default highlights or `FocusHighlightFromNode.ts` for custom highlights if possible. These will manage
styling and repositioning for you. If you use a more custom highlight Node, it is your responsibility to
reposition the highlight if the Node it surrounds resizes or moves.
