# Fluent Translation Guide

## Steps for creating and submitting a translation for a PhET simulation using Fluent.js.

1. Learn Fluent Syntax
Review the Fluent Syntax Guide to understand how to structure and format translations effectively.

 2. Set Up Translation Tools
Install necessary tools such as a text editor (e.g., VS Code) and a version control system (e.g., Git).
Clone the relevant PhET simulation repository from PhET's GitHub page.

3. Run the A11y View
Run the simulation in the a11y view to understand the content. Run it in English to review description strings in context. Then, run in your language. There may be strings that are already translated if they live in common code repositories.

4. Find the English strings in code.
English strings will live in multiple files. The files can be found in both the sim repo and common code repos. These files hold the contents that require translations.
{{ROOT_SIMS_DIRECTORY}}/{{SIM_REPO}}/strings/{{SimName}}_en.ftl
{{ROOT_SIMS_DIRECTORY}}/{{COMMON_CODE_REPO}}/strings/{{RepoName}}_en.ftl
{{ROOT_SIMS_DIRECTORY}}/{{COMMON_CODE_REPO}}/strings/{{ComponentName}}_en.ftl

Examples:
phetsims/ohms-law/strings/OhmsLaw_en.ftl
phetsims/scenery-phet/strings/SceneryPhet_en.ftl
phetsims/scenery-phet/strings/FaucetNode_en.ftl

5. Find translated strings in babel repo.
Babel holds PhET's translated strings. Accessibility strings using fluent.js will live in {{ROOT_SIMS_DIRECTORY}}/babel/fluent/{{repo-name}/. Example: phetsims/babel/fluent/ohms-law/.

6. For each file that you want to translate, find the corresponding file in the babel repo.
If the file does not exist, create it. The file needs to have the same name as the English file, but with the language code changed. For example: phetsims/ohms-law/strings/OhmsLaw_en.ftl to phetsims/babel/fluent/ohms-law/OhmsLaw_es.ftl

 7. Generate an AI Translation
Use an AI-based translation tool (e.g., Google Translate or DeepL) to create an initial translation of the English `.ftl` file.
Save the generated translations into the files that you created in the babel repo.

 8. Refine and Contextualize Translations
Review and edit the AI-generated translations for accuracy, cultural relevance, and context-specific appropriateness.
Ensure key terms align with the simulation's intended meaning, referencing documentation where needed.
Refer to the (PhET’s) fluent syntax guide to adjust for language differences commonly found in sims, e.g., adjusting for gender, number and word order. Tip: Fluent has a way to handle reusable strings. Add reusable strings to top of translation file.

9. Save and compile strings (aka modulify).
Strings are built into modules that are loadable by the simulation. To do this, run `grunt modulify` in the command line in the sim repo.
    $ cd {{ROOT_SIMS_DIRECTORY}}/{{SIM_REPO}}
    $ grunt modulify
   You will need to do this after every change to see the updated strings.

 6. Validate Translation Syntax
 Run the simulation with the new `.ftl` files to verify the translation displays correctly without syntax errors.
(Hopefully specific error messages will be shown in the dev tools.)

 7. Test Translation for Accuracy and Usability
Play with the simulation using the A11y View to check the simulation’s functionality with the translated descriptions to ensure names for user interface elements, help text, and other surrounding descriptions remain clear and effective. Don’t forget to check description strings in both panels of the A11y View.
Instructions on how to find all the content to translate.

 8. Submit the Translation
 Commit the finalized `.ftl` file to a new branch in your forked repository.
 Open a pull request to the main PhET repository, including a summary of your translation process and any decisions made during refinement.

 9. Address Feedback
Respond to reviewer comments, refining translations as necessary to meet project standards.
Once your pull request is accepted, have another translator review your translation using the A11y View of the sim.

 10. Reflect on the Process
Document your experience, including challenges encountered and strategies used.
Share insights with the community to support other contributors.
