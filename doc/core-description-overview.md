# Core Description Overview

@author Taliesin Smith
@author Jesse Greenberg

# Description Design Framework
![alt text "PhET's Description Design Framework."](images/descriptionDesignFramework.png "Description Design Framework")

PhET's _Description Design Framework_ divides the design of the Interactive Description feature, the entire interactive story of the sim, into manageable chunks. To meet the goals of _Core Description_, we are designing descriptions in all four categories defined in the design framework, but we are not designing all descriptions that will eventually be needed for a fully designed _Interactive Description_ feature. 

# What is “Core Description”?
_Core Description_ is part of a phased description design process to scale the design and implementation of description in simulations. _Core Description_ allows PhET to open simulation access up to learners who rely on description, **AND** to create simulation designs that meet most, if not all, relevant WCAG success criteria to be WCAG AA compliant.
 
Additionally, design and development of _Core Description_ of several simulations all at once allows the PhET Team to improve SceneryStack's high-level APIs, and the inclusive design and development skills of the entire team. Creating a phased description design process (_Core Description,_ then full _Interactive Description_) allows the team to gain the skills and expertise needed for the second description design phase. 

## Definitions for Core Description Options
 Our high-level API has specific options for each node or interactive component, see [Core Description Options](https://github.com/phetsims/phet-info/blob/main/doc/core-description-options.md) for a complete list of current description options.
 
 Core Description Design focuses on the following description options, allbeit that some interactive components have a more specific name for their "accessibleObjectResponse", "accessibleContextResponse," or even "accessibleHelpText." 
   
  - **Screen Summary Content** - A modular _State Description_ that includes the following static and dynamic descriptions meant to capture enough detail to scaffold productive interaction. *Note that design goal for full Interactive Description has been to create a big-picture summary of the entire screen. Core Descrition aims to be simpler.* 
      - playAreaContent (static)
	  - controlAreaContent (static)
	  - currentDetailsContent (dynamic)
	  - interactionHintContent (static or dynamic)
  - **Accessible Name** - A state description (typically static) that names (or labels) the interactive object.
  - **Accessible Help Text** - The supporting descriptions needed to scaffold interaction. Design needs vary by interactive object.
  - **Accessible Heading** - The descriptions that provide navigable sections within the PDOM. Headings help create information relationships. 
  - **Accessible Paragraph** - A description in the PDOM that is not directly part of an interactive object. Used to contain static or dynamic state descriptions.
  - *Accessible List (NOT YET in High-level-API)*
  - **Accessible Object Response** - A response containing a new value or new state of an interactive object. Not all objects have designed object responses. Slider objects deliver object responses natively via _aria-valuetext._ Custom objects deliver object responses alongside context responses via _ARIA Live._ For _Core Description_ design effort should concentrate on human readable quantitative values relevant to learning. 
  - **Accessible Context Response** - A response describing surrounding changes to the context as an object is being interacted with. For _Core Description_ design effort should focus on the context responses needed for simple UI components first, and then as resources allow, consider context responses for more complex interactions.

## Deciding What is Included in Core Description Design
_Core Description_ does not explicitly exclude any categories of description. If it is easy to design and implement, we want to include it. That said, there are clear boundary lines around the design of qualitative parameters needed for dynamic strings found in Object and Context Responses, and Dynamic State Descriptions.

Core Description is focused on the following:
- Creating a basic screen summary to quickly scaffold interaction.
- Accessible names for all interactive components.
- Accessible help text, while always optional, design help text for the components that benefit from additional scaffolding.
- Accessible headings necessary for creating relationships within the PDOM. Like help text, headings are optional.
- Accessible paragraphs for state information and graphics. Description content in accessible paragraphs can be dynamic.
- Accessible object responses for objects that have a well-defined value or a numeric value.
- Accessible context responses for simple UI components like checkboxes and buttons.

## Strategies to Keep Core Description Design Focused
- Keep the current details of the screen summary simple.
  - Use binary states if possible, and then provide additional state information close to the interactive object.
- Consider simplifying the information you want to provide.
- Avoid qualitative information requiring multiple parameters with qualitatively described scales.
- Call in other team members with more experience, and/or discuss challenges at the weekly Design Meeting.

## General Requirements and Considerations for Interactive Components
Description options vary for each interactive component. Always keep the stategies listed above in mind when working on _Core Description_.

For _Core Description_:
 - You always need to design an accessibleName. 
 - You always need to consider designing accessibleHelpText. 
 - You need to review the options for each component listed in [Core Description Options](https://github.com/phetsims/phet-info/blob/main/doc/core-description-options.md), then depending the interaction, determine if you have the resources to design and implement all listed options. Review the strategies above if/when you encounter design challenges.
 
# Punctuation in Description Options
- **accessibleName:** Is like a proper name. Use title case, and generally no punctuation. Example: “Detector Probe”
- **accessibleHelpText:** Is generally a full sentence or a complete phrase. Use sentence case, with punctuation. Example: “Move probe or jump to useful positions with keyboard shortcut.”
- **accessibleObjectResponse:** Is generally a phrase fragment rather than a full phrase. Does not need sentence casing and no final punctuation is needed. Example: “1.07 centimeters”
- **accessibleContextResponse:** Is generally a phrase or sentence. Use sentence case, with punctuation. Example: "In light source path, centered in cuvette. Transmittance is 52.69 percent."
- **accessibleParagraph:** Is a sentence or paragraph that contains full sentences. Use sentence case and appropriate punctuation. Example: "Transmittance is 52.96 percent."


# Core Description Exemplars and Examples

## pH Scale and pH Scale:Basics
In _pH Scale_ the designers made good choices to keep the Screen Summary simple, while at the same time providing essential scaffolds for interactive exploration:
   - The "Current Details" describes whether the beaker "contains liquid" or "is empty".
   - The "Interaction Hint" prompts to either, "Move probe to start exploring," or "Add a solution to beaker and play," depending on the state of the beaker.
The rest of the details such as which solution, the current volume, the current pH reading, and the color of solution, are left for a learner to interactively discover further down, either directly from the state of the interactive objects or through accessible paragraphs and lists near the interactive objects.

Compare the description design of [Molarity]() with [pH Scale]() to see how Molarity's _Interactive Description_ design includes more detail and more qualitative detail in both the Screen Summary and the Play Area. The dynamic states in the _Core Description_ design of _pH Scale_ rely mainly on visually available quantitative values, and use qualitative descriptions sparingly to describe 2 or 3 essentail states rather than all states (e.g., "beaker contains liquid" or "beaker is empty.") 

  


# Requirements for Common Interactive Components (THIS SECTION IN PROGRESS)
Slider:
-  accessibleName
- accessibleHelpText (optional)
- accessible object response (currently option createAriaValueText) (numeric value, rounded to human-readable value)
- accessible context response (currently option createContextResponseAlert) (if simple)

# Delivery of Core Description with Screen Reader Software

TODO: Make this more about core description.

- Information users can find and read in the PDOM with their cursor keys without changing the state of the simulation includes:
    - All information in the screen summary, 
    - Accessible headings, 
    - Accessible names, 
    - Accessible help text, 
    - Descriptions in accessible paragraphs and lists, and
    - The current accessibleObjectResponse for objects like a slider, number picker, number spinner.
  
- Users have many strategies to read, skim, or scan information in the PDOM:
    -  Read continuously from the top, read line-by-line, read by word, or read by letter to resolve ambiguities.
    -  Use screen reader hot keys to navigate document structures such as headings, paragraphs and list items.
 
- When ready to interact, users have many strategies for finding interactive objects:
    - Tab-navigation.
    - Use screen screen reader hot keys to search for common interactions, such as buttons.
    - Use screen screen reader hot keys to find something known to them.
    - Use special navigation modes, e.g. "Forms mode" (JAWS), "Quick Nav" (VoiceOver).
       
- When navigating by interactive object, e.g., Tab-navigation, what users will hear from the screen reader software varies. They expect to hear:
    - an accessible name
    - a current value if the interaction has a value 
    - the role of the interactive object, e.g., button, checkbox, slider
 
- Once making changes, they hear:
   - changing states in "built-in" or accessible object responses  present on the object.
   - changes to surrounding context in accessible context responses.  
   
# References on how to use a screen reader
From the description course: [Description Design for Interactive Learning Resources](https://www.coursera.org/learn/description-design-for-interactive-learning-resources):
- Tip Sheet - [Using VoiceOver with a PhET Sim](https://docs.google.com/document/d/1qz0Dm2lA67tRhgw1GaHVeOSnldBoMj7AT5UE_UaXz1U/edit?tab=t.0#heading=h.rj5etgrq1nf7)
- Tip Sheet - [Using NVDA with a PhET Sim](https://docs.google.com/document/d/1pgfyEER7ZlpJlXSwvSCbNBuoCa5oOexc7QvTuFZu-Mo/edit?tab=t.0#heading=h.rj5etgrq1nf7)
- Tip Sheet - [Using JAWS with a PhET Sim](https://docs.google.com/document/d/1aggemqGsb2CdR7PxgLG50kOg4ZwBPM2M3eI3okyZHJ8/edit?tab=t.0#heading=h.rj5etgrq1nf7)

# References for designers and developers
- [Descriptipn Design Guide: Core](https://docs.google.com/document/d/1kCivjmuXiMzrFkYUigZFgDkssoEWGW_-OaXDk9myV00/edit?tab=t.0#heading=h.rj5etgrq1nf7)
- [PhET's Interactive Style Guide (Binder)](https://phetsims.github.io/binder/)
- [Core Description Options](https://github.com/phetsims/phet-info/blob/main/doc/core-description-options.md)
- [Core Description Quickstart Guide (Development)](https://github.com/phetsims/phet-info/blob/main/doc/core-description-quickstart-guide.md)
- [Core Voicing Quickstart Guide (Development)](https://github.com/phetsims/phet-info/blob/main/doc/core-voicing-quickstart-guide.md)
