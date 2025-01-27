# Glossary of Terms for Accessible Description Translation

This glossary of terms covers key terms and concepts translators may need to be aware of when translating accessible descriptions for a simulation or project using Fluent.js for accessible descriptions.

## About Accessible Descriptions
- ***Accessible Descriptions***
	- *Accessible descriptions* are the descriptions designed to be access through through text-to-speech features, specifically the Interactive Description and Voicing features.  While there is overlap with the text visually displayed on the screen, many more descriptions are needed to provide descriptions for accessibility purposes. Note: The number of PhET simulations that have accessible description that can be accessed through one or both text-to-speech features is growing.

- ***Speech Synthesis and Text-to-Speech***
	- *Speech synthesis* is the artificial production of human speech. A computer system used for this purpose is called a speech synthesizer, and can be implemented in software or hardware products. A *text-to-speech (TTS) system* converts normal language text into speech.

- ***Interactive Description***
	- The *Interactive Description feature* provides a robust set of dynamic and contextually relevant descriptions that can be accessed using traditonal screen reader software (e.g. JAWS, NVDA and VoiceOver) while also using alternative input such as a keyboard. The interactive description feature is designed to meet the needs of learners who are comfortable using screen reader software, such as people who blind or have low vision (BLV).  

- ***Voicing***
	- The *Voicing feature* provides a customizable described experience. A robust set of dynamic and contextually relevant voicing responses are delivered natively through a user's browser. No addition screen reader software is required making the Voicing feature accessible to anyone who would like some spoken descriptions to in addition to sound and visuals.
	
- ***A11y View***
	- The *A11y View* is a tool that displays all the accessible descriptions that are currently designed to be delivered through the Interactive Desction feature. This tool is very useful for translators as it contains all the available desciptions that can be spread across a number of Fluent files. Using the A11y View translators can see what has already has been translated through the *PhET Translation Utility*, and what descriptions may be coming from common code repositories. At the time of writing the A11y View is limited to PhET Simulations, and to the Interactive Description feature.

## Description Design Framework Terms
 PhET has designed and uses a simple *Description Design Framework* [Smith and Moore, 2020](https://dl.acm.org/doi/abs/10.1145/3313831.3376460) to do description design. We even have a coursera course about it, see [Description Design for Interactive Resources](https://www.coursera.org/learn/description-design-for-interactive-learning-resources). Translators will find references to different categories of description in the comments of the Fluent files. Familiarity with the different categories may provide some helpful context for translation. *State Descriptions* can be static or dynamic are designed to capture the _current state_ of the interactive when a user is not actively making changes. *Responsive Descriptions* are designed to describe _relevant changes_ as they occur in response to user interaction or ongoing changes to the model.

- Static state descriptions
	- Descriptions that are constant - always accurate and true with regard to the model. These descriptions are the easiest to translate, and require no additional knowledge of *Fluent* syntax. Common static state descriptions are:
		- The first part of the screen summary, often refered to as the 'sim overview'. 
		- Names of interactive controls.
		- Help text for interactive controls.
	
- Dynamic state descriptions 
	- Descriptions that update silently in the background staying in synch with the current state. Dynamic state descriptions will have embedded parameters - sub-strings to capture all the different possible states. These descriptions will require knowledge of additional *Fluent* syntax. Parameters for dynamic state descriptions may be associated with re-usable strings that used in more than one description. Common dynamic state descriptions are;
		- The second part of the screen summary, often referred to as the 'current details'.
		- Detailed descriptions of visualized objects.
		- Names and help text can also be dynamic, but description designers try to avoid doing that. 

- Object Responses
	- Very brief strings, often quantitative or qualitative values, that capture each possible state of an object. Object responses or their parameters are often listed in the re-usable strings section of the Fluent file. Descriptions for common code interactions may live in other Fluent files in other respositories. Object response are often followed by context responses. Examples of when object responses can be heard when:
		- A learner moves their keyboard focus to an interactve control, like a slider.
		- A learner presses arrow keys to change the value on a slider.
 

- Context Responses 
	- Brief strings or phrases that capture what is happening in the surrounding context, outside the direct changes happening to the object the user is actively manipulating. Context responses often have parameter. Context responses can be heard on their own or in addition to object responses. Examples of when context responses can are heard when: 
		- A learner checks or unchecks a checkbox. 
		- A learner moves an object and the new position creates a change to the context.
		- A learner activates toggles a control and starts causing ongoing changes tot he context.
		
		
	
	
	
	
	