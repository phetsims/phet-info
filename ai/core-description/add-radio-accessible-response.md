## Radio Button Accessible Context Responses

Radio buttons announce a single “context response” after selection changes so users know what the newly selected option does. `AquaRadioButton`/`RectangularRadioButton` expose this via `accessibleContextResponse` (see `sun/js/AquaRadioButton.ts:61`), and `AquaRadioButtonGroup`/`RectangularRadioButtonGroup` simply pass those responses through. The same string is reused for Voicing context output unless you supply an override, so the guidance below keeps both modalities in sync.

### What the responses should say
- Describe the effect of the newly selected option, not the gesture (“Preset mode selected” is too vague). `beers-law-lab/js/beerslaw/view/LightModeRadioButtonGroup.ts:48` plays back “Light source wavelength set to …” so learners hear the updated wavelength plus its color range (string defined in `beers-law-lab/beers-law-lab-strings_en.json:489`).
- Include the minimum context needed to distinguish choices. `membrane-transport/js/common/view/MembranePotentialPanel.ts:35` derives responses like “Sodium-selective Voltage-gated, open.” / “Voltage-gated channels closed.” from `membrane-transport/membrane-transport-strings_en.yaml:590`, so the announcement tells which channels changed when the membrane potential shifted.
- Keep it short (one clause) and in present tense. Reserve extra detail for help text/paragraphs so the rapid feedback stays scannable. When qualitative names are helpful (e.g., “violet range” for wavelengths), append them after the quantitative value.

### Where to put the strings
1. Add the base message to `{sim}-strings_en.yaml` (or `.json` for legacy sims) under the relevant `a11y` section. For shared patterns, group them the way `beers-law-lab/beers-law-lab-strings_en.json:489` does in `a11y.sharedAccessibleContextResponses`.
2. If the statement needs live data, define placeholders/selector blocks in YAML or build a derived Property in code that stitches together existing localized strings. `MembranePotentialDescriber.createDescriptionStringProperty` (`membrane-transport/js/common/view/MembranePotentialDescriber.ts:12`) converts channel state changes into fluent strings instead of duplicating text inside each button.
3. Let perennial’s watcher regenerate `{sim}Strings.ts` and `{sim}Fluent.ts`; reference the generated string/Property rather than hard-coding text.

```yaml
a11y:
  sharedAccessibleContextResponses:
    presetWavelengthSet: Light source wavelength set to { $wavelength } { $units }, { $colorName } range.
```

### Hooking the responses up in code
1. **Per-button responses:** Pass the string Property directly in each item’s options. `beers-law-lab/js/beerslaw/view/DetectorModeRadioButtonGroup.ts:47` supplies two DerivedProperties—one describing transmittance with units, another describing absorbance—via the item’s `accessibleContextResponse`. The group handles layout; each button keeps its own announcement.
2. **Shared response for every button:** When the announcement logic depends on the selected value but not on which control triggered it (e.g., multiple widgets set the same property), provide a single Property through `radioButtonOptions.accessibleContextResponse`. `MembranePotentialPanel` shares `MembranePotentialDescriber.createDescriptionStringProperty( model )` with every membrane-potential button so whichever value you choose produces the same, fully contextual string.
3. **Don’t skip it:** If `accessibleContextResponse` is omitted, assistive tech will keep repeating whatever the last control said, which is misleading for mutually exclusive options. Always pair the response with a distinct accessible name and (if needed) help text.

### Implementation checklist
1. Decide what state change each radio option causes and summarize it in one clause (“Transmittance measured at 85 percent”). Capture any numeric values or qualitative tags users rely on.
2. Add the string/Fluent pattern to `{sim}-strings_en.yaml` (or `.json`) and wire it up through `{sim}Strings.ts`/`{sim}Fluent.ts`. Use placeholders or DerivedProperties when the value depends on live model data.
3. Reference the string Property via each item’s `accessibleContextResponse` (or via shared `radioButtonOptions`) when creating the `AquaRadioButtonGroup`/`RectangularRadioButtonGroup`.
4. Spot-check with a screen reader or Voicing: arrow through the group and confirm the announcement describes the selection’s effect and matches the updated visual state.
