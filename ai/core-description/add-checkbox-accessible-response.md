## Checkbox Accessible Context Responses

PhET checkboxes announce a short “context response” immediately after a toggle so that screen reader and Voicing users know what changed. `Checkbox` defaults to the provided `accessibleContextResponseChecked`/`accessibleContextResponseUnchecked` (see `sun/js/Checkbox.ts`) and also reuses them for Voicing context responses, so getting these strings right benefits every modality.

### What the responses should say
- Describe the state of the visualization **after** the toggle, not the action the user took. Keep the statement short, declarative, and scoped to what the checkbox controls (e.g., “Tick marks labeled.” instead of “You checked the tick marks checkbox.”).
- Mention the specific objects that appear/disappear so the response stands on its own. Example strings in `number-pairs/number-pairs-strings_en.yaml:411`–`420` describe which annotations are shown on the number line (“Addends are { $leftAddend } and { $rightAddend }, labeled on number line.”) and what hides when unchecked (“Total jump not shown.”).
- Use present tense and avoid redundant wording. `forces-and-motion-basics/forces-and-motion-basics-strings_en.yaml:235`–`248` shows the preferred pattern: “Applied force arrow shown.” / “Applied force arrow hidden.”
- Provide only the context necessary to understand the change. If extra qualifiers are important (e.g., where something is added), include them succinctly (“Stopwatch added to Play Area.” in `forces-and-motion-basics-strings_en.yaml:243`).

### Where to put the strings
1. Add both responses to the sim’s `{sim}-strings_en.yaml` near the checkbox’s other a11y strings. Nest under the same logical section so `Fluent` keys match existing naming conventions.
2. When the response needs dynamic data, declare placeholders and document them in the YAML entry just like other Fluent strings (see `{ $leftAddend }` and `{ $rightAddend }` in `number-pairs-strings_en.yaml:411`).
3. The perennial string watcher will regenerate `{sim}Strings.ts` and `{sim}Fluent.ts` automatically after the YAML edit; no manual JSON edits are needed.

```yaml
a11y:
  controls:
    addendsCheckbox:
      accessibleContextResponseChecked:   Addends are { $leftAddend } and { $rightAddend }, labeled on number line.
      accessibleContextResponseUnchecked: Addends hidden.
```

### Hooking the responses up in code
1. Import the generated Fluent string properties and pass them to the checkbox options:
   - `number-pairs/js/common/view/NumberLineCheckboxItems.ts:23`–`38` shows passing a `FluentValue` with placeholders to `accessibleContextResponseChecked` and the static unchecked property for the “Addends” checkbox.
   - `forces-and-motion-basics/js/motion/view/MotionControlPanel.ts:160`–`257` demonstrates the same pattern inside a `VerticalCheckboxGroup`, sometimes pairing a derived description property for the checked response (e.g., `this.sumOfForcesDescriptionProperty`) with a static unchecked string when the “visible” state depends on live data.
2. When the checked response needs live values, use a `DerivedProperty` or the Fluent helper’s `.createProperty` to supply the parameters (see `createAddendsCheckboxItem` in `NumberLineCheckboxItems.ts`).
3. Pass both responses wherever a `Checkbox` is instantiated—directly or via helpers like `VerticalCheckboxGroupItem.options`—so each toggle announces the new state. Omitting one leaves the last announcement cached, which confuses assistive technologies.

### Implementation checklist
1. Decide what the user needs to know when the checkbox turns on/off. Summarize the resulting visual/aural change in one clause per response.
2. Add the Fluent strings (checked + unchecked) to `{sim}-strings_en.yaml`, including placeholders for any dynamic values.
3. Reference the generated string properties from code and connect them through `Checkbox` options (or `VerticalCheckboxGroupItem.options`) for both states.
4. Test with a screen reader or Voicing to confirm that toggling the checkbox produces the expected announcement and that the wording matches the updated UI.
