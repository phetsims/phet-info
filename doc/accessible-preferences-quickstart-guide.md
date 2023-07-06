# Accessible Preferences - Quickstart Guide

- @author Jesse Greenberg (PhET Interactive Simulations)
- @author Taliesin Smith (PhET Interactive Simulations)

## Overview

This document is a quicksart guide for adding Interactive Description to the Preferences dialog in PhET simulations.

Please see the alternative-input-quickstart-guide.md first. This guide assumes you are familiar with that
and have enabled Interactive Description in your package.json.

PhET is going to start adding Interactive Description to the Preferences Menu dialog for simulations that support
alternative input. By adding Interactive Description to our Preferences Menu dialog, we enable students to access and use
specific simulation controls that can aid their learning process.

Interactive Description allows individuals who rely on screen readers to interact with our user interfaces effectively.
By adding screen reader support for the Preferences Menu dialog, we empower users to access essential features. For
example, a user can enable the Voicing option, even if the simulation does not fully support screen reader access.

## General Dscription Design and Instrumentation Process

### 1. Identify the components that require instrumentation

Start by identifying components that need to be made accessible. If your sim includes sim-specific components for
Preferences, you will need to instrument them and design descriptions for them. Otherwise, you are done! The shared components and tabs for Preferences are already instrumented for screen reader accessibility.

### 2. Set component options for Interactive Description

Most components will require a few additional options to be set in order to be screen reader accessible.

### 3. Inspect components with the a11y-view

Once you have set the component options and added descriptions to the component, use the 'a11y-view' for the sim to make sure that accessible content (i.e., the added description) is set correctly.

### 4. Test with a screen reader

Use a screen reader to navigate and find the instrumented components, interact with them using the keyboard, and verify that the descriptions you hear work well in the screen reader experience.

## Detailed Instrumentation Process and Description Design Tips

### Setting component options

Screen reader accessibility is supported by scenery/ParallelDOM.ts, a super class for scenery/Node. This class has many
options you can set on a Node for accessibility. But most common code components have options you can use to easily
set their accessible content. These options let you set things like:

- The accessible name for the component.
- The help text description for the component, i.e., a optional description that provides some contextual information about what the component does. If you need a help text description, it is a good practice to start the help text with a verb.
- Context responses to succinctly confirm or describe the resulting change to the surrounding context that result from the action taken on the component.

Here are two examples using the options for a sun/Checkbox:

```js
const myCheckbox = new Checkbox( someBooleanProperty, someContentNode, {
  labelContent: 'Extra Sounds',
  descriptionContent: 'Play additional sound that may be helpful for some learners.',

  // Context responses that describe or confirm the changed context upon toggling the checkbox
  checkedContextResponse: 'Extra sounds on.',
  uncheckedContextResponse: 'Extra sounds off.'
} );
```
**Chekbox Description Design Tip:** In the Preferences Menu, both the name and the help text description are visually displayed. This is not the case for simulation description design. You can potentially avoid the need for help text by creating an action-oriented name that starts with a verb, and context responses that succinctly confirm the success of the taken action.

```js
const myCheckbox = new Checkbox( someBooleanProperty, someContentNode, {
  labelContent: 'Voice surrounding context changes',

  // Context responses that describe or confirm the changed context upon toggling the checkbox
  checkedContextResponse: 'Voicing surrounding context changes.',
  uncheckedContextResponse: 'Surrounding context changes muted.'
} );
```

Here is an example of using the options for a sun/AquaRadioButtonGroup:

```js
// labelContent sets an accessible name on each radio button in the group.
const items = [
  { value: 'item1', createNode: () => new Text( 'Item 1' ), labelContent: 'Item 1' },
  { value: 'item2', createNode: () => new Text( 'Item 2' ), labelContent: 'Item 2' },
  { value: 'item3', createNode: () => new Text( 'Item 3' ), labelContent: 'Item 3' }
];

const myRadioButtonGroup = new AquaRadioButtonGroup( someProperty, items, {
  // the label and help text description for the whole radio button group.
  labelContent: 'My Radio Button Group',
  descriptionContent: 'Choose an option that does something.'
} );

// optional context responses that describe the result of the changing Property
someProperty.lazyLink( value => {
  myRadioButtonGroup.alertDescriptionUtterance( value );
} );
```

Here is an example of using the options for a sun/Slider:

```js
const mySlider = new Slider( someProperty, {
  labelContent: 'My Slider',
  descriptionContent: 'This is a slider that explores a range of some values.',

  // optional context responses that describe the result of the action
  a11yCreateContextResponseAlert: value => { `The value has changed to ${value}.` }
} );
```

Here is an example of using the options for scenery/Text:

```js
const myText = new Text( 'My Text', {
  tagName: 'p',
  innerContent: 'This is the content for the text that you want in the PDOM.'
} );
```

### Reviewing components with a11y-view

The "a11y-view" is a debugging tool that lets you see the descriptions that have been designed for the simulation. The ally-view is not a full representation of the screen rader experience, but it helpfully displays all the content that screen reader software can access and read out. The a11y-view is automatically generated for sims that support Interactive Description. 

You can run the a11y-view for a simulation from phetmarks. 
Or, go to http://localhost:8080/{{SIMULATION}}/{{SIMULATION}}_a11y_view.html?brand=phet&ea&debugger.

Open the Preferences dialog and make sure that all of your components and have the name (`labelContent`) and help text (`descriptionContent`) you
expect.

### Testing with a screen reader

The QA handbook has good resources about how to use a screen reader. You can find it
here: https://github.com/phetsims/QA/blob/master/documentation/qa-book.md#screen-readers.
With that information you should be able to turn on a screen reader, navigate to the Preferences dialog, and read
components in the Preferences dialog.

## Examples
- See greenhouse-effect for an example of instrumented simulation preferences.

## Additional Resources

For a more thorough guide to Interactive Description, please see the interactive-description-technical-guide.md.
The fundamental scenery component for accessibility
is [ParallelDOM.ts](https://github.com/phetsims/scenery/blob/master/js/accessibility/pdom/ParallelDOM.ts)
