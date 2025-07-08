# Strings, i18n, YAML, and Fluent

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

To this end, we have developed a custom string management system to address these concerns.

In order for patterns to be translatable in a grammatically correct way, we use Fluent. To support structuring and
multiline values, we use YAML. To support Rosetta and backward compatibility, we output to the legacy JSON format. We
preserve support for our legacy placeholder formats `{0}` and `{{value}}` for backward compatibility.

**YAML and Fluent are new languages for our project, our team must dedicate time to learning them.**

For YAML, we recommend reading
the [YAML specification](https://yaml.org/spec/1.2/spec.html), [Learn YAML in Y minutes](https://learnxinyminutes.com/yaml/),
[YAML quick start guide](https://quickref.me/yaml.html) (watch out for ads) for more details on YAML syntax. Note that
YAML is whitespace sensitive, so indentation is important.

For Fluent, we recommend reading the [Fluent Project](https://projectfluent.org/), and experimenting with
the [Fluent Playground](https://projectfluent.org/play/) is a great resource for experimenting with Fluent patterns.
Note that we do not support 100% of Fluent syntax, such as attributes. Note that Fluent is also whitespace sensitive, so
its own indentation is also important.

NOTE: Due to numerous technical constraints, we are not writing full Fluent *.ftl files, but rather using a subset of
Fluent syntax in YAML files. In the future, if we abandon the legacy JSON format and some of the related constraints, we
may be able to use full Fluent format.

NOTE: Rosetta does not yet support translating Fluent fragments, so please do not use Fluent patterns in the visual
strings. If you need a pattern in the visual strings, please use the legacy `{{value}}` pattern for now.

NOTE: When porting a legacy sim's JSON to YAML, you should preserve the placeholder syntax as it was. Sim code and
translations cannot be seamlessly transitioned to Fluent patterns without significant effort. So you can consider the
Fluent syntax for new strings, or when it is important to redo legacy pattern strings.

# Getting Started with YAML and Fluent

1. We do not currently have a script that converts the legacy {{REPO}}-strings_en.json files to YAML. That is currently a manual
   process.
2. For the YAML file, each value is either a constant, one of the legacy placeholders, or a Fluent pattern.
3. Once the YAML file is created or edited, run `grunt modulify --targets=strings` to autogenerate the JSON file, and
   the corresponding {{REPO}}Fluent.ts file.
4. Note that once a sim has a {{REPO}}-strings_en.yaml file, the legacy {{REPO}}-strings_en.json file should be treated as a
   read-only build artifact (created by the `grunt modulify` command), and should not be edited directly. To that end,
   it is recommended to exclude the legacy JSON file from the IDE project to avoid finding it is search results.
5. Set up your IDE to align the values for YAML. In WebStorm, this can be done by going to
   `Preferences > Editor > Code Style > YAML`, and setting the `Align values in maps` option to `value`. This will help
   with readability and maintainability of the YAML files. You can also achieve this by importing the Code Style
   settings from phet-info/ide/idea/phet-idea-codestyle.xml

# Syntax and Gotchas

1. YAML does not support newline `\n` escaped characters, but instead should be converted to a multiline string using
   the `|-` syntax. For example:
   ```yaml
   myMultilineString: |-
     This is a multiline string.
     It can have multiple lines.
   ```

Please note that this is just one of many syntax options for multiline strings, and the syntax may be different depending on your multiline
string.

2. Fluent and YAML are both whitespace sensitive, and in Fluent, subsequent lines must be indented. In this example, note the indent on the Data Values and Median lines:

```yaml
   accessibleParagraph: |-
   Median is the number that splits a sorted data set in half.
     
     Data Values (in meters): {$values}
     Median = {$median}
```

3. Strings that start with curly braces or end with colons must be quoted:

```yaml
grabbedLigandResponseWithEmptyMembraneHintPattern: "{ a11y.grabbedLigandResponsePattern } Space to release. Add transport proteins."
```

4. A multiline block scalar needs to start with a space so that the Fluent syntax is valid.
5. simMetadata can be provided via a `__simMetadata` key, see convertStringsYamlToJson.ts
6. Normally YAML values parse as non-string primitives, such as `true`, `false`, `yes`, `no`, and `null`. To ensure that
   these values are treated as strings, our system uses `FAILSAFE_SCHEMA` to ensure that all values are treated as
   strings.
7. chipper and scenerystack also provide direct support for *.ftl files, but this is not recommended for PhET
   simulations, as it does not support the same features as the YAML system, such PhET-iO support, Rosetta integration,
   etc. It is recommended to use the YAML system for all PhET simulations.
8. When used with RichText, you can use HTML markup as needed. But keep in mind that this is a burden for translators, so use
   markup sparingly.

# Implementation Notes

The conversion from YAML to JSON and Fluent processing during the modulify build step is handled by a sophisticated
pipeline that preserves type-safety while enabling internationalization. When `grunt modulify --targets=strings` is
executed, the system first checks for the existence of a {{REPO}}-strings_en.yaml file. If found, it processes this file
using the js-yaml library with a FAILSAFE_SCHEMA to ensure all values are preserved as strings (preventing automatic
type conversion of values like "true" or "null"). The conversion transforms the flat YAML structure by nesting string
values under a `"value"` key (e.g., `"text"` becomes `{ "value": "text" }`), handles special `__simMetadata` keys by merging
them as simMetadata properties, and processes Fluent references by converting dot notation to underscores for
compatibility with PhET's naming conventions.

After JSON generation, the system creates TypeScript type definitions and Fluent objects through generateFluentTypes.ts.
This process analyzes the YAML structure to distinguish between simple constant strings and parameterized patterns,
generating FluentConstant objects for basic strings and FluentPattern objects for strings with variables. The system
maintains backward compatibility by detecting legacy placeholder patterns (`{0} and `{{value}}`) and handling them
separately from modern Fluent syntax (`{ variable }`). The resulting artifacts include the auto-generated JSON file for
Rosetta compatibility, TypeScript modules with proper typing for development, and Fluent message objects that support
runtime string resolution with proper parameterization. This architecture enables PhET simulations to leverage modern
internationalization practices while preserving the existing toolchain and translation workflow.

# References

1. Please refer to membrane-transport-strings_en.yaml for an example of a YAML file.
