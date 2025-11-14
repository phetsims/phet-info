# Accessible Preferences - Quickstart Guide

- @author Jesse Greenberg (PhET Interactive Simulations)
- @author Taliesin Smith (PhET Interactive Simulations)

## Overview

This document is a quickstart guide for adding Interactive Description to the Preferences dialog in PhET simulations.

Please see the alternative-input-quickstart-guide.md first. This guide assumes you are familiar with that and have
enabled Interactive Description in your package.json.

By adding Interactive Description to a Preferences dialog, learners who rely on screen reader software are
empowered to access essential features. For example, a blind learner will be able to enable the Voicing feature, even if
the simulation does not fully support Interactive Description. Having a fully accessible Preferences Menu supports
learner agency in accessing and using any features in the Preferences Menu that can aid in their learning process.

## General Description Design and Instrumentation Process

### 1. Identify the components that require instrumentation

Start by identifying components that need to be made accessible. If your sim includes sim-specific components for
Preferences, you will need to instrument them and design descriptions for them. Otherwise, you are done! The shared
components and tabs for Preferences are already instrumented for screen reader accessibility.

### 2. Set component options for Interactive Description

Most components will require a few additional options to be set in order to be screen reader accessible.

### 3. Inspect components with the a11y-view

Once you have set the component options and added descriptions to the component, use the 'a11y-view' for the sim to make
sure that accessible content (i.e., the added descriptions) is displayed correctly.

### 4. Test with a screen reader

Use a screen reader to navigate and find the instrumented components, interact with them using the keyboard, and verify
that the descriptions you hear work well when delivered through the screen reader experience. Do not use the A11y View
tool for this step.

## Detailed Instrumentation Process and Description Design Tips

### Setting component options

Screen reader accessibility is supported by scenery/ParallelDOM.ts, a super class for scenery/Node. This class has many
options you can set on a Node for accessibility. But most common code components have options you can use to easily set
their accessible content (i.e., the descriptions you add). These options let you set things like:

- The accessible name.
- The help text description, i.e., an optional description that provides some contextual information about what the
  component does. If you need a help text description, it is good practice to start the help text with a verb.
- Depending on the component type, you may need object responses to communicate current and changed values. Not all
  interactive components require object responses.
- Depending on the component type, you may need context responses to succinctly confirm or describe the resulting change
  to the surrounding context that results from the action taken on the component.

Here are two examples from the Preferences Menu that use the options for a sun/Checkbox:

**Checkbox Description Design Tips:** You can potentially avoid the need for help text by creating an action-oriented
name that starts with a verb and context responses that succinctly confirm the success of the action (see second
example).

```js
const myCheckbox = new Checkbox( someBooleanProperty, someContentNode, {
  labelContent: 'Extra Sounds',
  descriptionContent: 'Play additional sound that may be helpful for some learners.',

  // Context responses that describe or confirm the changed context upon toggling the checkbox
  accessibleContextResponseChecked: 'Extra sounds on.',
  accessibleContextResponseUnchecked: 'Extra sounds off.'
} );
```

```js
const myCheckbox = new Checkbox( someBooleanProperty, someContentNode, {
  labelContent: 'Voice surrounding context changes',

  // Context responses that describe or confirm the changed context upon toggling the checkbox
  accessibleContextResponseChecked: 'Voicing surrounding context changes.',
  accessibleContextResponseUnchecked: 'Surrounding context changes muted.'
} );
```

Here is an example from Density's Simulation Tab that uses the options for a sun/AquaRadioButtonGroup:

**Radio button group Description Design Tips:** Radio butttons rarely need context responses. Consider using "Choose" as
part of the group name or help text, and always spell out abbreviations and symbols for screen reader accessibility.

```js
// labelContent sets an accessible name on each radio button in the group.
const items = [
  { value: 'item1', createNode: () => new Text( 'liters (L)' ), labelContent: 'liters (L)' },
  { value: 'item2', createNode: () => new Text( 'cubic decimeters (dm cubed)' ), labelContent: 'cubic decimeters (dm3)' },
];

const myRadioButtonGroup = new AquaRadioButtonGroup( someProperty, items, {
  // the label and optional help text description for the whole radio button group.
  labelContent: 'Choose volume units',
  // descriptionContent: ''
} );
```

```js
// optional context responses that describe the result of the changing Property
//someProperty.lazyLink( value => {
//  myRadioButtonGroup.addAccessibleResponse( value );
//} );
```

Here is an example of using the options for a sun/Slider implemented for Quadrilateral's Input Tab:

**Slider Description Design Tips:** Sliders always need a range of object responses to communicate their current and
changed values. Object responses can be quantitative or qualitative. Be mindful of where you might need to adjust for
singular or plural wording, e.g., "1 value" versus "5 values". A help text description is often helpful but always
optional. For the Preferences Menu, context responses for slider components are likely not needed. This is not the case
for sliders in simulations.

```js
const mySlider = new Slider( someProperty, {
  labelContent: 'Smoothing Avergage',
  descriptionContent: 'Adjust number of values used to smooth noise in incoming sensor values from input device.',

  // spoken every time the slider value changes, describing the new value
  createAriaValueText: value => { `${value} values` }

  // optional context responses that describe the result of the action
  // pdomCreateContextResponseAlert: value => { `The value has changed to ${value}.` }
} );
```

Here is a canned example of using the options for scenery/Text:

```js
const myText = new Text( 'My Text', {
  tagName: 'p',
  innerContent: 'This is the content for the text that you want in the PDOM.'
} );
```

### Reviewing components with a11y-view

The "a11y-view" is a debugging tool that lets you see the descriptions that have been designed for the simulation. The
ally-view is not a full representation of the screen reader experience, but it helpfully displays all the content that
screen reader software can access and read out. The a11y-view is automatically generated for sims that support
Interactive Description.

You can run the a11y-view for a simulation from phetmarks. Or, go
to http://localhost:8080/{{SIMULATION}}/{{SIMULATION}}_a11y_view.html?brand=phet&ea&debugger.

Open the Preferences dialog and make sure that all of your components have the name and help text you expect.

### Testing with a screen reader

The QA handbook has good resources about how to use a screen reader. You can find it
here: https://github.com/phetsims/QA/blob/main/documentation/qa-book.md#screen-readers. With that information, you
should be able to turn on a screen reader, navigate to the Preferences Menu, and read through descriptions and interact
with the described components in the Preferences Menu.

## Examples

- See greenhouse-effect for an example of instrumented simulation preferences.

## Additional Resources

For a more thorough guide to Interactive Description implementation, please see the
interactive-description-technical-guide.md. The fundamental scenery component for accessibility
is [ParallelDOM.ts](https://github.com/phetsims/scenery/blob/main/js/accessibility/pdom/ParallelDOM.ts)
