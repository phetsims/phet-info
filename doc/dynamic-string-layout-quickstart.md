# Dynamic Strings Layout Quickstart Guide

## Table of Contents

- First Steps
- PatternStringProperty
- Testing

### First Steps

Strings should be converted to `TReadOnlyProperty` instances. These properties are auto-generated in the strings file,
and every single usage case should be converted.

Certain components may need to be set to `resizable: true`. If you see that components are not resizing as expected,
this is a good place to start.

You can define support for dynamic locale in the package.json. It is recommended to wait until all strings have bring converted to use the `*stringProperty` from the strings file. If you know that you will not need to support dynamic locale for your publication, you can opt out in the package.json
like:

```json
{
  "simFeatures": {
    "supportsDynamicLocale": false
  }
}
```

### PatternStringProperty and DerivedStringProperty

For situations where a pattern string is needed generally use `PatternStringProperty`. This replaces the pattern where
we use `StringUtils.fillIn()`. Refer to `PatternStringProperty.ts`
for implementation documentation. There may be rare/specific situations where `PatternStringProperty` is not needed.
Also know that these are likely good cases for DerivedStringProperty, which should be used for i18n derived, non-pattern
strings. We prefer `DerivedStringProperty` to `DerivedProperty<string>` for PhET-iO consistency.

### Testing

**If your sim has been published and has translations:**

Run with `?locales=*` to enable the locale-testing button (globe) in the navigation bar. Open the locale dialog by
pressing the globe button in the navigation bar. Press and hold while moving the pointer over locale names. This changes
the locale. Watch for layout problems. Fix any layout problems that are identified. For example, if a Text node needs to
remain centered on something, then a boundsProperty listener may be needed.

**If you are working on an unpublished sim:**

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

CM tracked some useful roadblocks that came up during Natural Selection conversion
here: https://github.com/phetsims/natural-selection/issues/319
