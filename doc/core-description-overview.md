# Core Description Overview (IN PROGRESS)

@author Taliesin Smith
@author Jesse Greenberg

# Description Design Framework
![alt text "PhET's Description Design Framework."](images/descriptionDesignFramework.png "Description Design Framework")
PhET's _Description Design Framework_ divides the design of the Interactive Description feature, the entire interactive story of the sim, into manageable chunks. To meet the goals of _Core Description_, we are designing descriptions of all categories, but we are not designing all descriptions found in the full Interactive Description feature. For _Core Description_ we want to focus on the subset of descriptions pieces that will provide both broad access to learners **AND** meet WCAG Level AA design guidance success criteria.

# What is “Core Description”?
_Core Description_ is a sub set of descriptions needed for the Interactive Description feature that aims to meet WCAG A and AA Success Criteria while at the same time creating a phased description design process that allows the team to open simulation access to learners who rely on description. 

Additionally, design and development of _Core Description_ of several sims at once and all new sims allows us to improve SceneryStack's high-level APIs, and all the inclusive design and develpment skills of the entire team. Creating a phased design approach allow us to gain the skills and expertise needed when we get the Interactive Description design phase. 

# What is included and excluded in Core Description
_Core Description_ does not explicitly exclude any categories of description. If it is easy to design and implement, we want to include it. That said, there are clear boundary lines around the design of qualitative parameters needed for more dynamic strings found in Object and Context Responses, and Dynamic State Descriptions.


# Core Description pieces (a definition of each and high level overview)
  - screen summary - A three-piece state description capturing a big picture summary of the screen. (UNDER DISCUSSION)
  - accessible name - 
  - accessible help text
  - accessible headings
  - accessible paragraph
  - accessible object response
    - Quantitative values for object responses
  - accessible context response
    - Simple statements tied to a UI component or user interaction.
    - {{pedagogically critical quantitative information?}}

# Drawing the line between Core and Interactive Description.
 - Try to break this into general dos and don'ts
 - Qualitative information in dynamic strings
 - Descriptions around custom objects
 - Keep current details to the absolute essentials (practices in process - will summarize)

# Punctuation
- accessibleName: Title case, no punctuation. Example: “Concentration Probe”
- accessibleHelpText: Sentence case, with punctuation. Example: “Move the probe.”
- accessibleObjectResponse: Fragment, no sentence casing, no punctuation. Example: “5 centimeters”,  “dispensing”
- accessibleContextResponse: Sentence case, with punctuation. Example: "Vector added to graph area."
- accessibleParagraph: a paragraph of full sentences, with sentence case and punctuation.

#Delivery of Descriptions with Screen Reader Software
- briefly describe the reading experience
   - for example, accessible help text is accessed only when reading and never with Tab key navigation.
- briefly describe the Tab navigation and the interactive experience
- briefly describe the robust navigation options available to screen reader users 

# Examples for each Core Description piece

# References to relevant existing design documents for Core Description

# References on how to use a screen reader

# References to the development overview
