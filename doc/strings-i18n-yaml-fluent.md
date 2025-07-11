# Strings, i18n, YAML, and Fluent

## 1. Purpose

This document is a quickstart guide for developers on how to use PhET's YAML/Fluent-based internationalization (i18n)
system. Its goal is to answer:

* How do I use this system to localize a simulation?
* How do I convert a simulation from the legacy JSON-based system?
* What are the key APIs and workflows?

This system was introduced to support more powerful and grammatically correct translations, especially for complex
strings with placeholders.

### Core Concepts: YAML and Fluent

The new system uses two languages:

* **YAML**: Provides the **structure** for the string files. It organizes strings into a nested, readable, key-value
  format.
* **Fluent**: Provides the **syntax for the string values**. It is a powerful localization system designed for
  natural-sounding translations, especially for strings with dynamic parts (placeholders).

In short: **YAML is the container, and Fluent provides the content.**

## 2. The Old System vs. The New System

Here is a comparison of the artifacts and APIs for both systems.

### The Legacy System (JSON-based)

* **Source File**: `{{REPO}}-strings_en.json`
* **Generated Artifacts**: Running `grunt modulify` creates `{{REPO}}Strings.ts`.
* **API**:
  * `{{REPO}}Strings.ts` contains `LocalizedStringProperty` instances for all strings.
  * For patterns, developers used `PatternStringProperty`, `StringUtils.fillIn`, or `StringUtils.format` with
    `{{placeholder}}` or `{0}` style placeholders.

### The New System (YAML/Fluent-based)

* **Source File**: `{{REPO}}-strings_en.yaml` (this is the single source of truth).
* **Generated Artifacts**: Running `grunt modulify --targets=strings` creates:
  1. `{{REPO}}-strings_en.json`: A JSON version for backward compatibility with the Rosetta translation tool. **This
     file is a build artifact and should not be edited directly.**
  2. `{{REPO}}Strings.ts`: Preserved for backward compatibility, allowing for gradual refactoring. It contains the same `LocalizedStringProperty` instances as the old system.
  3. `{{REPO}}Fluent.ts`: The primary file for development. It contains typed objects for interacting with your strings.
* **API**:
  * `FluentConstant`: For simple, static strings. It is a `TReadOnlyProperty<string>`. Found in `{{REPO}}Fluent.ts`. A FluentConstant does not have any external inputs, though it may cross-reference other variables within the fluent file.
  * `FluentPattern`: For strings with placeholders. Found in `{{REPO}}Fluent.ts`.
    * `FluentPattern.createProperty(...)`: Creates a reactive `TReadOnlyProperty<string>` that automatically updates
      when its placeholder values (which can be other Properties) change.
    * `FluentPattern.format(...)`: A static function to format a string once with a given set of values.
  * `FluentConstant` is generated from the YAML `#` comments, so that we can access the comments at runtime, for display in tooling.

## 3. How to Convert a Simulation to YAML/Fluent

Follow these steps to migrate a sim from the legacy JSON system.

**Step 1: Create the YAML file**

From your sim's root directory, run:

```bash
grunt create-yaml
```

This command reads your existing `{{REPO}}-strings_en.json` file and creates a new `{{REPO}}-strings_en.yaml` file. This automates the initial conversion.

**Step 2: Generate the new artifacts**

Next, run `modulify` to generate the JSON, `...Strings.ts`, and `...Fluent.ts` files from your new YAML file:

```bash
grunt modulify --targets=strings
```

**Step 3: Verify backward compatibility**

After running `modulify`, check that `{{REPO}}Strings.ts` has not changed. This is important because it confirms that
the conversion has not broken any existing string usages, allowing you to refactor gradually.

**Step 4: Refactor code to use the Fluent API**

Now you can begin updating your sim's code to use the new, more powerful API from `{{REPO}}Fluent.ts`.

* **For constant strings**:
  * **Old:** import from `'{{REPO}}Strings.js'` this gives LocalizedStringProperty instances.
  * **New:** import from `{{REPO}}Fluent.js` this gives `FluentPattern | FluentConstant` instances.

* **For pattern strings**:
  * **Old:** `new PatternStringProperty( somePatternStringProperty, { ... } )` or `StringUtils.fillIn(...)`
  * **New:** import from `'{{REPO}}Fluent.js';`
    * Use `somePattern.createProperty( { ... } )` to create a reactive Property.
    * Use `somePattern.format( { ... } )` to format the string once.

## 4. Practical Usage and Syntax ("Implementation Patterns")

Here are examples of how to write strings in your `.yaml` file and use them in code.

### YAML: The Structure

PhET uses a small subset of YAML's features. The most important concept is that **indentation creates nesting**.

```yaml
# parent is a key
parent:
  # child is nested under parent because it is indented
  child: 'Some string value'
```

For readability, we recommend configuring your IDE to align values in maps. In WebStorm, this is
`Settings > Editor > Code Style > YAML > Align values in maps`.

### Fluent: The Content

Examples below show how to write strings in Fluent syntax, which is used for both constant strings and patterns.  Note that we do not support 100% of Fluent syntax, such as attributes.

#### Constant Strings

A simple key-value pair.

```yaml
# In {{REPO}}-strings_en.yaml
myCoolButton: 'My Cool Button'

# In code
import MyRepoFluent from '{{REPO}}Fluent.js';
const button = new PushButton( MyRepoFluent.myCoolButton, { ... } );
```

##### More Constant Examples from membrane-transport

```yaml
# Simple constants
solutes:                     Solutes
outside:                     Outside
inside:                      Inside

# Constants with HTML formatting
oxygen:                      O<sub>2</sub>
carbonDioxide:               CO<sub>2</sub>
sodiumIon:                   Na<sup>+</sup>
potassiumIon:                K<sup>+</sup>

# Longer descriptive constants
animateLipidsDescription:    Whether the phospholipids forming the cell membrane should be animated.
glucoseMetabolismDescription: Glucose fades from the inside of the cell. Barcharts display constant high concentration of glucose inside the cell.
```

#### Pattern Strings (Placeholders)

Use `{ $variableName }` for placeholders. The spacing is flexible: `{ $value }`, `{$value}`, and `{ $value}` are all equivalent.

```yaml
# In {{REPO}}-strings_en.yaml
valueLabelPattern: 'Value: { $value }'

# In code
import MyRepoFluent from '{{REPO}}Fluent.js';

const valueProperty = new NumberProperty( 5 );

// Create a reactive Property that updates when valueProperty changes
const labelProperty = MyRepoFluent.valueLabelPattern.createProperty( { value: valueProperty } ); // "Value: 5"

// Or format it once
const labelString = valueLabelPattern.format( { value: 10 } ); // "Value: 10"
```

##### Simple Pattern Examples from membrane-transport

```yaml
# Basic patterns with single variables
accessibleName:     "{ a11y.soluteCapitalized } Outside Cell"
accessibleName:     "{ a11y.soluteCapitalized } Inside Cell"

# Patterns with cross-references to other Fluent strings
initialResponse:    "{ a11y.soluteCapitalized } crossing membrane, { a11y.soluteConcentrationsAccordionBox.barChart.comparison }."
```

#### Fluent Selectors (Pluralization and Conditionals)

Fluent's most powerful feature is selectors, which allow for grammatically correct translations based on variable values. This is especially important for pluralization and conditional text.

##### Basic Pluralization Examples from membrane-transport

```yaml
# Simple pluralization with count
soluteTypesOnOutside: |-
  { $count ->
    [one] { $count } solute type on outside
   *[other] { $count } solute types on outside
  }

soluteTypesOnInside: |-
  { $count ->
    [one] { $count } solute type on inside
   *[other] { $count } solute types on inside
  }
```

##### Conditional Selectors from membrane-transport

```yaml
# Conditional text based on enum values
membranePotentialValue: |-
  { $membranePotential ->
    [-70] negative 70
    [-50] negative 50
    *[30] positive 30
  } millivolts

# Conditional text for different amounts
accessibleObjectResponse: |-
  { $amount ->
    [none] no
    [few] a few
    [some] some
    [smallAmount] small amount of
    [several] several
    [many] many
    [largeAmount] large amount of
    [hugeAmount] huge amount of
    *[maxAmount] max amount of
  } { a11y.solute }
```

##### Reusable Selectors with Cross-References

```yaml
# A multiline selector defined once, then reused elsewhere
a11y:
  # Capitalized names for the solute type. Reused in various places.
  soluteCapitalized:      |-
                          { $soluteType ->
                            [oxygen]        Oxygen Molecules
                            [carbonDioxide] Carbon Dioxide molecules
                            [sodiumIon]     Sodium Ions
                            [potassiumIon]  Potassium Ions
                            [glucose]       Glucose Molecules
                           *[atp]           Atp Molecules
                          }
  myLabel:
    accessibleName:     "{ a11y.soluteCapitalized } Outside Cell"
```

#### Complex Pattern Examples

These examples demonstrate advanced Fluent features combining multiple variables, cross-references, and complex conditional logic.

##### Multi-Variable Complex Patterns from membrane-transport

```yaml
# Complex pluralization with multiple variables
transportProteins: |-
  { $proteinCount ->
    [one] { $proteinCount} transport protein
    *[other] { $proteinCount} transport proteins
  } of { $proteinTypeCount ->
    [one] { $proteinTypeCount } type
   *[other] { $proteinTypeCount} types
  }, in membrane

# Complex pattern with multiple variables and cross-references
accessibleContextResponse: |-
  { $amount ->
    [aLittle] A little
    *[aLot]    A lot
  } { $addedOrRemoved ->
    [added]   added
    *[removed] removed
  }. Now,
  { $moreOrLessOrSameOrNone ->
    [none] no { a11y.solute } outside or inside.
    [same] same amount of solute inside and outside.
    *[other] { $differenceSize ->
      [aLittle] a little
     *[aLot]    a lot
    }
    { $moreOrLessOrSameOrNone ->
      [more] more
     *[less] less
    }
    { a11y.solute }
    { $directionality ->
      [insideThanOutside] inside than outside
     *[outsideThanInside] outside than inside
    }.
  }
```

> **IMPORTANT**: Currently, Fluent syntax (e.g., `{ $variable }`) should **only** be used for strings under the `a11y`
> key. Rosetta, our translation tool, does not yet support Fluent syntax for visual strings. For any visual string that
> requires a placeholder, you must continue to use the legacy `{{placeholder}}` syntax.

#### Multiline Strings

Use `|-` for multiline strings. In Fluent, subsequent lines of a single message must be indented.

```yaml
# Note the indentation on the second and third lines
myMultilineString: |-
  This is the first line.
   This is the second line.
   This is the third line.
```

##### Multiline Examples from membrane-transport

```yaml
# Simple multiline descriptive text
intro: |-
  An observation window zooms in on a cross-section of a cell's membrane.
    The membrane consists of a wiggling phospholipid bilayer, a double-layered sheet
    that separates fluids inside and outside of cell. When added to outside or inside,
    solute particles are suspended in fluid and randomly move with Brownian motion.

# Multiline accessibility help text
accessibleHelpText: |-
  Add up to 7 proteins to membrane. Use keyboard shortcuts to grab, sort,
    and release proteins into membrane.

# Multiline with Fluent selectors
accessibleName: |-
  { $ligandType ->
    [starLigand]     Star Ligand
    *[triangleLigand] Triangle Ligand
  }

# Complex multiline with multiple conditional branches
accessibleHelpText: |-
  Membrane potential is { a11y.membranePotentialValue }. Proteins in membrane, {$typeCount ->
    [one] { $typeCount } type
    *[other] { $typeCount } types
  }. Look for Solute Controls to add or remove solutes types.
```

#### Quoting

You must quote strings that start with `{` or end with `:`.

```yaml
myQuotedString: '{ a11y.somePattern } is a pattern.'
```

#### Nesting Styles

You will see two different key styles in `.yaml` files. This is a convention based on how strings are organized.

1.  **Dot-notation keys (for UI strings)**: Used for most strings outside of the `a11y` tree.
    ```yaml
    screen.home.title: 'My Sim'
    ```
2.  **Indented keys (for a11y strings)**: Used for descriptive `a11y` strings for readability.
    ```yaml
    a11y:
      section:
        description: 'This is an accessible description.'
    ```

The dot-notation style is currently required outside of the `a11y` subtree, and the nested style
is preferred within the `a11y` subtree.

#### Metadata (`__simMetadata`)

You can add metadata like `phetioDocumentation` or `phetioReadOnly` using the `__simMetadata` key.

```yaml
myString:
  value: 'Some Value'
  __simMetadata:
    phetioDocumentation: 'This is documentation for PhET-iO.'
    phetioReadOnly: true
```

## 5. Syntax and Gotchas

* **Newlines**: YAML does not support the `\n` escape character for newlines. Use the `|-` multiline syntax instead (see
  the "Multiline Strings" example above).
* **IDE Configuration**: It is highly recommended to exclude the generated `{{REPO}}-strings_en.json` file from your
  IDE's project view. This prevents it from appearing in search results, ensuring you always edit the authoritative
  `.yaml` file.
* **Direct `.ftl` support**: While `chipper` and `scenerystack` have some direct support for `.ftl` files, the
  YAML-based system described here is the standard for PhET simulations, as it integrates with PhET-iO, Rosetta, and
  other required features.
* **HTML in RichText**: You can use HTML markup in strings that will be displayed with `RichText`. However, be aware
  that this increases the complexity for translators, so use it sparingly.

## 6. Tooling and Workflow

* `grunt create-yaml`: Converts a legacy `...-strings_en.json` file to `...-strings_en.yaml`.
* `grunt modulify --targets=strings`: Generates all derived string artifacts from the YAML source file.
* **Rosetta**: The translation tool has **not changed**. It continues to read from and write to the auto-generated `{{REPO}}-strings_en.json` file. Translators will not see or edit YAML/Fluent files directly.
* **Linting**: A lint rule (`phet/require-fluent`) exists to help enforce the use of the new Fluent API where appropriate. See membrane-transport/eslint.config.mjs for an example of how to enable it.

## 6. What is `FAILSAFE_SCHEMA`?

You may see `FAILSAFE_SCHEMA` mentioned in the build tools. This is a technical detail of the YAML parser configuration. It ensures that all values in the `.yaml` file (like `true`, `no`, `null`, or `1.0`) are treated as strings, preventing the parser from automatically converting them to booleans, numbers, or other types. You do not need to do anything about this; it's handled automatically by the build process.

## 7. Further Reading

* For a complete, real-world example, see `membrane-transport/membrane-transport-strings_en.yaml`.
* For YAML, we recommend reading
the [YAML specification](https://yaml.org/spec/1.2/spec.html), [Learn YAML in Y minutes](https://learnxinyminutes.com/yaml/),
[YAML quick start guide](https://quickref.me/yaml.html) (watch out for ads) for more details on YAML syntax.
* For Fluent, we recommend reading the [Fluent Project](https://projectfluent.org/), and experimenting with
the [Fluent Playground](https://projectfluent.org/play/) is a great resource for experimenting with Fluent patterns.

## Appendix 1. Requirements for PhET's i18n Concerns

PhET Simulations can be translated into many languages. The string system relates to many overlapping parts, and must
support the following features:

1. Visual and non-visual strings must be translatable.
2. Strings must support patterns/placeholders, and be translated into other languages in a grammatically correct way.
   This is important because grammatical incorrectness can create a barrier, dissonance, or confusion, and impede
   streamlined usage of the sim.
3. There should be one way of doing things (as much as possible), while retaining backward compatibility with legacy
   string formats.
4. Support for Axon Properties. This means the resultant strings should implement `TReadOnlyProperty<string>`, and
   pattern-based strings should accept `string` or `TReadOnlyProperty<string>` parameters.
5. Type safety for constants and patterns. This includes but is not limited to string literal unions for selector types.
6. Readability and maintainability of the string files, so that they are easy to read, understand, and modify by
   developers, designers, and can support hundreds of strings.
7. Strings must be structured, so one object can have multiple "children" or recursively nested descendants, and so that
   strings can be grouped together in a way that makes sense for the sim.
8. Strings must be interoperable with Rosetta (the translation utility), so must be discoverable, editable, testable,
   storable, and maintenance-releasable.
9. Strings must be prunable, so that only specific strings used in a sim are shown in Rosetta. For instance, if a sim
   does not have a FaucetNode, then the FaucetNode strings should not be shown in Rosetta.
10. Strings must appear as PhET-iO instrumented objects which can be changed at runtime.
11. Strings must support metadata, such as phetioReadOnly or phetioDocumentation.
12. Strings must be selectable using PhET-iO Studio string autoselect, so strings can be automatically discovered in
    mouseover. This is necessary for constant strings, and not required for pattern strings.

## Appendix 2. Implementation Notes

The conversion from YAML to JSON and Fluent processing during the modulify build step is handled by a sophisticated
pipeline that preserves type-safety while enabling internationalization. When `grunt modulify --targets=strings` is
executed, the system first checks for the existence of a {{REPO}}-strings_en.yaml file. If found, it processes this file
using the js-yaml library with a FAILSAFE_SCHEMA to ensure all values are preserved as strings (preventing automatic
type conversion of values like "true" or "null"). The conversion transforms the flat YAML structure by nesting string
values under a `"value"` key (e.g., `"text"` becomes `{ "value": "text" }`), handles special `__simMetadata` keys by
merging them as simMetadata properties, and processes Fluent references by converting dot notation to underscores for
compatibility with PhET's naming conventions.

After JSON generation, the system creates TypeScript type definitions and Fluent objects through generateFluentTypes.ts.
This process analyzes the YAML structure to distinguish between simple constant strings and parameterized patterns,
generating FluentConstant objects for basic strings and FluentPattern objects for strings with variables. The system
maintains backward compatibility by detecting legacy placeholder patterns (`{0}` and `{{value}}`) and handling them
separately from modern Fluent syntax (`{ $variable }`). The resulting artifacts include the auto-generated JSON file for
Rosetta compatibility, TypeScript modules with proper typing for development, and Fluent message objects that support
runtime string resolution with proper parameterization. This architecture enables PhET simulations to leverage modern
internationalization practices while preserving the existing toolchain and translation workflow.
