# Overview
PhET Simulations can be translated into many languages. The translated strings have many overlapping concerns, and must support the following features:

1. Visual and non-visual strings must be translatable.
2. Strings must appear as PhET-iO instrumented objects which can be changed at runtime.
3. Strings must support metadata, such as phetioReadOnly or phetioDocumentation.
4. Strings must be interoperable with Rosetta (the translation utility), so must be discoverable, editable, testable, storable, and maintenance-releasable.
5. Strings must be prunable, so that only specific strings used in a sim are shown in Rosetta.
6. Strings must be structured, so one object can have multiple "children" or recursively nested descendants, and so that strings can be grouped together in a way that makes sense for the sim.
7. Strings must support patterns/placeholders, and be translated into other languages in a grammatically correct way. This is important because grammatical incorrectness can create a barrier, dissonance, or confusion, and impede streamlined usage of the sim.

To this end, we have developed a custom string management system to address these concerns.

In order for patterns to be translatable in a grammatically correct way, we use Fluent, see https://projectfluent.org/. To support structuring and multiline values, we use YAML. To support Rosetta and backward compatibility, we output to the legacy JSON format. We preserve support for our legacy placeholder formats `{0}` and `{{myValue}}` for backward compatibility.

# Getting Started with YAML and Fluent
1. We do not currently have a script that converts the legacy sim_en.json files to YAML, that is currently a manual process.
2. To create a new YAML file, copy an existing one and change the name to match the sim name, e.g. `my-sim-en.yaml`.
3. For the YAML file, each value is either a constant, one of the legacy placeholders, or a Fluent pattern.
4. NOTE: YAML does not support newline `\n` escaped characters, but instead should be converted to a multiline string using the `|-` syntax. For example:
   ```yaml
   myMultilineString: |-
     This is a multiline string.
     It can have multiple lines.
   ```
5. Once the YAML file is created, run `grunt modulify` to autogenerate the json file, and the corresponding SimFluent.ts file.