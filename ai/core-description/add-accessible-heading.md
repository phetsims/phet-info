### Goal
Create a heading that screen readers can use to describe a logical section of the PDOM such as a description block, control group, or button set.

### 1. Add the heading string in the sim’s Fluent YAML
1. Open the sim’s `{sim}-strings_en.yaml`.
2. Add `accessibleHeading` (or a selector pattern) under the relevant `a11y` subgroup so that it sits next to the rest of the copy for that section.
3. Keep headings concise; they are announced each time the user enters the region.

Examples  
`number-pairs/number-pairs-strings_en.yaml`  
```yaml
a11y:
  countingArea:
    accessibleHeading: Counting Area
```
`forces-and-motion-basics/forces-and-motion-basics-strings_en.yaml```  
```yaml
a11y:
  motionScreen:
    playAreaControls:
      appliedForceControl:
        accessibleHeading: Applied Force Control
```
The perennial watcher regenerates `*Strings.ts` and `*Fluent.ts` automatically, so no manual build step is needed after saving the YAML.

### 2. Reference the new string from code
1. Import the sim’s Fluent module (e.g., `NumberPairsFluent`, `ForcesAndMotionBasicsFluent`).
2. Pass the associated `accessibleHeading` property to the `Node` (or control class) that represents the logical section.  
   - If the heading text is static, use the generated `...accessibleHeadingStringProperty`.  
   - If the heading varies (e.g., per challenge type), call `.accessibleHeading.createProperty( { ... } )` with the variants.
3. The heading typically lives on a `Node` with `tagName: 'div'` that wraps the child nodes the user will explore—yes, nesting a wrapper `Node` is the right approach if the widget itself cannot accept the heading option.

Examples  
`number-pairs/js/common/view/description/CountingAreaDescriptionNode.ts`  
```ts
const options = optionize<...>()( {
  accessibleHeading: NumberPairsFluent.a11y.countingArea.accessibleHeadingStringProperty,
  children: [ countingAreaAccessibleListNode, numberLineDescription ]
}, providedOptions );
```
`number-pairs/js/game/view/AnswerButtonGroup.ts` (dynamic heading)  
```ts
accessibleHeading: NumberPairsFluent.a11y.gameScreen.answerButtonGroup.accessibleHeading.createProperty( {
  challengeType: challengeTypeProperty
} ),
```
`forces-and-motion-basics/js/motion/view/MotionScreenView.ts` (wrapping Node)  
```ts
const appliedForcePlayAreaControlNode = new Node( {
  tagName: 'div',
  accessibleHeading: ForcesAndMotionBasicsFluent.a11y.motionScreen.playAreaControls.appliedForceControl.accessibleHeadingStringProperty,
  descriptionContent: ForcesAndMotionBasicsFluent.a11y.motionScreen.playAreaControls.appliedForceControl.descriptionStringProperty,
  children: [ appliedForceControl ]
} );
```

### 3. Keep the PDOM structure coherent
- Group related elements under the heading wrapper so the heading precedes the content in reading order.
- When adding a wrapper Node, forward `tandem`, `visibleProperty`, and other important options so instrumentation still works.
- If you already extend a class that exposes `AccessibleOptions`, set `accessibleHeading` directly on the subclass options object instead of introducing another wrapper.

### 4. Validate
- Tab through the sim (or inspect the PDOM with browser dev tools) to confirm the heading now appears before the intended section.
- Confirm that no duplicate headings exist for the same content and that any dynamic variants announce correctly.

Following this pattern ensures new sections match existing implementations in `number-pairs` and `forces-and-motion-basics`, so screen reader users receive consistent structural cues throughout the sims.
