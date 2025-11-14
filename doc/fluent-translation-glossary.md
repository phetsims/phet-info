# Glossary of Terms for Accessible Description Translation

This glossary of terms covers key terms and concepts translators may need to be aware of when making a translation of the *accessible descriptions* for a simulation or a project using **. 

## About Accessible Descriptions
- ***Accessible Descriptions***
	- *Accessible descriptions* are the descriptions designed to be accessed through alternative methods, such as text-to-speech, specifically the *Interactive Description* and *Voicing* features. While there is overlap in content with the text visually displayed on the screen, more descriptions are needed to support a diverse range of needs, including non-visual access. Note: The number of PhET simulations that have accessible description that can be accessed through one or both of these description features is growing.

- ***Speech Synthesis*** and ***Text-to-Speech***
	- *Speech synthesis* is the artificial production of human speech. A computer system used for this purpose is called a speech synthesizer, and can be implemented in software or hardware products. A *text-to-speech (TTS) system* converts language strings (text) into speech.

- ***Interactive Description***
	- The *Interactive Description* feature provides a robust set of dynamic and contextually relevant descriptions that can be accessed using traditonal screen reader software (e.g. JAWS, NVDA and VoiceOver) while also using alternative input such as a keyboard. The interactive description feature is designed to meet the needs of learners who are comfortable using screen reader software, such as people who blind or have low vision (BLV).   

- ***Voicing***
	- The *Voicing* feature provides a customizable described experience. This includes a robust set of dynamic and contextually relevant *voicing responses* that are delivered natively through a user's browser. No additional screen reader software is required making the *Voicing* feature accessible to a much broader audience--anyone who would like spoken descriptions in addition to other sound and visuals.
	
- ***A11y View (Interactive Description)*** 
	- The *A11y View* is a tool that displays all of the descriptions that are currently designed to be delivered through the *Interactive Description* feature--these descriptions can originate from multiple locations, including the sim repository, common code repositories, and the babel repository. The *A11y View* tool is very useful for first checking to see if parts of the sim have already been translated, and for testing translated description originating from *Fluent* files. At the time of writing (January 2025), the *A11y View* displays the accessible descriptions that are available in the *Interactive Description* feature only for PhET Simulations. Community effort may expand this tool.  

## Description Terminology
- ***Static State Descriptions***
	- Descriptions strings that are constant--always accurate and true regardless of user interaction. These descriptions are the easiest to translate, and require no additional knowledge of *Fluent* syntax. Common static state descriptions are:
		- The first part of the screen summary, often refered to as the 'overview'. 
		- Names of interactive controls.
		- Help text for interactive controls.
	
- ***Dynamic State Descriptions*** 
	- Descriptions strings that update silently in the background, staying in synch with the current state. *Dynamic state descriptions* will have embedded *parameters*. Translating *dynamic state descriptions* and their *parameters* will require knowledge of additional *Fluent* syntax. Common *dynamic state descriptions* are:
		- The second part of the screen summary, often referred to as the 'current details'.
		- Detailed descriptions of state of objects.
		- Names and help text can also be dynamic, but only when absolutely necessary. 

- ***Object Responses***
	- Brief strings or phrases, often quantitative or qualitative values, that convey the current state of an object. Object responses or their parameters are often listed in the re-usable strings section of the *Fluent* file. Descriptions for common code interactions may live in other *Fluent* files in other respositories. Object response are often followed by context responses. Examples of when object responses can be heard are when:
		- A learner moves their keyboard focus to an interactve control, like a slider.
		- A learner presses arrow keys to change the value on a slider.
 
- ***Context Responses*** 
	- Brief strings or phrases that convey the current state of the surrounding context, beyond the object the user is actively manipulating. This allows for interpreting cause and effect relationships. Context responses often have embedded *parameters*. Context responses can be heard on their own or in addition to object responses. Examples of when context responses can be heard are when: 
		- A learner checks or unchecks a checkbox. 
		- A learner moves an object and the new position creates a change to the context.
		- A learner activates or toggles a control, causing ongoing changes to the context.
		
- ***Parameters*** and ***Re-usable strings***
	 -  Sub-strings--often used in more than one description--are strings that fill in the changing parts of *State* and *Responsive descriptions*. *Parameters* are designed to capture all meaningful states of a particular description and to minimize wording changes. Because *parameter* are often used in more than one description, they are often listed in the ***re-usable strings*** section at the top of the *Fluent* file. Translators may find the need to add to the re-usable strings section to handle language specific changes. Doing so, is optional, but can make translations more efficient.

- ***Voicing Responses***
	- *Voicing responses* are the *accessible descriptions* that are delivered through the *Voicing* feature. The *Voicing responses* often consist of the same strings used for *Interactive Description*, but they can differ. You might find a seperate section in the *Fluent* file with *accessible description* for the *Voicing* feature.
	
 - ***Description Design Framework***
 	- PhET created and uses the *Description Design Framework* [Smith and Moore, 2020](https://dl.acm.org/doi/abs/10.1145/3313831.3376460) to design *accessible descriptions*. To learn more, we encourage you to take our free online Coursera course, see [Description Design for Interactive Resources](https://www.coursera.org/learn/description-design-for-interactive-learning-resources). The description terminology above can be referenced in the comments of *Fluent* files. Familiarity with the types of descriptions may provide some helpful context for translation. All *accessible descriptions* are either *State Descriptions* designed to capture the ***current state*** when a user is not actively making changes, or *Responsive Descriptions* designed to describe ***relevant changes*** as they occur in response to user interaction or ongoing changes to the model. There is typically significant overlap between the *accessible descriptions* delivered via the *Interactive Description* and *Voicing features*.




	
	
	
