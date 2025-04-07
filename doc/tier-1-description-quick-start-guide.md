# Tier 1 Description - Quickstart Guide

@author Jesse Greenberg

A quick guide for adding Tier 1 Interactive Description to a PhET simulation.

Tier 1 Interactive Description implements critical screen reader accessibility features, including:

- Accessible names for interactive objects
- Accessible help text for interactive objects
- A screen summary for each screen (overview, current details, and hints)
- Descriptions for non-interactive visual content

Implementing Tier 1 significantly improves a simulation’s accessibility. This guide outlines the process and introduces
the fundamental options and tools for the implementation. Refer to the source code documentation for more detailed
information.

## Overall Process

The simulation design team provides the content required for Tier 1 Interactive Description in a design document. This
includes:

- A screen summary for each screen (covering the play area, control area, current details, and interaction hint).
- A heading structure outlining major areas of the simulation.
- Accessible names for interactive components.
- Accessible help text for interactive components.
- Accessible paragraphs for non-interactive UI elements.

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

## Screen Summary

Use ScreenSummaryContent.ts in joist to implement the screen summary.

For each screen, the design document provides text for the play area, control area, current details, and an interaction
hint. Pass these to ScreenSummaryContent, then include that content as an option in the ScreenView constructor.

## Basic options

The options `accessibleName`, `accessibleHelpText`, and `accessibleParagraph` are defined in scenery's ParallelDOM.ts.
These are most of what you will use to implement Tier 1 Interactive Description.

### accessibleName and accessibleHelpText

Each interactive component needs to have an `accessibleName`, which is how screen readers identify the UI element. Some
components also have `accessibleHelpText`, which explains how to use the UI component or give the user more context.

For common code components (e.g., buttons, checkboxes, dialogs), these can be set as options or via setters:

```ts
const myCheckBox = new Checkbox( checkedProperty, {
  accessibleName: myAccessibleNameStringProperty,
  accessibleHelpText: myAccessibleHelpTextStringProperty
} );
```

For sim-specific interactive components, specify a `tagName` to enable accessibility. If the component is in the
traversal order, make it `focusable: true`.

```ts
const interactiveCircle = new Circle( 25, {
  tagName: 'div',
  focusable: true,
  accessibleName: myAccessibleNameStringProperty,
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

### accessibleHeading (UNDER CONSTRUCTION)

Use `accessibleHeading` to define headings within the simulation. Headings help users navigate sections easily and
maintain accessible structure. Scenery automatically determines the heading level based on the scene graph and
`pdomOrder`.

```ts
const controlsContainer = new VBox( {
  children: controls,
  accessibleHeading: accessibleHeadingStringProperty,
  tagName: 'div'
} ); 
```

Nodes with `accessibleHeading` are typically parents for other accessible content, establishing the heading scope for
their children. For details, see ParallelDOM.setAccessibleHeading.

## Default accessible names

Many UI components with a visual label will automatically use that label as their `accessibleName`. If needed, you can
override it by setting `accessibleName` in the component’s options.

## pdomOrder

Use pdomOrder to define the navigation order for both focusable and non-focusable elements. This ensures that items
using accessibleParagraph or accessibleHeading appear in the correct reading sequence and follow a logical structure in
the DOM.

## String Properties

Use a LocalizedStringProperty for all accessibility content so it’s ready for dynamic locales and future translation
support.

When describing model values in plain language, DerivedProperty.fromRecord can help select the correct string based on
the current state:

```ts
const diagram = new Node( {
  children: [ graphics ],
  accessibleParagraph: DerivedProperty.fromRecord( selectedValuesProperty, {
    time: new StringProperty( 'Describes the diagram when plotting against time.' ),
    energy: new StringProperty( 'Describes the diagram when plotting against energy.' )
  } )
} );
```

For controlling how many digits to display, use DerivedProperty.toFixed. For example:

```ts
const fixedValueProperty = DerivedProperty.toFixed( modelValueProperty, 2 );
const numberReadout = new Text( fixedValueProperty, {
  accessibleParagraph: fixedValueProperty
} );
```

## Disposal

Accessibility options take axon `Property` instances, so dispose of Nodes when they are no longer needed to avoid memory
leaks.

## Specific Components

### Sliders

Sliders use `AccessibleValueHandler` to report their numeric value through a screen reader. This value is read in
addition to the component’s `accessibleName`. Be sure to use a readable level of precision, and include units if needed.
You can customize the text that’s read by providing a function to `AccessibleSlider`’s `pdomCreateAriaValueText` option,
for example:

```ts
const slider = new HSlider( valueProperty, range, {
  pdomCreateAriaValueText: value => {
    return `${toFixed( value, 2 )} units`
  }
} );
```

### KeyboardDragListener

Draggable components will likely use `KeyboardDragListener`. Use `dragDelta` instead of `dragSpeed` options if possible.
This approach moves the object in discrete steps for each key press. Avoid `dragSpeed`, which tries to move the object
while the key is held down. This is often incompatible with screen readers that do not support press-and-hold
interactions.

To make a component fully keyboard accessible, pass `AccessibleDraggableOptions` to the target Node. These options add
the necessary support for screen-reader interaction.

## Internationalization

Accessibility strings are not yet translatable. However, plan for future translation by keeping string patterns simple
and avoiding multiple placeholders. Complex strings with multiple placeholders can create challenges for gender,
pluralization, and other grammatical rules when translated.

### Accessibility Strings

Accessibility strings should be placed under the "a11y" key to keep them separate from translatable strings (they are
not yet translated).

It’s generally fine to reuse the same string for visual text and accessibility if the meaning is truly identical.
However, if the string is used in multiple contexts or has a different meaning, create a separate key to allow for
unique translations or messaging later.

Use the following guidelines for naming and organization:

- Keys under the `a11y` key should be nested for readability.
- Use key names that match the tandem name of the component using the string.
- Under the component name key, use a nested key that matches the accessibility option you are using.
- For screen summary content, use a key called `screenSummary` and nest each section under it.
- For string patterns, include `Pattern` in the suffix of the key.
- For entries that have string patterns with values to fill in, use additional nesting for readability.
- For strings that do not fit into these categories, use a descriptive key that indicates how it is used.

For example:

```json
{
  "a11y": {
    "screenA": {
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

## Additional resources

### How to use screen readers

The following resources contain information about how to use a screen reader:

- [VoiceOver](https://docs.google.com/document/d/1qz0Dm2lA67tRhgw1GaHVeOSnldBoMj7AT5UE_UaXz1U/edit)
- [NVDA](https://docs.google.com/document/d/1pgfyEER7ZlpJlXSwvSCbNBuoCa5oOexc7QvTuFZu-Mo/edit)
- [JAWS](https://docs.google.com/document/d/1aggemqGsb2CdR7PxgLG50kOg4ZwBPM2M3eI3okyZHJ8/edit)

### Alt Input

Interactive Description includes alternative input. Refer to the Alternative Input quickstart guide for setup:
[Alternative Input Quickstart Guide](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md).

### Tier 1 Voicing

For Tier 1 Voicing implementation guide, see
[Tier 1 Voicing Quickstart Guide](link to  guide).