# Overview

PhET Simulations can be translated into many languages. The string system relates to many overlapping parts, and must
support the following features:

1. Visual and non-visual strings must be translatable.
2. Strings must appear as PhET-iO instrumented objects which can be changed at runtime.
3. Strings must support metadata, such as phetioReadOnly or phetioDocumentation.
4. Strings must be interoperable with Rosetta (the translation utility), so must be discoverable, editable, testable,
   storable, and maintenance-releasable.
5. Strings must be prunable, so that only specific strings used in a sim are shown in Rosetta.
6. Strings must be structured, so one object can have multiple "children" or recursively nested descendants, and so that
   strings can be grouped together in a way that makes sense for the sim.
7. Strings must support patterns/placeholders, and be translated into other languages in a grammatically correct way.
   This is important because grammatical incorrectness can create a barrier, dissonance, or confusion, and impede
   streamlined usage of the sim.
8. There should be one way of doing things (as much as possible), while retaining backward compatibility with legacy
   string formats.
9. Type safety for constants and patterns.
10. Support for Axon Properties
11. Readability and maintainability of the string files, so that they are easy to read, understand, and modify by
    developers, designers, and can support hundreds of strings.
12. PhET-iO studio string autoselect, so strings can be automatically discovered in mouseover.

To this end, we have developed a custom string management system to address these concerns.

In order for patterns to be translatable in a grammatically correct way, we use Fluent. To support structuring and
multiline values, we use YAML. To support Rosetta and backward compatibility, we output to the legacy JSON format. We
preserve support for our legacy placeholder formats `{0}` and `{{myValue}}` for backward compatibility.

YAML and Fluent are new languages for our project, and you should dedicate time to learning them.

For YAML, we recommend reading
the [YAML specification](https://yaml.org/spec/1.2/spec.html), [YAML quick start guide](https://quickref.me/yaml.html) (
watch out for ads) for more details on YAML syntax. Note that YAML is whitespace sensitive, so indentation is important.

For Fluent, we recommend reading the [Fluent Project](https://projectfluent.org/), and experimenting with
the [Fluent Playground](https://projectfluent.org/play/) is a great resource for experimenting with Fluent patterns.
Note that we do not support 100% of Fluent syntax, such as attributes.

# Getting Started with YAML and Fluent

1. We do not currently have a script that converts the legacy sim_en.json files to YAML, that is currently a manual
   process.
2. For the YAML file, each value is either a constant, one of the legacy placeholders, or a Fluent pattern.
3. Once the YAML file is created, run `grunt modulify` to autogenerate the json file, and the corresponding SimFluent.ts
   file.
4. Note that once a sim has a {{simName}}_en.yaml file, the legacy {{simName}}_en.json file should be treated as a
   read-only build-artifact (created by the `grunt modulify` command), and should not be edited directly. To that end,
   it is recommended to exclude the legacy JSON file from the IDE project to avoid finding it is search results.
5. Set up your IDE to align the values for YAML. In WebStorm, this can be done by going to
   `Preferences > Editor > Code Style > YAML`, and setting the `Align values` option to `true`. This will help with
   readability and maintainability of the YAML files. You can also import the code style settings from
   phet-info/ide/idea/phet-idea-codestyle.xml
6. simMetadata can be provided via a `__simMetadata` key, see convertStringsYamlToJson.ts

# Syntax and Gotchas

1. YAML does not support newline `\n` escaped characters, but instead should be converted to a multiline string using
   the `|-` syntax. For example:
   ```yaml
   myMultilineString: |-
     This is a multiline string.
     It can have multiple lines.
   ```
2. Strings that start with curly braces or end with colons must be quoted:

```yaml
grabbedLigandResponseWithEmptyMembraneHintPattern: "{ a11y.grabbedLigandResponsePattern } Space to release. Add transport proteins."
```

3. A multiline block scalar needs to start with a space so that the fluent syntax is valid.