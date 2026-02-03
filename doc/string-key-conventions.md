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
  "iWentToTheStore": {
    "value": "I went to the store to get milk, eggs, butter, and sugar."
  },

  // key is based on purpose
  "describeTheScreen": {
    "value": "The Play Area is a small room. The Control Panel has buttons, a checkbox, and radio buttons to change conditions in the room."
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
