# Prototype Checklist

This checklist includes minimal list of things that should be completed before
a prototype version is published.

- [ ] Run with `stringTest=X` to verify that all strings are translatable. You should see nothing but 'X' strings in the
  running sim. This is important because prototypes are translatable.

- [ ] Inspect `${REPO}-strings_en.json` and verify that all string keys conform to PhET guidelines. String keys are
  difficult to change after a sim has been published, and they appear in the PhET-iO API (and Studio) as the phetioIDs 
  for StringProperties. Guidelines can be found in the
 [CRC](https://github.com/phetsims/phet-info/blob/main/checklists/code-review-checklist.md) - search for 
 "Guidelines for string keys".

- [ ] Verify that the About dialog shows appropriate credits. If a third party was involved, verify that they are 
  included in credits. See `SimOptions.credits` for how to specify credits.
