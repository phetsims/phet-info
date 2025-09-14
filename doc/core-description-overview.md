# Core Description Overview (IN PROGRESS)

@author Taliesin Smith
@author Jesse Greenberg

# Description Design Framework
![alt text "PhET's Description Design Framework."](images/descriptionDesignFramework.png "Description Design Framework")
PhET's _Description Design Framework_ divides the design of the Interactive Description feature, the entire interactive story of the sim, into manageable chunks. To meet the goals of _Core Description_, we are designing descriptions of all categories, but we are not designing all descriptions found in the full _Interactive Description_ feature. For _Core Description_ we want to focus on the subset of descriptions pieces that will provide both broad access to learners **AND** meet WCAG Level AA design guidance success criteria.

# What is “Core Description”?
_Core Description_ is a sub set of descriptions needed for the Interactive Description feature that aims to meet WCAG A and AA Success Criteria while at the same time creating a phased description design process that allows the team to open simulation access to learners who rely on description. 

Additionally, design and development of _Core Description_ of several sims at once allows us to improve SceneryStack's high-level APIs, and all the inclusive design and develpment skills of the entire team. Creating a phased description design approach (_Core Description,_ then full _Interactive Description_) allows us to gain the skills and expertise needed when for the second descriptin design phase. 

# What is included and excluded in Core Description
_Core Description_ does not explicitly exclude any categories of description. If it is easy to design and implement, we want to include it. That said, there are clear boundary lines around the design of qualitative parameters needed for more dynamic strings found in Object and Context Responses, and Dynamic State Descriptions.

# Core Description Options (a definition of each and high level overview)
  - screen summary - A _State Description_ that includes static and dynamic descriptions meant to capture a big-picture summary of the current screen. 
  - accessible name - The name (or label) of the interactive object.
  - accessible help text - The supporting descriptions needed to scaffold interaction. Design needs vary by interactive object.
  - accessible headings - The descriptions that provide navigable sections within the PDOM. Headings help create information relationships. 
  - accessible paragraph - A description in the PDOM that is not directly part of an interactive object. Used to contain static or dynamic state descriptions. 
  - accessible object response - a response containing a new value or new state of an interactive object. Not all objects have designed object responses. Slider object deliver their object responses via _aria-valuetext._ Custom objects deliver object responses along side context responses via _ARIA Live._ For _Core Description_ design effort should concentrate on human readable quantitative values relevant to learning. 
  - accessible context response - a response describing surrounding changes to the context as an object is being interacted with. For _Core Description_ design effort should focus on the context responses needed for simple UI components first, and then as respurces allow more complex interactions.

# Drawing the line between Core and Interactive Description.
 - Try to break this into general dos and don'ts
 - Qualitative information in dynamic strings
 - Descriptions around custom objects
 - Keep current details to the absolute essentials (practices in process - will summarize)

# Punctuation
- accessibleName: Title case, no punctuation. Example: “Detector Probe”
- accessibleHelpText: Sentence case, with punctuation. Example: “Move probe or jump to useful positions with keyboard shortcut.”
- accessibleObjectResponse: Fragment, no sentence casing, no punctuation. Example: “1.07 centimeters”
- accessibleContextResponse: Sentence case, with punctuation. Example: "In light source path, centered in cuvette. Transmittance is 52.69 percent."
- accessibleParagraph: a paragraph of full sentences, with sentence case and punctuation. Example: "Transmittance is 52.96 percent."

# Delivery of Descriptions with Screen Reader Software
- briefly describe the reading experience
   - for example, accessible help text is accessed only when reading and never with Tab key navigation.
- briefly describe the Tab navigation and the interactive experience
- briefly describe the robust navigation options available to screen reader users 

# Examples for each Core Description piece

# References to relevant existing design documents for Core Description

# References on how to use a screen reader

# References to the development overview
