# Core Voicing - Quickstart Guide

@author Jesse Greenberg

A quick guide for adding Core Voicing to a PhET simulation.

Voicing uses speech synthesis to make PhET simulations more accessible. Unlike Interactive Description, which primarily
uses the Parallel DOM for screen reader support, Voicing provides a built-in solution that self-voices content.

Core Voicing is a subset of the full Voicing feature. It focuses on four main elements:

- Voicing names for interactive objects
- Voicing hint responses
- Screen summary content (overview, details, hints)
- Reading blocks for prominent text

These features are generally quicker to design and implement but still significantly improve accessibility. Because
Voicing content often overlaps with Interactive Description, it is recommended to implementing both at once.

This guide outlines the fundamentals of Core Voicing and shows how to integrate it into your simulation. Refer to the
source code documentation for more advanced details.

## Overall Process

The simulation design team typically provides Core Voicing content in a table, often alongside Interactive Description
details. Developers then reference those tables to apply the appropriate Voicing options in the code. For sim-specific
components, you will use scenery’s Voicing classes and mixins to ensure interactive objects speak their assigned
content.

## package.json

In package.json, set the following flag to enable Core Voicing:

```json
{
  "phet": {
    "simFeatures": {
      "supportsCoreVoicing": true
    }
  }
}
```

After modifying package.json, run `grunt update` to apply changes.

## Testing

Once Core Voicing is enabled in package.json, launch the simulation. In the Preferences dialog, go to the Audio tab
and enable Voicing. A toolbar will then appear on the left with buttons that play screen summary content.

Some components already support Voicing by default. Click them to hear their audio. For other UI elements, add Voicing
using the appropriate options and setters.

For debugging, use the ?logVoicingResponses query parameter to log spoken output in the console.

## Screen Summary

Use `ScreenSummaryContent.ts` in joist to implement the screen summary.

By default, this pulls the same content used by Interactive Description. If the Voicing content differs from Core
Description, you can customize with options.

For each screen, the design document provides text for the play area, control area, current details, and an interaction
hint. Pass these to the `ScreenSummaryContent`, then include that content as an option in the `ScreenView` constructor.

```ts
const screenView = new ScreenView( {
  screenSummaryContent: new ScreenSummaryContent( {
    playAreaContent: playAreaDescriptionStringProperty,
    controlAreaContent: controlAreaDescriptionStringProperty,
    currentDetailsContent: [ firstDescriptionStringProperty, secondDescriptionStringProperty ],
    
    // An example of how to set content that will be customized for Voicing.
    interactionHintContent: {
      descriptionContent: [ descriptionInteractionHintStringProperty ],
      voicingContent: [ voicingInteractionHintStringProperty ]
    }
  } )
} );
```

## Voicing.ts

`Voicing.ts` is a trait defined in Scenery that you mix into any Scenery Node.

```ts
const voicingRectangle = new ( Voicing( Rectangle ) )( 0, 0, 40, 40, {
  fill: 'green',

  // Voicing options
  voicingNameResponse: nameStringProperty,
  voicingHintResponse: hintStringProperty
} );
```
- `voicingNameResponse` is the name for the component and is spoken when the component is focused or activated.
- `voicingHintResponse` is a brief hint and is spoken after the name when the component is focused.
Together, these options satisfy almost all Core Voicing requirements.

## Default Content for common code

Many components already determine their default Voicing content.

- If a component has an `accessibleName`, it is used for `voicingNameResponse`.
- If it has an `accessibleHelpText`, that is used for `voicingHintResponse`.

As a result, Core Voicing often comes for free once Core Interactive Description is in place. However, you can
always override these defaults by supplying your own `voicingNameResponse` and `voicingHintResponse` options.

NOTE: PhET is in the process of implementing this behavior in common code components. If you find a component where
these options do not work as expected, please create an issue in the component repository.

## Sim Specific Components

For custom elements, compose your Node with Voicing. You can then specify `voicingNameResponse` and
`voicingHintResponse`. If a component can be pressed or dragged, also set `voicingPressable: true` to announce its
content during interaction.

```ts
const voicingCircle = ( new Voicing( Circle )( 25, {
  voicingNameResponse: nameStringProperty,
  voicingHintResponse: hintStringProperty,
  voicingPressable: true
} ) );
```

## Reading Blocks

Reading Blocks highlight important text so it can be spoken when clicked or focused. This text is identified in the
design document.

In most cases, implement Reading Blocks with VoicingText or VoicingRichText:

```ts
const voicingText = new VoicingText( myStringProperty );
const voicingRichText = new VoicingRichText( myStringProperty );
```

By default, they also add their text to the PDOM for Interactive Description. Make sure they appear in the correct
location in the `pdomOrder`.

## Interactive Highlights

Interactive Highlights is already included through Voicing, so you don’t need to separately mix in
`InteractiveHighlighting`. Any Node using Voicing will automatically gain Interactive Highlights features. For more
details, see [the Interactive Highlights quickstart guide](https://github.com/phetsims/phet-info/blob/f9fcab965f857627b7a2da4d0bb90f95ea9edc1e/doc/interactive-highlights-quickstart-guide.md).

## Accessibility Strings

Accessibility strings for Core Voicing follow the same guidelines as Core Interactive Description. For details, see
the Core Description quickstart guide.

- If a string is only used for Voicing, include the option name of its usage site (like `voicingNameResponse`) in the
  key.
- If a string is only used for Voicing but not tied to a specific option, prefix the key with "voicing" to clarify its
  purpose.
- If there is an equivalent string that appears in Interactive Description (`description`), prefix its key with
  `description` to show it is the Interactive Description version, and use the `voicing` prefix for the Voicing version.

```json
{
  "a11y": {
    "screenA": {
      "screenSummary": {
        "playArea": {
          "voicing": {
            "value": "Voicing specific play area content..."
          },
          "description": {
            "value": "Contains a light source and..."
          }
        }
      }
    }
  },
  "visibilityCheckbox": {
    "accessibleNameResponse": {
      "value": "Units"
    },
    "voicingNameResponse": {
      "value": "Units Visibility"
    },
    "voicingHintResponse": {
      "value": "Toggle to hide units"
    }
  }
}
```

## Disposal

Voicing adds listeners that enable speech from input events. When a Node using Voicing is no longer needed, call its
`dispose()` method to avoid memory leaks.

## Additional Resources

### Alt Input

Voicing is closely integrated with alternative input. Refer to the Alternative Input quickstart guide for that
implementation:
[Alternative Input Quickstart Guide](https://github.com/phetsims/phet-info/blob/main/doc/alternative-input-quickstart-guide.md).

### Core Description

Core Voicing complements Core Interactive Description. If you already support Interactive Description, much of your
voicing content will come “for free.” For details,
see [Core Description Quickstart Guide](https://github.com/phetsims/phet-info/blob/main/doc/core-description-quick-start-guide.md).