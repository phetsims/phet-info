# Core Description Overview

@author Taliesin Smith
@author Jesse Greenberg

# Description Design Framework
![alt text "PhET's Description Design Framework."](images/descriptionDesignFramework.png "Description Design Framework")

PhET's _Description Design Framework_ divides the design of the Interactive Description feature, the entire interactive story of the sim, into manageable chunks. To meet the goals of _Core Description_, we are designing descriptions in all four categories defined in the design framework, but we are not designing all descriptions that will eventually be needed for a fully designed _Interactive Description_ feature. 

# What is “Core Description”?
_Core Description_ is part of a phased description design process to scale the design and implementation of description in simulations. _Core Description_ allows PhET to open simulation access up to learners who rely on description, **AND** to create simulation designs that meet most, if not all, relevant WCAG success criteria to be WCAG AA compliant.
 
Additionally, design and development of _Core Description_ of several simulations all at once allows the PhET Team to improve SceneryStack's high-level APIs, and the inclusive design and development skills of the entire team. Creating a phased description design process (_Core Description,_ then full _Interactive Description_) allows the team to gain the skills and expertise needed for the second description design phase. 

# What is included and excluded in Core Description
_Core Description_ does not explicitly exclude any categories of description. If it is easy to design and implement, we want to include it. That said, there are clear boundary lines around the design of qualitative parameters needed for more dynamic strings found in Object and Context Responses, and Dynamic State Descriptions.

# Definitions for [Core Description Options](https://github.com/phetsims/phet-info/blob/main/doc/core-description-options.md): 
  - screen summary - A _State Description_ that includes static and dynamic descriptions meant to capture a big-picture summary of the current screen. 
  - accessible name - A state description (typically static) that names (or labels) the interactive object.
  - accessible help text - The supporting descriptions needed to scaffold interaction. Design needs vary by interactive object.
  - accessible headings - The descriptions that provide navigable sections within the PDOM. Headings help create information relationships. 
  - accessible paragraph - A description in the PDOM that is not directly part of an interactive object. Used to contain static or dynamic state descriptions. 
  - accessible object response - a response containing a new value or new state of an interactive object. Not all objects have designed object responses. Slider objects deliver object responses via _aria-valuetext._ Custom objects deliver object responses alonoside context responses via _ARIA Live._ For _Core Description_ design effort should concentrate on human readable quantitative values relevant to learning. 
  - accessible context response - a response describing surrounding changes to the context as an object is being interacted with. For _Core Description_ design effort should focus on the context responses needed for simple UI components first, and then as respurces allow more complex interactions.

# Drawing the line between Core and Interactive Description
Core Description is focused on these categories:
- Basic screen summary
- accessible names
- accessible help text (optional)
- accessible headings necessary for scaffolding and relationships (optional)
- accessible paragraphs for state information and graphics
- Accessible object responses for objects that have a well-defined value or a numeric value.
- Accessible context responses for simple UI components.

# Use the following strategies
- Keep the current details of the screen summary simple.
  - Use binary states if possible, and then provide additional state information close to the interactive object.
- Consider simplifying the information you want to provide.
- Avoid qualitative information requiring multiple parameters with described scales.
- Call in other team members with more experience, and/or discuss at the weekly Design Meeting.

# Punctuation
- accessibleName: Title case, no punctuation. Example: “Detector Probe”
- accessibleHelpText: Sentence case, with punctuation. Example: “Move probe or jump to useful positions with keyboard shortcut.”
- accessibleObjectResponse: Fragment, no sentence casing, no punctuation. Example: “1.07 centimeters”
- accessibleContextResponse: Sentence case, with punctuation. Example: "In light source path, centered in cuvette. Transmittance is 52.69 percent."
- accessibleParagraph: a paragraph of full sentences, with sentence case and punctuation. Example: "Transmittance is 52.96 percent."

# Delivery of Descriptions with Screen Reader Software

TODO: Make this more about core description.

- Information users can find and read in the PDOM with their cursor keys without changing the state of the simualtion includes:
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

# Examples for each Core Description Options
- ToDo - What kinds of examples are needed here?

Example of how to keep the Screen Summary simple:
 - See the screen summary in ph-scale for a good example of a simple "Current Details".
   - The screen summary is kept simple by using a binary state describing whether the beaker has a liquid or not.
   - Additionally, provides a dynamic interaction hint, supporting these two states.

For each interactive component
 - Design an accessibleName
 - Consider accessibleHelpText
 - Design en entry for each of the other Core Description options for the component listed in [Core Description Options](https://github.com/phetsims/phet-info/blob/main/doc/core-description-options.md)

For example:
  - For a slider:
    - accessibleName
    - accessibleHelpText (optional)
    - accessible object response (currently option pdomCreateAriaValueText) (numeric value, rounded to human-readable value)
    - accessible context response (currently option pdomCreateContextResponseAlert) (if simple)

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
