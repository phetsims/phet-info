# Core Description Options

This document was written in response to https://github.com/phetsims/phet-info/issues/243 so designers and developers
could see all the options for specifying descriptive text in one place, with the exact option names. I do not know how
to automatically keep this in sync with the code.

* @author Sam Reid (PhET Interactive Simulations).

## SCENERY

### Node

* accessibleName
* accessibleHelpText
* accessibleParagraph
* accessibleHeading
* accessibleRoleDescription

### Most buttons and simple components, including but not limited to AquaRadioButton | ComboBox | ButtonNode

* accessibleContextResponse

## SUN

### ABSwitch

* valueAAccessibleName (to be renamed to accessibleNameValueA soon)
* valueBAccessibleName (to be renamed to accessibleNameValueB soon)

### AccordionBox

* accessibleContextResponseExpanded
* accessibleContextResponseCollapsed
* accessibleHelpTextExpanded
* accessibleHelpTextCollapsed

### AccessibleSlider
* pdomCreateAriaValueText (for object responses, to be renamed soon)
* pdomCreateContextResponseAlert (for context responses, to be renamed soon)
* keyboardStep
* shiftKeyboardStep
* pageKeyboardStep

### AccessibleValueHandler

* pdomCreateAriaValueText
* pdomCreateContextResponseAlert

### AquaRadioButton

* accessibleContextResponse

### ButtonNode

* accessibleContextResponse

### Checkbox

* accessibleContextResponseChecked
* accessibleContextResponseUnchecked

### ComboBox

* accessibleContextResponse

### RectangularMomentaryButton | RoundMomentaryButton

* accessibleContextResponseValueOn
* accessibleContextResponseValueOff

### ToggleSwitch

* accessibleContextResponseLeftValue
* accessibleContextResponseRightValue

## SCENERY PHET

### PlayControlButton

* startPlayingAccessibleName (to be renamed to accessibleNameStartPlaying soon)
* endPlayingAccessibleName (to be renamed to accessibleNameEndPlaying soon)

### PlayPauseStepButtonGroup

* playingHelpText (to be renamed to accessibleHelpTextPlaying soon)
* pausedHelpText (to be renamed to accessibleHelpTextPaused soon)

### ZoomButtonGroup

* accessibleNameZoomIn
* accessibleHelpTextZoomIn
* accessibleNameZoomOut
* accessibleHelpTextZoomOut

## JOIST

### Screen

* screenButtonsHelpText

### ScreenSummaryContent

* playAreaContent
* controlAreaContent
* currentDetailsContent
* interactionHintContent
