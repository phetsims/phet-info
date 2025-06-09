# Dynamic Strings Layout Quickstart Guide

## Table of Contents

- First Steps
- PatternStringProperty
- Dynamic Layout
- Testing
- Final steps

### First Steps

String lookups should be changed to the `*StringProperty` suffix, e.g. `someSimStrings.something` to 
`someSimStrings.somethingStringProperty`. These are auto-generated`TReadOnlyProperty<string>` instances that will 
dynamically update when the locale changes, and every single usage of string accesses of this form should be converted.

Any code that relied on these being a `string` should be refactored to be dynamic, and to accept a
`TReadOnlyProperty<string>`. This should happen all the way to the displayed `Text` Nodes, which can take a
`TReadOnlyProperty<string>` as a constructor argument (or as a `stringProperty` option).

Certain components may need to be set to `resizable: true`. If you see that components are not resizing as expected,
this is a good place to start.

You can define support for dynamic locale in the package.json. It is recommended to wait until all strings have been 
converted to use the `*stringProperty` from the strings file. If you know that you will not need to support dynamic 
locale for your publication, you can opt out in the package.json
like:

```json
{
  "simFeatures": {
    "supportsDynamicLocale": false
  }
}
```

### PatternStringProperty and DerivedStringProperty

For situations where a pattern string is needed, generally use `PatternStringProperty`. This replaces the pattern where
we use `StringUtils.fillIn()`. Refer to `PatternStringProperty.ts`
for implementation documentation. There may be rare/specific situations where `PatternStringProperty` is not needed.
Also know that these are likely good cases for DerivedStringProperty, which should be used for i18n derived, non-pattern
strings. We prefer `DerivedStringProperty` to `DerivedProperty<string>` for PhET-iO consistency.

### Dynamic Layout
Sizable components found in both Scenery and Sun support dynamic strings in sims. Familiarize yourself with the 
[Scenery Layout Documentation](https://scenerystack.org/learn/scenery-layout/) to learn more about sizable components and how they can help you create a dynamic 
and robust layout architecture for your sim. It is recommended to use these components instead of listening to 
`BoundsProperty`.

### Testing
Use the `stringTest=dynamic` query parameter to change all the strings in your sim at once. `DynamicStringTest` uses a
keyboard event listener to adjust the length of strings with the arrow keys and space bar. For more specific usage info
refer to [DynamicStringTest](https://github.com/phetsims/joist/blob/main/js/DynamicStringTest.ts) documentation. This
tool will allow you to see if dynamic layout is working as anticipated, and that components are resizing as would be
expected. Strings will only change if they have been implemented with a `TReadOnlyProperty` from the strings file.

### Final Steps

To support dynamic locales in your sim update your `package.json` with:

```json
{
  "simFeatures": {
    "supportsDynamicLocale": true
  }
}
```

This will create a Typescript error if the old style of strings is used, forcing you to access i18n strings via
the `*StringProperty` key. 

Also make sure to run `grunt update`.

CM tracked some useful roadblocks that came up during Natural Selection conversion
here: https://github.com/phetsims/natural-selection/issues/319
