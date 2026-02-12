# Conventions for naming string keys

This document described the naming conventions for string keys that appear in translated string files. It is important
to get these right before publication because keys are difficult to change after a sim has been published, and they
appear in the PhET-iO API (and Studio) as the phetioIDs for StringProperties.
_If you're unsure about these conventions, ask another PhET developer._

Guidelines:

(1) Strings keys should generally match their values. E.g.:

```json
  "gravityForce": {
"value": "Gravity Force"
},
"quadraticTerms": {
"value": "Quadratic Terms"
}
```

(2) String keys for screen names should have the general form `"screen.{{screenName}}"`. E.g.:

```json
    "screen.explore": {
"value": "Explore"
},
```

(3) If a string key would be exceptionally long, use a key name that is an abbreviated form of the string value, or that
captures the purpose/essence of the value. E.g.:

```js
  // key is abbreviated
"iWentToTheStore"
:
{
  "value"
:
  "I went to the store to get milk, eggs, butter, and sugar."
}
,

// key is based on purpose
"describeTheScreen"
:
{
  "value"
:
  "The Play Area is a small room. The Control Panel has buttons, a checkbox, and radio buttons to change conditions in the room."
}
```

(4) If string keys would collide, use your judgment to disambiguate them. E.g.:

```json
  "simplifyTitle": {
"value": "Simplify!"
},
"simplifyCheckbox": {
"value": "simplify"
}
```

(5) String patterns that contain placeholders should use keys that are unlikely to conflict with strings that might be
needed in the future. For example, for value `"The price is {{dollars}}"` consider using key `"pricePattern"`
or `"thePriceIsDollars"`
instead of `"price"`, if you think there might be a future need for a `"Price"` string value.

(6) It is acceptable to group related strings with a prefix, for example:

```json
  "material.brick": {
"value": "Brick"
},
"material.metal": {
"value": "Metal"
},
"material.plastic": {
"value": "Plastic"
},
"material.wood": {
"value": "Wood"
},
```

(7) For strings that begin with a number, the string key should also begin with a number. For example:

```json
  "3DHeight": {
"value": "3D Height"
},
```

## Accessibility strings and Internationalization

Accessibility strings are not yet translatable. However, plan for future translation by keeping string patterns simple
and avoiding multiple placeholders. Complex strings with multiple placeholders can create challenges for gender,
pluralization, and other grammatical rules when translated.

### Accessibility string key conventions

Accessibility strings should be placed under the `a11y` key in the strings.json file. This keeps them separate from
translatable strings (they are not yet translated).

It’s generally fine to reuse the same string for visual text and accessibility if the meaning is truly identical.
However, if the string is used in multiple contexts or has a different meaning, create a separate key to allow for
unique translations or messaging later.

It is recommended to use YAML files for accessibility strings. Using YAML allows for better organization, readability,
and more complicated string patterns that will eventually support translations. For more information about YAML and
Fluent, see
the [YAML/Fluent documentation](https://github.com/phetsims/phet-info/blob/main/doc/strings-i18n-yaml-fluent.md).

Use the following guidelines for naming and organization:

- Key structure:
  - Keys under the `a11y` key should be nested for readability.
  - Match key names to PhET-iO tandem names when possible. This keeps design, phet-io, and accessibility terminology
    aligned and makes usage easier to identify.
  - If a component has no tandem name, use the class or instance variable name.
  - If tandem terminology differs from description terminology, it is acceptable to use the description terminology.
  - Nested keys should use the option names in the code (e.g., accessibleName, accessibleHelpText,
    accessibleParagraph, etc.).
  - If a string needs multiple variants with unique values, nest them under the option key (see example below).
- For screen summary content, use the screen name as a key, then nest a screenSummary key, with playArea, controlArea,
  currentDetails, and interactionHint as sub-keys.
- Nest `screenButtonsHelpText` under the screen name.
- Prefer longer or duplicated strings over complex string patterns. This simplifies code and translation. Patterns often
  assume English-specific grammar.

Here is a documented example:

```yaml
a11y:

  # Tandem name is pushButtonGroup. Use that for the key name.
  pushButtonGroup:

    # Option names.
    accessibleHeading:  Actions
    accessibleHelpText: Choose action to take.

  # Match the tandem name for the button.
  eyeToggleButton:

    # Matching the option name.
    accessibleNameOn:

      # Different instances require a unique accessibleName.
      buttonA: Hide Object A
      buttonB: Hide Object B
      buttonC: Hide Object C
      buttonD: Hide Object D

    # Matching the option name.
    accessibleNameOff:

      # Different instances require a unique accessibleName.
      buttonA: Show Object A
      buttonB: Show Object B
      buttonC: Show Object C
      buttonD: Show Object D

    # Option names.
    accessibleHelpText:           Show or hide object.
    accessibleContextResponseOff: Object hidden.
    accessibleContextResponseOn:  Object shown.
      
  # Matching the tandem name for the checkbox.
  visibilityCheckbox:
    
    # Matching option names in the code.
    accessibleName:                     Units Visible
    accessibleHelpText:                 Toggle to hide all units in the simulation.
    accessibleContextResponseChecked:   Units are visible.
    accessibleContextResponseUnchecked: Units are hidden.

  # Example structure for screen summary content.
  screenA:
    screenButtonsHelpText: "Use a light source to explore the atom's energy states."
    screenSummary:
      playArea:        "Contains a light source and..."
      controlArea:     "Contains buttons and checkboxes that..."
      currentDetails:
        energyState: "Currently, the atom is in its {{level}} energy state."
        highest:     "highest"
        lowest:      "lowest"
      interactionHint: "Turn on light source to start exploring."

  # Example structure for component with no tandem. Imagine an instance variable "atom".
  atom:

    # Option names.
    accessibleName:      "Atom"
    accessibleParagraph: "Atom energy state: {{state}}."

    # Values for the {{state}} placeholder in the accessibleParagraph.
    highest:             "highest"
    lowest:              "lowest"
```