# Fluent Translation Guide

This guide will help you understand how to create and submit translations for PhET simulations using Fluent.js.

## Introduction to Fluent

### What is Fluent?
Fluent is a localization system developed by Mozilla that allows for more flexible and expressive translations than basic
formatting. It is particularly useful for complex strings that require dynamic content or context-specific translations,
such as long descriptions for accessibility.

### Difference Between Fluent.js Translations and Rosetta

PhET uses an existing translation system called Rosetta for strings that can be seen visually in the simulation.
However, Fluent.js is necessary for translations that require more complex formatting or context-specific content, like detailed descriptions for accessibility features.
For more information about Rosetta, see [Rosetta Documentation]({{LINK TO ROSETTA DOCS}}).

## Prerequisites

Ensure you have the following tools and resources before starting:

1) Fluent Syntax Knowledge
Review the the Fluent documentation to understand how to structure and format translations effectively.
Project Fluent - https://projectfluent.org/
Fluent Syntax Guide - https://projectfluent.org/fluent/guide/

The most important Fluent.js concepts for PhET simulations include Terms, Messages, and Selectors.

2) PhET Development Environment Setup
Set up a development environment for the simulation you want to translate by following the PhET Development Overview.
Make sure you can run the simulation locally in your browser and access and edit the code.

## Steps to Create and Submit Translations

1) Run the A11y View
Use the Accessibility (A11y) View to understand the content that requires translation.

2) Understanding the content
The A11y View displays the screen reader content in a simulation and provides documentation on how and when content is read to the user.
Run the simulation in English first to familiarize yourself with the content. Then, run it in your language by adding the query parameter ?locale={{LOCALE_CODE}} to the URL (e.g., ?locale=es for Spanish).

3) Locate English Strings in the Code
Find the English strings that need translation in the .ftl files. Most strings are located in the simulation repository. You can find them
at files like this:
```{{ROOT_SIMS_DIRECTORY}}/{{SIM_REPO}}/strings/{{SimName}}_en.ftl```

Example:
```phetsims/ohms-law/strings/OhmsLaw_en.ftl```

Some strings will be located in other PhET repositories used by the simulation. They can be found in files like this:
{{ROOT_SIMS_DIRECTORY}}/{{COMMON_CODE_REPO}}/strings/{{RepoName}}_en.ftl
{{ROOT_SIMS_DIRECTORY}}/{{COMMON_CODE_REPO}}/strings/{{ComponentName}}_en.ftl

Example:
```phetsims/scenery-phet/strings/SceneryPhet_en.ftl```
```phetsims/scenery-phet/strings/FaucetNode_en.ftl```

4) Find or Create Translated Strings in the babel Repository

Translated accessibility strings using Fluent.js are stored in the Babel repository:

```
{{ROOT_SIMS_DIRECTORY}}/babel/fluent/{{repo-name}}/{{RepoName}}_{{LOCALE_CODE}}.ftl
{{ROOT_SIMS_DIRECTORY}}/babel/fluent/{{repo-name}}/{{ComponentName}}_{{LOCALE_CODE}}.ftl
```

Example:
```phetsims/babel/fluent/ohms-law/OhmsLaw_es.ftl```
```phetsims/babel/fluent/scenery-phet/SceneryPhet_es.ftl```
```phetsims/babel/fluent/scenery-phet/FaucetNode_es.ftl```

For each English .ftl file you want to translate:
If the file exists: Open it for editing.
If the file does not exist: Create a new file with the same name as the english file, replacing _en with your language code (e.g., _es for Spanish).

Example:
From: phetsims/ohms-law/strings/OhmsLaw_en.ftl
Create or Edit: phetsims/babel/fluent/ohms-law/OhmsLaw_es.ftl

5) Generate an Initial Translation (optional)
Use an AI-based tool such as ChatGPT or Gemini to create an initial translation of the English .ftl file. Save the generated translations into the corresponding files in the babel repository.

6) Refine and Contextualize Translations
Review and edit the AI-generated translations for:
- Accuracy: Ensure the translation accurately reflects the original meaning.
- Context Appropriateness: Confirm that the translation fits the simulation's context.
- Quality: Ensure that translations are correct for all cases and that reused Terms and Messages are correct in all contexts they are used.

Adjust for language differences, such as gender, number, and word order. Consider adding reusable Terms or Messages at the top of the translation file if needed.

7) Compile Strings (Modulify)

Compile the Fluent strings into modules that the simulation can load.

!! You will need to need to do this every time you make changes to the .ftl files !!

- Open the command line and navigate to the simulation repository:
```cd {{ROOT_SIMS_DIRECTORY}}/{{SIM_REPO}}```

- Run the modulify command:
```grunt modulify```

8) Test the Translation

- Run the simulation in your browser with the locale query parameter set to your language code (e.g., ?locale=es for Spanish).
- Check the developer tools console for any error messages that may indicate issues with the translation files.
- Interact with the simulation to verify the content.

9) Submit the Translation

Once you are satisfied with the translations, submit a pull request to the PhET GitHub repository with the changes.
- Commit Changes: Commit the changes to the .ftl files in the babel repository.
- Open a Pull Request: Create a pull request with the changes to the PhET GitHub repository.
- Review and Approval: The PhET team will review and approve the submission to verify functionality. Addres any feedback or changes.
- Finalization: Once approved, your translation will be merged into the main repository. Your translation will be included in future releases of the simulation.

## Examples

To review an example of Fluent.js files, see the following:
- [Greenhouse Effect English Fluent Strings](https://github.com/phetsims/greenhouse-effect/tree/main/strings)
- [Greenhouse Effect French Fluent Strings](https://github.com/phetsims/babel/blob/main/fluent/greenhouse-effect)
