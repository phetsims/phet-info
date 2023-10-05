# Prototype Checklist

This checklist includes a minimal list of tasks that should be completed before
a prototype version is published.

- [ ] Run with `stringTest=X` to verify that all strings are translatable. You should see nothing but 'X' strings in the
  running sim. This is important because prototypes are translatable.

- [ ] Inspect `{REPO}-strings_en.json` and verify that all string keys conform to [PhET string key conventions](https://github.com/phetsims/phet-info/blob/main/doc/string-key-conventions.md).
  String keys are difficult to change after a sim has been published, and they appear in the PhET-iO API (and Studio) as the
  phetioIDs for StringProperties.

- [ ] Verify that the About dialog shows appropriate credits. If a third party was involved, verify that they are 
  included in credits. See `SimOptions.credits` for how to specify credits.
