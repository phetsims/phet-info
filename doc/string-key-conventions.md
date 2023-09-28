# Conventions for naming string keys

This document described the naming conventions for string keys that appear in 
translated string files. It is important to get these right before publication 
because keys are difficult to change after a sim has been published, and they
appear in the PhET-iO API (and Studio) as the phetioIDs for StringProperties.

Guidelines:

(1) Strings keys should generally match their values. E.g.:

  ```js
  "helloWorld": {
    value: "Hello World!"
  },
  "quadraticTerms": {
    value: "Quadratic Terms"
  }
  ```

(2) If a string key would be exceptionally long, use a key name that is an abbreviated form of the string value, or
that captures the purpose/essence of the value. E.g.:

  ```js
  // key is abbreviated
  "iWentToTheStore": {
    value: "I went to the store to get milk, eggs, butter, and sugar."
  },

  // key is based on purpose
  "describeTheScreen": {
    value: "The Play Area is a small room. The Control Panel has buttons, a checkbox, and radio buttons to change conditions in the room."
  }
  ```
(3) If string key names would collide, use your judgment to disambiguate. E.g.:

  ```js
  "simplifyTitle": {
     value: "Simplify!"
  },
  "simplifyCheckbox": {
     value: "simplify"
  }
  ```

(4) String keys for screen names should have the general form `"screen.{{screenName}}"`. E.g.:

  ```js
    "screen.explore": {
      "value": "Explore"
    },
  ```

(5) String patterns that contain placeholders (e.g. `"My name is {{first}} {{last}}"`) should use keys that are
unlikely to conflict with strings that might be needed in the future. For example, for `"{{price}}"` consider using
key `"pricePattern"` instead of `"price"`, if you think there might be a future need for a `"price"` string.

(6) It is acceptable to group related strings with a prefix, like so:

```json
  "material.water": {
    "value": "Water"
  },
  "material.wood": {
    "value": "Wood"
  },
  "shape.block": {
    "value": "Block"
  },
  "shape.cone": {
    "value": "Cone"
  },
```

Note that nested substructure is not yet fully supported for string keys.