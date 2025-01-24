# Translation Guide for Accessible Descriptions
[[Maybe a "Who is this Guide For? section instead of this intro?]]
This guide is about how to create translations for accessible descriptions using Fluent.

This guide will help you understand how to create and submit translations using the Fluent System, the system of fluent.js files we use to store the _accessible descriptions_ (i.e., the descriptions available through the inclusive features Voicing and Interactive Description; more about inclusive features (https://phet.colorado.edu/en/inclusive-design/features). These _accessible descriptions_ are in addition to and seperate from the visual text that appears on-screen. The _Fluent System_ provides options so that translators can make language-specific changes in order to address common grammatical needs that arise in longer phrases. For example, using Fluent transltors can easily address number and gender agreement, word order, and other differences that exist across languages.

## Two Systems for Translations 

PhET has two systems for submitting translations, one for short visual strings and one for longer _accessible descriptions_. 
1. The _PhET Translation Utility (a.k.a Rosetta)_ works well for the short strings that you can see visually in the simulation - visual strings like labels for checkboxes. Volunteer translators have used the _Rosetta_ to translate the visual strings of sims into more than 129 languages. At this time, the _Rosetta_ cannot handle longer phrases found in the _accessible descriptions_. To find more information about the _PhET Translation Utility (HTML_, see [documentation here]({{https://docs.google.com/document/u/1/d/e/2PACX-1vSYc8f01StQ7e2nQWBA38BZfLoqkm6rkn-F9BzTmxdNgazOzFfLDm5RI-3I3IdKccuBFQpFdT2ST5Px/pub
https://phet.colorado.edu/en/for-translators}}).
2. The _Fluent System_ provides a higher level translation system in order to address the language-specific changes required when translating the longer phrases found in _accessible descriptions_. We now organize _accessible descriptions_ in fluent files. Once a translator is familiar with some basic fluent syntax, they can create, test and submit grammatically correct translations of _accessible descriptions_. 

**Note: Translators may need to use both systems to create a complete translation. Or they may find that the visual strings have already been translated by another translator.**

## Introduction to Fluent

### What is Fluent?
Fluent is a localization system developed by Mozilla. It is particularly useful for the translation of complex dynamic content such as the descriptions designed for accessibility.


## Prerequisites for Translating Accessible Descriptions

Using the Fluent System requires a working development environment, basic knowledge of Fluent's syntax, and some familiarity with how refer to and organize _accessible descriptions- in the _Fluent files_.

### PhET Development Environment Setup
- Set up a development environment for the simulation you want to translate by following the PhET Development Overview.
Make sure you can run the simulation locally in your browser and access and edit the code. **Reach out to the community when you need help.**

### Fluent Syntax Knowledge
- Review Fluent's documentation to understand how to structure and format translations effectively.
  - Project Fluent - https://projectfluent.org/
  - Fluent Syntax Guide - https://projectfluent.org/fluent/guide/
  - The most important Fluent concepts for PhET simulations include Terms, Messages, Placeables, and Selectors. Ensure you are familair with the syntax for these four Fluent concepts.
  - Fluent files are text files with the file extension **.ftl**

### Description Framework Terminology 
- PhET has developed a simple description design framework that assists designers in designing the complex strings needed to create dynamci _accessible descriptions_. As you work with the Fluent files you will notice references to description categories in the comments surrounding the descriptions. Familiarizing yourself with the description design framework terminology may assist you in your translation effort. [[See more in glossary of terms]].

## Steps to Create and Submit Translations


### 1) Check for Existing Accessible Descriptions
- maybe a step to verify there is somethign to translate?

### 2) Run the A11y View
- Use the Accessibility (A11y) View to understand the content that requires translation.
- The a11y view is an HTML file that can be found next to the simulation's HTML file. For example, navigate to `http://localhost:8080/greenhouse-effect/greenhouse-effect_a11y_view.html` when you are running a development server.
- The A11y View displays the screen reader content in a simulation and provides documentation on how and when content is read to the user.
- Run the simulation in English first to familiarize yourself with the content. Then, run it in your language by adding the query parameter ?locale={{LOCALE_CODE}} to the URL (e.g., ?locale=es for Spanish).

### 3) Locate English Strings in the Code
- Find the English strings that need translation in the .ftl files. Most strings are located in the simulation repository. You can find them at files like this: `{{ROOT_SIMS_DIRECTORY}}/{{SIM_REPO}}/strings/{{SimName}}_en.ftl`
- Example: `phetsims/ohms-law/strings/OhmsLaw_en.ftl`
- Some strings will be located in other PhET repositories used by the simulation. They can be found in files like this:
```
{{ROOT_SIMS_DIRECTORY}}/{{COMMON_CODE_REPO}}/strings/{{RepoName}}_en.ftl
{{ROOT_SIMS_DIRECTORY}}/{{COMMON_CODE_REPO}}/strings/{{ComponentName}}_en.ftl
```
Example:
```
phetsims/scenery-phet/strings/SceneryPhet_en.ftl
phetsims/scenery-phet/strings/FaucetNode_en.ftl
```

### 4) Find or Create Translated Strings in the babel Repository
- Translated accessibility strings using Fluent.js are stored in the Babel repository:
```
{{ROOT_SIMS_DIRECTORY}}/babel/fluent/{{repo-name}}/{{RepoName}}_{{LOCALE_CODE}}.ftl
{{ROOT_SIMS_DIRECTORY}}/babel/fluent/{{repo-name}}/{{ComponentName}}_{{LOCALE_CODE}}.ftl
```
Example:
```
phetsims/babel/fluent/ohms-law/OhmsLaw_es.ftl
phetsims/babel/fluent/scenery-phet/SceneryPhet_es.ftl
phetsims/babel/fluent/scenery-phet/FaucetNode_es.ftl
```
- For each English .ftl file you want to translate:
  - If the file exists: Open it for editing.
  - If the file does not exist: Create a new file with the same name as the english file, replacing _en with your language code (e.g., _es for Spanish).

Example:
  - From: phetsims/ohms-law/strings/OhmsLaw_en.ftl
  - Create or Edit: phetsims/babel/fluent/ohms-law/OhmsLaw_es.ftl

### 5) Generate an Initial Translation (optional)
- Use an AI-based tool such as ChatGPT or Gemini to create an initial translation of the English .ftl file. Save the generated translations into the corresponding files in the babel repository.

### 6) Refine and Contextualize Translations
- Review and edit the AI-generated translations for:
  - Syntax: Make sure that Message names in the translated file have the same spelling and capitalization as the English file.
  - Accuracy: Ensure the translation accurately reflects the original meaning.
  - Context Appropriateness: Confirm that the translation fits the simulation's context.
  - Quality: Ensure that translations are correct for all cases and that reused Terms and Messages are correct in all contexts they are used.
  - Language Specifics: Adjust for language differences, such as gender, number, and word order. Consider adding reusable Terms or Messages at the top of the translation file if needed.

### 7) Compile Strings (Modulify)
⚠️ **You will need to need to do this every time you make changes to any of the .ftl files.
If you do not do this, reloading the sim will not show your changes.** ⚠️
- Compile the Fluent strings into modules that the simulation can load.
  - Open the command line and navigate to the simulation repository: `cd {{ROOT_SIMS_DIRECTORY}}/{{SIM_REPO}}`
  - Run the modulify command: `grunt modulify`

### 8) Test the Translation
  - Run the simulation in your browser with the locale query parameter set to your language code (e.g., ?locale=es for Spanish).
  - Check the developer tools console for any error messages that may indicate issues with the translation files.
  - Interact with the simulation to verify the content.

### 9) Submit the Translation
  - Once you are satisfied with the translations, submit a pull request to the PhET GitHub repository with the changes.
    - Commit Changes: Commit the changes to the .ftl files in the babel repository.
    - Open a Pull Request: Create a pull request with the changes to the PhET GitHub repository.
    - Review and Approval: The PhET team will review and approve the submission to verify functionality. Addres any feedback or changes.
    - Finalization: Once approved, your translation will be merged into the main repository. Your translation will be included in future releases of the simulation.

## Examples

To review example of Fluent.js strings and translations, see the following:
- [Greenhouse Effect English Fluent Strings](https://github.com/phetsims/greenhouse-effect/tree/main/strings)
- [Greenhouse Effect French Fluent Strings](https://github.com/phetsims/babel/blob/main/fluent/greenhouse-effect)


### Questions to discuss with team
- Is greenhouse-effect the best example to use? Confusion around molecules-and-light relationship.
    - It is our most complete example. Just make it clear in the documentation.
    - Consider renaming greenhouse effect strings to MoleculesAndLightStrings_en.ftl
    - Try to find the ohms law strings if we can. That would be a more simple example.

- Did we have any other translations finished that we can include?
- What documentation should we point to for "PhET Development Environment Setup"?
  - FOR NOW, refer to the phet-development-overview.md
- Steps for submitting a pull request?

References to translation documentation:
https://docs.google.com/document/u/1/d/e/2PACX-1vSYc8f01StQ7e2nQWBA38BZfLoqkm6rkn-F9BzTmxdNgazOzFfLDm5RI-3I3IdKccuBFQpFdT2ST5Px/pub
https://phet.colorado.edu/en/for-translators

- These steps are not compatible whith the "SceneryStack" development setup/environment.
- Decide how integrated this system needs to be with SceneryStack. Understand the changed required for the process and
  create new steps for that process.
- Right now, the process is set up for PhET code contributions

Making changes to PhET code through SceneryStack: https://scenerystack.org/learn/modifying-scenerystack/#getting-the-latest-code

Add a note to the translation info page on the website referring to this document.

Refer to key terms document glossary.
    The glossary will refer to the description design course or other materials.


Add a section here about the format and organization of the file. Reusable terms at the top. For sim translation files,
strings are organized by the order in which they appear in the a11y view.