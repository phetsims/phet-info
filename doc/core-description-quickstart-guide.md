# Core Description - Quickstart Guide

@author Jesse Greenberg

A quick guide for adding Core Description to a PhET simulation.

Core Description implements critical screen reader accessibility features, including:

- Accessible names for interactive objects
- Accessible help text for interactive objects
- A screen summary for each screen (overview, current details, and hints)
- Descriptions for non-interactive visual content
- Accessible headings for important areas of the simulation
- Accessible responses (alerts) for important events or changes in the simulation or for voicing values that are not
  otherwise available

Implementing Core Description significantly improves a simulation’s accessibility. This guide outlines the process and
introduces the fundamental options and tools for the implementation. Refer to the source code documentation for more
detailed information.

## Overall Process

The simulation design team provides the content required for Core Description in a design document. This includes:

- A screen summary for each screen (covering the play area, control area, current details, and interaction hint)
- A heading structure outlining major areas of the simulation
- Accessible names for interactive components
- Accessible help text for interactive components
- Accessible paragraphs for non-interactive UI elements
- Accessible responses (alerts) for important events or changes in the simulation, or for voicing values that are not
  otherwise available

## package.json

In package.json, set the following flag to enable interactive description:

```json
{
  "phet": {
    "simFeatures": {
      "supportsInteractiveDescription": true
    }
  }
}
```

After modifying package.json, run `grunt update` to apply changes.

## Testing

After enabling Interactive Description in package.json, launch the a11y-view from phetmarks. An iframe on the left shows
the simulation, and on the right you’ll see a representation of the accessible content. This right pane displays what a
screen reader can read. As you add or revise accessibility content, refresh the page to see your changes.

To test directly with a screen reader, run the simulation without the a11y-view and enable your screen reader. For
details on installing and using screen readers, see the resources at the end of this document.

## Screen Summary

Use `ScreenSummaryContent.ts` in joist to implement the screen summary.

For each screen, the design document provides text for the play area, control area, current details, and an interaction
hint. Pass these to `ScreenSummaryContent`, then include that content as an option in the `ScreenView` constructor.

```ts
const screenView = new ScreenView( {
  screenSummaryContent: new ScreenSummaryContent( {
    playAreaContent: playAreaDescriptionStringProperty,
    controlAreaContent: controlAreaDescriptionStringProperty,
    currentDetailsContent: [ firstDescriptionStringProperty, secondDescriptionStringProperty ],
    interactionHintContent: interactionHintStringProperty
  } )
} );
```

## AccessibleListNode

The design document often includes lists of description. Lists help simplify the strings and break up content into
understandable parts. Use AccessibleListNode for this. They are most often used in the Screen Summary.

```ts
const screenView = new ScreenView( {
  screenSummaryContent: new ScreenSummaryContent( {
    currentDetailsContent: new AccessibleListNode( [
      new StringProperty( '1 apple' ),
      new StringProperty( '2 oranges' ),
      new StringProperty( '4 strawberries' )
    ], {
      leadingParagraphStringProperty: new StringProperty( 'Currently, the fruit basket has:' )
    } )
  } )
} );
```

The above will produce the following list content in the PDOM:

```text
Currently, the fruit basket has:
- 1 apple
- 2 oranges
- 4 strawberries
```

AccessibleListNode is a Node. If not in the screen summary, add the AccessibleListNode to the scene graph with
`addChild`. Use `pdomOrder` to put it in the correct place in the reading order.

## Basic options

The options `accessibleName`, `accessibleHelpText`, and `accessibleParagraph` are defined in scenery's `ParallelDOM.ts`.
These are most of what you will use to implement Core Description.

NOTE: PhET is in the process of implementing accessibleName and accessibleHelpText in common code components. If you
find a component where these options do not work as expected, please create an issue in the component repository.

### accessibleName

Each interactive component should have an `accessibleName`, which is how screen readers identify the UI element. For
common code components
(e.g., buttons, checkboxes, sliders), you can set `accessibleName` as an option or via setters:

```ts
const myCheckBox = new Checkbox( checkedProperty, {
  accessibleName: myAccessibleNameStringProperty
} );
```

For sim-specific interactive components, specify a `tagName` to enable accessibility. If the component is in the
traversal order, make it `focusable: true`.

```ts
const interactiveCircle = new Circle( 25, {
  tagName: 'div',
  focusable: true,
  accessibleName: myAccessibleNameStringProperty
} );
```

#### Default accessibleName

Many UI components with a visual label will use the same string for the `accessibleName`. Occasionally, you will need to
supply an
`accessibleName` that is different from the default visible name. This is typically the case when the label is unclear
when spoken
(for example, when it contains an abbreviation). The design team will indicate when this is necessary in the design
document. The default can be overridden by passing an `accessibleName` option to the component constructor.

```ts
const checkbox = new Checkbox( checkedProperty, new Text( 'Show Cos Plot' ), {
  accessibleName: 'Show Cosine Plot'
} );
```

NOTE: PhET is in the process of implementing this default. If you find a component that does not do this, please create
an issue in the component repository.

### accessibleHelpText

Some components also have `accessibleHelpText`, which explains how to use the UI component or give the user more
context.

For common code components (e.g., buttons, checkboxes, dialogs), `accessibleHelpText` can be set as options or via
setters:

```ts
const myCheckBox = new Checkbox( checkedProperty, {
  accessibleHelpText: myAccessibleHelpTextStringProperty
} );
```

### accessibleParagraph

Use `accessibleParagraph` to describe non-interactive graphical content (images, graphs, text, etc.).

```ts
const myImage = new Image( imageData, {
  accessibleParagraph: myAccessibleParagraphStringProperty
} );
```

### accessibleHeading

`accessibleHeading` adds a semantic heading for screen-reader users. Headings help users navigate sections easily and
maintain accessible structure. Scenery picks the correct level (h1–h6) from the node’s place in the scene graph and
`pdomOrder`.

When you set an `accessibleHeading` on a Node, all child Nodes and all Nodes listed in its `pdomOrder` will be
considered "under" that heading.

The Node with `accessibleHeading` must be a child in the scene graph, or it will not appear in the accessible content.

Prefer `pdomOrder` over `children` to place Nodes under a heading. This lets you position accessible content under a
heading without changing the visual rendering order. It keeps the logical heading structure intact if the visual layout
changes. Using `children` is fine for layout containers like `VBox` or `Panel` where the visual and logical order
usually match.

#### Implementation Examples

The design document indicates where each “Accessible Heading” is needed and lists the content under it.

1) Create a wrapper Node and set the `accessibleHeading` option to the string `Property` that contains the heading text.
2) Use `pdomOrder` to place Nodes under the heading.
3) Add the wrapper Node to the scene graph, and place it in the parent's `pdomOrder` (often in the Play Area or Control
   Area).

```ts
const accessibleHeadingNode = new Node( {
  accessibleHeading: accessibleHeadingStringProperty,
  pdomOrder: [ firstNode, secondNode, thirdNode ]
} );
screenView.addChild( accessibleHeadingNode );

screenView.pdomPlayAreaNode.pdomOrder = [
  someNode,
  accessibleHeadingNode,
  anotherNode
];
```

Layout container variant:

```ts
const controlsContainer = new VBox( {
  accessibleHeading: accessibleHeadingStringProperty,
  children: controls
} ); 
```

## Accessible responses

Responses alert the screen-reader user to important changes or guidance while the sim is running.  
The design document labels each string with one of three response types:

- Accessible Object Response – state info about a specific object
- Accessible Context Response – broader information about the simulation
- Accessible Help Response – brief instructions or tips

### Common-code components

Many UI components expose convenience options that wire everything up for you.  
For example, `ButtonNode` supports `accessibleContextResponse`:

```ts
const importantButton = new RectangularPushButton( {
  accessibleName: accessibleNameStringProperty,
  accessibleContextResponse: accessibleContextResponseStringProperty
} );
```

NOTE: PhET is in the process of implementing responses in common code components. If you find a component where a
required response type is not implemented, please create an issue in the component repository.

### Sim-specific components

For custom Nodes, use the helper functions defined in scenery’s ParallelDOM.

#### addAccessibleObjectResponse

Should be spoken when the object receives focus and when its value or state changes.

```ts
const draggableCircle = new Circle( 25, combineOptions<CircleOptions>( {
  accessibleName: 'Draggable Circle'
}, AccessibleDraggableOptions ) );

const positionStatementStringProperty = new PatternStringProperty( 'The circle is at {{x}}, {{y}}', {
  x: xProperty,
  y: yProperty
} );

draggableCircle.focusedProperty.link( focused => {
  if ( focused ) {
    draggableCircle.addAccessibleObjectResponse( positionStatementStringProperty );
  }
} );

draggableCircle.addInputListener( new DragListener( {
  end: () => {
    draggableCircle.addAccessibleObjectResponse( positionStatementStringProperty );
  }
} ) );
```

#### addAccessibleContextResponse

Should be spoken immediately after interaction.

```ts
const clickableImage = new Image( img, {
  tagName: 'div',
  focusable: true,
  accessibleName: 'My Clickable Image'
} );

clickableImage.addInputListener( new PressListener( {
  press: () => {
    clickableImage.addAccessibleContextResponse( 'Something happened because you clicked the image.' );
  }
} ) );
```

### addAccessibleHelpResponse

Used sparingly; most hints should live in accessibleHelpText.

```ts
clickableImage.focusedProperty.link( focused => {
  if ( focused ) {
    clickableImage.addAccessibleHelpResponse( 'This image can be clicked to do something.' );
  }
} );
```

## pdomOrder

Use pdomOrder to define the navigation order for both focusable and non-focusable elements. This ensures that items
using `accessibleParagraph` or `accessibleHeading` appear in the correct reading sequence and follow a logical structure
in the DOM.

## String Properties

Use a `LocalizedStringProperty` for all accessibility content so it’s ready for dynamic locales and future translation
support.

When describing model values in plain language, `DerivedProperty.fromRecord` can help select the correct string based on
the current state:

```ts
const diagram = new Node( {
  children: [ graphics ],
  accessibleParagraph: DerivedProperty.fromRecord( selectedValuesProperty, {
    time: new StringProperty( 'Describes the diagram when plotting against time.' ),
    distance: new StringProperty( 'Describes the diagram when plotting against distance.' )
  } )
} );
```

## Disposal

Accessibility options take axon `Property` instances, so dispose of Nodes when they are no longer needed to avoid memory
leaks.

## Specific Components

### Sliders

Sliders use `AccessibleValueHandler` to report their numeric value through a screen reader. This value is read in
addition to the component’s `accessibleName`. Be sure to use a readable level of precision, and include units if needed.
You can customize the text that’s read by providing a function to `AccessibleSlider`’s `createAriaValueText` option,
for example:

```ts
const slider = new HSlider( valueProperty, range, {
  createAriaValueText: value => {
    return `${toFixed( value, 2 )} units`
  }
} );
```

### KeyboardDragListener

KeyboardDragListener is the preferred way to make a draggable object keyboard-accessible. Whenever possible, use
`dragDelta` (one key press -> one discrete move) instead of `dragSpeed` (move while the key is held), because many
screen-reader/OS combinations do not recognize press-and-hold interactions. g1

To make a component fully accessible, use `AccessibleDraggableOptions` with the target Node. These options add the
necessary support for screen-reader interaction. For example:

```ts
const accessibleDraggableOptions = combineOptions<ParallelDOMOptions>( {}, AccessibleDraggableOptions, {
  accessibleName: 'Circle'
} );
```

### KeyboardListener

KeyboardListener is used to add general keyboard input to a Node. You can use KeyboardListener to make a Node respond to
key presses without "dragging" behavior.

To make the component fully accessible, use `AccessibleInteractiveOptions` with the target Node. These options add the
necessary support for screen-reader interaction. For example:

```ts
const accessibleInteractiveOptions = combineOptions<ParallelDOMOptions>( {}, AccessibleInteractiveOptions, {
  accessibleName: 'My Interactive Node'
} );
```

### Roles

Certain components benefit from a custom role description, which explains their purpose and how to interact with them.
The `accessibleRoleDescription` will be provided by the design team. The string should be localized, so put it in the
strings.json file. See Accessibility Strings section below. You can set it with the option `accessibleRoleDescription`:

```ts
const movableCircle = new Circle( 5, {
  accessibleRoleDescription: 'movable',

  tagName: 'div',
  focusable: true,
} );
```

## Numeric Precision

Expose numeric values at the same precision in the PDOM as on-screen.

- Use the same formatter (toFixed, NumberFormatter) for both visual text and PDOM
  strings.
- If a value is shown with units or a label visually, include the same units or label in the PDOM string.
- For components that supply their own PDOM value text (such as AccessibleSlider or AccessibleValueHandler), override
  the default with createAriaValueText if necessary to keep precision consistent.

```ts
// Show the value to two decimal places both visually and in the PDOM.
const formattedValueProperty = new DerivedProperty( [ modelValueProperty ], modelValue => {
  return toFixed( modelValue, 2 );
} );

const readoutText = new Text( formattedValueProperty, {
  accessibleParagraph: formattedValueProperty
} );

const slider = new HSlider( modelValueProperty, range, {
  createAriaValueText: value => `${formattedValueProperty.value} meters`,
  accessibleName: accessibleSliderNameStringProperty
} );
```

## Internationalization

Accessibility strings are not yet translatable. However, plan for future translation by keeping string patterns simple
and avoiding multiple placeholders. Complex strings with multiple placeholders can create challenges for gender,
pluralization, and other grammatical rules when translated.

### Accessibility Strings

Accessibility strings should be placed under the `a11y` key in the strings.json file. This keeps them separate from
translatable strings (they are not yet translated).

It’s generally fine to reuse the same string for visual text and accessibility if the meaning is truly identical.
However, if the string is used in multiple contexts or has a different meaning, create a separate key to allow for
unique translations or messaging later.

Use the following guidelines for naming and organization:

- Keys under the `a11y` key should be nested for readability.
- Use key names that match the tandem name of the component using the string.
- Under the component name key, nest a key for the specific accessibility option (e.g., accessibleName,
  accessibleHelpText, accessibleParagraph, etc.).
- For screen summary content, use the screen name as a key, then nest a screenSummary key, with playArea, controlArea,
  currentDetails, and interactionHint as sub-keys.
- Nest `screenButtonsHelpText` under the screen name.
- Avoid unnecessary nesting under screen name keys; this makes reuse harder. For example, even if a checkbox appears in
  only one screen, do not nest its strings under that screen name.
- For entries that have string patterns with values to fill in, use additional nesting for readability.
- For strings that do not fit into these categories, use a descriptive key that indicates how it is used.
- Prefer longer or duplicated strings over complex string patterns. This simplifies code and translation. Patterns often
  assume English-specific grammar.

For example:

```json
{
  "a11y": {
    "screenA": {
      "screenButtonsHelpText": {
        "value": "Use a light source to explore the atom's energy states."
      },
      "screenSummary": {
        "playArea": {
          "value": "Contains a light source and..."
        },
        "controlArea": {
          "value": "Contains buttons and checkboxes that..."
        },
        "currentDetails": {
          "pattern": {
            "value": "Currently, the atom is in its {{level}} energy state."
          },
          "highest": {
            "value": "highest"
          },
          "lowest": {
            "value": "lowest"
          }
        },
        "interactionHint": {
          "value": "Turn on light source to start exploring."
        }
      }
    },
    "visibilityCheckbox": {
      "accessibleName": {
        "value": "Units Visible"
      },
      "accessibleHelpText": {
        "value": "Toggle to hide all units in the simulation."
      }
    },
    "energyDiagram": {
      "accessibleParagraph": {
        "value": "A plot of energy vs time with..."
      }
    },
    "atom": {
      "accessibleName": {
        "value": "Atom"
      },
      "accessibleParagraphPattern": {
        "value": "Atom energy state: {{state}}."
      },
      "highest": {
        "value": "highest"
      },
      "lowest": {
        "value": "lowest"
      }
    }
  }
}
```

## Implementation Tips

### Use visibility to manage accessible content

When a node is not visible, its accessible content is also hidden from screen readers. You can leverage this to manage
dynamic descriptions. For example, assign different `accessibleParagraph`
values to nodes that toggle visibility based on state. Only the relevant description will be available.

```ts
const emptyStringProperty = new StringProperty( 'The basket is empty.' );
const emptyStateText = new Text( emptyStringProperty, {
  visibleProperty: DerivedProperty.not( isBasketFilledProperty ),
  accessibleParagraph: emptyStringProperty
} );

const filledStringProperty = new StringProperty( 'The basket contains 3 apples and 2 oranges.' );
const filledStateText = new Text( filledStringProperty, {
  visibleProperty: isBasketFilledProperty,
  accessibleParagraph: filledStringProperty
} );
```

## Additional resources

### How to use screen readers

The following resources contain information about how to use a screen reader:

- [VoiceOver](https://docs.google.com/document/d/1qz0Dm2lA67tRhgw1GaHVeOSnldBoMj7AT5UE_UaXz1U/edit)
- [NVDA](https://docs.google.com/document/d/1pgfyEER7ZlpJlXSwvSCbNBuoCa5oOexc7QvTuFZu-Mo/edit)
- [JAWS](https://docs.google.com/document/d/1aggemqGsb2CdR7PxgLG50kOg4ZwBPM2M3eI3okyZHJ8/edit)

### Alt Input

Interactive Description includes alternative input. Refer to the Alternative Input quickstart guide for setup:
[Alternative Input Quickstart Guide](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md).

### Core Voicing

For Core Voicing implementation guide, see
[Core Voicing Quickstart Guide](https://github.com/phetsims/phet-info/blob/main/doc/core-voicing-quick-start-guide.md).