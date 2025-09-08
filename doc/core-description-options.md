# Core Description Options

This document was written in response to https://github.com/phetsims/phet-info/issues/243 so designers and developers
could see all the options for specifying descriptive text in one place, with the exact option names. I do not know how
to automatically keep this in sync with the code. @author Sam Reid (PhET Interactive Simulations).

## SCENERY

### Node

* accessibleName
* accessibleHelpText
* accessibleParagraph
* accessibleHeading

and those each have their associated "Behavior", such as `accessibleNameBehavior`. The rest of the options are here in
the details:

<details>

```ts

  // Order matters. Having focus before tagName covers the case where you change the tagName and focusability of a
  // currently focused Node. We want the focusability to update correctly.
  'focusable',
  'tagName',

  /*
   * Higher Level API Functions
   */
  'accessibleName',
  'accessibleNameBehavior',
  'accessibleHelpText',
  'accessibleHelpTextBehavior',
  'accessibleParagraph',
  'accessibleParagraphBehavior',

  /*
   * Lower Level API Functions
   */
  'accessibleHeading',
  'accessibleHeadingIncrement',
  'accessibleRoleDescription',

  'containerTagName',
  'containerAriaRole',

  'innerContent',
  'inputType',
  'inputValue',
  'pdomChecked',
  'pdomNamespace',
  'ariaLabel',
  'ariaRole',

  'labelTagName',
  'labelContent',
  'appendLabel',

  'descriptionTagName',
  'descriptionContent',
  'appendDescription',

  'accessibleParagraphContent',

  'focusHighlight',
  'focusHighlightLayerable',
  'groupFocusHighlight',
  'pdomVisibleProperty',
  'pdomVisible',
  'pdomOrder',

  'pdomAttributes',

  'ariaLabelledbyAssociations',
  'ariaDescribedbyAssociations',
  'activeDescendantAssociations',

  'focusPanTargetBoundsProperty',
  'limitPanDirection',

  'positionInPDOM',

  'pdomTransformSourceNode'

```

</details>

## SUN

### Checkbox

* accessibleContextResponseChecked
* accessibleContextResponseUnchecked

### ToggleSwitch

* accessibleContextResponseLeftValue
* accessibleContextResponseRightValue

### AccordionBox

* accessibleContextResponseExpanded
* accessibleContextResponseCollapsed
* accessibleHelpTextExpanded
* accessibleHelpTextCollapsed

### AquaRadioButton | ComboBox | ButtonNode

* accessibleContextResponse

### RectangularMomentaryButton | RoundMomentaryButton

* accessibleContextResponseValueOn
* accessibleContextResponseValueOff

## SCENERY PHET


### GrabDragInteraction

* objectToGrabString
* idleStateAccessibleName
* accessibleHelpText
* gestureHelpText

### ZoomButtonGroup

* accessibleNameZoomIn
* accessibleHelpTextZoomIn
* accessibleNameZoomOut
* accessibleHelpTextZoomOut

## JOIST

### Screen

* screenButtonsHelpText