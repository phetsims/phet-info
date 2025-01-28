# Translation Guide for Accessible Descriptions

## Who is this guide for?
This guide is designed for translators looking to create and submit translations for _accessible descriptions_
using the Fluent system.

## Two Systems for Translations 

PhET has two systems for submitting translations, one for short visual strings and one for longer _accessible descriptions_.
1. The _PhET Translation Utility (HTML5)_ works well for the short strings that you can see visually in the simulation - visual strings like labels for checkboxes. Volunteer translators have used the PhET Translation Utility (HTML5) to translate the visual strings of sims into more than 129 languages. At this time, this system cannot handle longer phrases found in the _accessible descriptions_. To learn more about the PhET Translation Utility (HTML5), you can find [information here](https://phet.colorado.edu/en/for-translators) and [documentation here](https://docs.google.com/document/u/1/d/e/2PACX-1vSYc8f01StQ7e2nQWBA38BZfLoqkm6rkn-F9BzTmxdNgazOzFfLDm5RI-3I3IdKccuBFQpFdT2ST5Px/pub).
2. Fluent provides a higher level translation system in order to address the language-specific changes required when translating the longer phrases found in _accessible descriptions_. Once a translator is familiar with some basic fluent syntax, they can create, test and submit grammatically correct translations of _accessible descriptions_.

**Note: Translators may need to use both systems to create a complete translation. Some accessible descriptions may use the same strings as the visual strings. In this case, both the PhET Translation Utiltiy (HTML5) and Fluent must be used to create a complete translation.** 
## Introduction to Fluent

### What is Fluent?
Fluent is a localization system developed by Mozilla.
It is particularly useful for the translation of complex
dynamic content such as the descriptions designed for accessibility.
More information about inclusive features can be found [here](https://phet.colorado.edu/en/inclusive-design/features). 
These _accessible descriptions_ are in addition to and seperate from the visual text that appfears on-screen.  Using Fluent, translators can effectively handle language-specific challenges like number
and gender agreement, word order, and other differences that exist across languages.

## Prerequisites for Translating Accessible Descriptions

Using Fluent requires a working development environment, basic knowledge of Fluent's syntax, and some familiarity with how refer to and organize _accessible descriptions- in the _Fluent files_.

### PhET Development Environment Setup
- Set up a development environment for the simulation you want to translate by following the [PhET Development Overview](https://github.com/phetsims/phet-info/blob/main/doc/phet-development-overview.md).
Make sure you can run the simulation locally in your browser and access and edit the code. **Reach out to the community when you need help.**

### Fluent Syntax Knowledge
- Review Fluent's documentation to understand how to structure and format translations effectively.
  - Project Fluent - https://projectfluent.org/
  - Fluent Syntax Guide - https://projectfluent.org/fluent/guide/
  - The most important Fluent concepts for PhET simulations include Terms, Messages, Placeables, and Selectors. Ensure you are familair with the syntax for these four Fluent concepts.

### Description Framework Terminology 
- PhET has developed a simple description design framework that assists designers in designing the complex strings needed to create dynamci _accessible descriptions_. As you work with the Fluent files you will notice references to description categories in the comments surrounding the descriptions. Familiarizing yourself with the description design framework terminology may assist you in your translation effort. [[See more in glossary of terms]].

## Steps to Create and Submit Translations

### 1) Locate Accessible Descriptions in the Code
- Find the English strings that need translation. Fluent files use the .ftl extension. Most strings are located in the simulation repository. You can find them at files like this: `{{ROOT_SIMS_DIRECTORY}}/{{SIM_REPO}}/strings/{{SimName}}_en.ftl`
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

### 2) Run the A11y View
- Use the Accessibility (A11y) View to understand the content that requires translation.
- The a11y view is an HTML file that can be found next to the simulation's HTML file. For example, navigate to `http://localhost:8080/greenhouse-effect/greenhouse-effect_a11y_view.html` when you are running a development server.
- The A11y View displays the screen reader content in a simulation and provides documentation on how and when content is read to the user.
- Run the simulation in English first to familiarize yourself with the content. Then, run it in your language by adding the query parameter ?locale={{LOCALE_CODE}} to the URL (e.g., ?locale=es for Spanish).
- If the simulation supports Voicing, enable it in the Preferences Dialog. Play with the simulation to hear the Voicing content in context.

### 3) Find or Create Translated Strings in the babel Repository
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

### 4) Generate an Initial Translation (optional)
- Use an AI-based tool such as ChatGPT or Gemini to create an initial translation of the English .ftl file. Save the generated translations into the corresponding files in the babel repository.

### 5) Refine and Contextualize Translations
- Review and edit the AI-generated translations for:
  - Syntax: Make sure that Message names in the translated file have the same spelling and capitalization as the English file.
  - Accuracy: Ensure the translation accurately reflects the original meaning.
  - Context Appropriateness: Confirm that the translation fits the simulation's context.
  - Quality: Ensure that translations are correct for all cases and that reused Terms and Messages are correct in all contexts they are used.
  - Language Specifics: Adjust for language differences, such as gender, number, and word order. Consider adding reusable Terms or Messages at the top of the translation file if needed.

### 6) Compile Strings (Modulify)
⚠️ **You will need to need to do this every time you make changes to any of the .ftl files.
If you do not do this, reloading the sim will not show your changes.** ⚠️
- Compile the Fluent strings into modules that the simulation can load.
  - Open the command line and navigate to the simulation repository: `cd {{ROOT_SIMS_DIRECTORY}}/{{SIM_REPO}}`
  - Run the modulify command: `grunt modulify`

### 7) Test the Translation
  - Run the simulation in your browser with the locale query parameter set to your language code (e.g., ?locale=es for Spanish).
  - Check the developer tools console for any error messages that may indicate issues with the translation files.
  - Interact with the simulation to verify the content.

### 8) Submit the Translation
  - Once you are satisfied with the translations, submit a pull request to the PhET GitHub repository with the changes.
    - Commit Changes: Commit the changes to the .ftl files in the babel repository.
    - Open a Pull Request: Create a pull request with the changes to the PhET GitHub repository.
    - Review and Approval: The PhET team will review and approve the submission to verify functionality. Addres any feedback or changes.
    - Finalization: Once approved, your translation will be merged into the main repository. Your translation will be included in future releases of the simulation.

## Examples

To review example of Fluent.js strings and translations, see the following:
- [Greenhouse Effect English Fluent Strings](https://github.com/phetsims/greenhouse-effect/tree/main/strings)
- [Greenhouse Effect French Fluent Strings](https://github.com/phetsims/babel/blob/main/fluent/greenhouse-effect)