<!-- 

Helpful Links

- Core Description Guide: [Description Design Guide and Tips:  Core](https://docs.google.com/document/d/1kCivjmuXiMzrFkYUigZFgDkssoEWGW_-OaXDk9myV00/edit?tab=t.0#heading=h.rj5etgrq1nf7)  
  Core Description Overview: [https://github.com/phetsims/phet-info/blob/main/doc/core-description-overview.md](https://github.com/phetsims/phet-info/blob/main/doc/core-description-overview.md)  
- QA Instructions on Testing Core Description: [https://github.com/phetsims/qa/blob/bcef426d259224dc6caac6da49e1ae70b6e10187/documentation/qa-book.md\#core-description](https://github.com/phetsims/qa/blob/bcef426d259224dc6caac6da49e1ae70b6e10187/documentation/qa-book.md#core-description)  
- Exemplars 

**To begin Core Description review, the responsible designer should:**

* Copy this checklist to a new GitHub issue titled "Core Description Review" and labeled `design:description`.
* Complete (or delete) the **Sim-Specific Instructions** section.
* Delete (or ~~strikethrough~~) checklist items and sections that are not relevant.
* Replace {{GITHUB_ISSUE_LINK}} with links to GitHub issues.
* Assign the GitHub issue to the designer who is doing the review.

* The responsible designer is responsible for removing the irrelevant parts
* A checked-off item doesn't mean "no problem here", it means "it was reviewed"
* Problems can be noted in side issues that reference this issue

!! DELETE THIS COMMENT BLOCK WHEN COPYING THE CHECKLIST !!

-->

# {{SIM_NAME}} {{VERSION}} Core Description Review Checklist

Goals of the Checklist

1. Meet WCAG: Ensure WCAG for Core Description requirements are being met, as often as possible.  
2. Meet PhET Standard: Provide best possible user experience given resource constraints.  
3. Reduce the time that QA spends reviewing sim for items that could be caught earlier in design.  
4. Provide Quick Reference as complement to the Core Description Guide

Audience (who will use this?)

1. Designer who created the Core Description to ensure they haven’t forgotten anything.  
2. Additional content expert to ensure language is pedagogically correct and relevant.  
3. An external reviewer (less desirable) to ensure quality of description is there.
   
## General Instructions

As you work through this list, be sure to keep notes to share with others at weekly Core Description meeting (idea of “continuous learning”).

Test using the simulation [A11y View](https://bayes.colorado.edu/dev/phettest/phetmarks/), as well as testing with screen-reader software to confirm the content is accessible and accurate.

- [Tip sheet VoiceOver](https://docs.google.com/document/d/1qz0Dm2lA67tRhgw1GaHVeOSnldBoMj7AT5UE_UaXz1U/edit)  
- [Tip sheet NVDA](https://docs.google.com/document/d/1pgfyEER7ZlpJlXSwvSCbNBuoCa5oOexc7QvTuFZu-Mo/edit)  
- [Tip sheet JAWS](https://docs.google.com/document/d/1aggemqGsb2CdR7PxgLG50kOg4ZwBPM2M3eI3okyZHJ8/edit)

As you work through the list, keep these 'general good-practice' reminders in the forefront.

- Does each description component sound natural? (Read it aloud to yourself)  
- Does it need more grammar/syntax? Less?
- Are descriptions (names, help text, summaries, etc.) pedagogically relevant? Decorative content and sometimes spatial placement are not critical for all sims.
- Anything the team has already decided is out of scope, for example, is [documented](#determined-to-be-out-of-scope-for-core-description) to inform the reviewer in advance

## Sim-Specific Instructions

- {{LINK TO DESIGN DOC WHERE DESCRIPTION IS FOUND}}
- {{INSTRUCTIONS FOR REVIEWER WRITTEN BY RESPONSIBLE DESIGNER}}

### Determined to be out of scope for Core Description

1. {{ NOTE }} or {{GITHUB_ISSUE_LINK}}  
2. {{ NOTE }} or {{GITHUB_ISSUE_LINK}}  
3. …

## Reviewer Checklist

**DATE OF REVIEW COMPLETION:** {{DATE}}

**REVIEWER:** {{REVIEWER NAME}}

### PDOM Structure & Navigation

- [ ] Verify Descriptions/A11y View matches the Simulation Design Doc  
- [ ] Ensure tab order makes sense (limit bouncing, similar items grouped)  
- [ ] Headings are used only when necessary, limit sub-levels  
- [ ] Components in each heading section make sense for the context of the sim (e.g., Play Area vs. Control Area)

### Screen Summary (review for each screen)

- [ ] Overview is succinct, static (if possible), general  
- [ ] Describes current screen and includes most important components  
- [ ] Current details is at a high level (generic) and supports different presets  
  - Example: PhET-iO hide/show, and/or don’t mention things that could be hidden  
- [ ] Interaction hint is screen-specific and supports different presets (e.g., PhET-iO hide/show)

### Home Screen

- [ ] Each screen has accessible names  
- [ ] Help text gives “playful” invitation to explore the screen

### Accessible Names

- [ ] Unique  
- [ ] Clear  
- [ ] aria-roledescription not repeated in name  
- [ ] Title case

### Accessible Help Text

- [ ] Implicitly guides users, as needed  
- [ ] Starts with verb when appropriate, consistent with role  
- [ ] Always true for any state  
- [ ] Sentence case with punctuation

### Custom Objects

- [ ] Confirm custom objects have a designed accessible role description (to avoid default: `web-application`)  
- [ ] Role and name and/or help text and consistent (e.g., when role is movable, use ‘move’ not ‘drag’)  
- [ ] Multi-step interactions: Descriptions accurate at each step (SEE [DESIGN GUIDE](https://docs.google.com/document/d/1kCivjmuXiMzrFkYUigZFgDkssoEWGW_-OaXDk9myV00/edit?tab=t.0#heading=h.rj5etgrq1nf7) FOR DETAILS)

### Visual Content Descriptions

- [ ] Non-interactive information is described in static or dynamic state descriptions (e.g., on-screen text, pop ups are described using accessible paragraph)

### Responsive Descriptions

If present, review responses given when pedagogically important events or state changes occur.

- [ ] \[Object Responses\] match format: Phrase fragments, no sentence casing, no period at end  
- [ ] Numerics in Object Responses are formatted to read naturally  
  - e.g., For ordered pairs in a coordinate grid, no ( ) are used  
  - e.g., Decimals are rounded to 2 or 3 decimal places to match visible accuracy  
- [ ] \[Context Responses\] match format: Full phrases, sentence casing, with punctuation  
- [ ] Context Responses are limited to pedagogically important and/or simple changes in the sim to confirm a user’s action or describe the impact of the action  
- [ ] In design doc: Object/Context responses are labeled correctly  
- [ ] Review order of content responses  
  - e.g., changing info is prioritized as first-read info, (“2.74, \-1.89, on primary parabola” rather than “on primary parabola, 2.74, \-1.89”)  
  - e.g., object responses come before context responses  
- [ ] Provide suggestions for any obvious and simple responses you feel are missing from the sim.

### **Preferences & Keyboard Help Dialog**

- [ ] Verify Keyboard Help Dialog has clear accessible alternative to the visual text description/icons.  
- [ ] Verify Sim-specific controls in Preferences have accessible text.

### **Capitalization for Core Description**

- [ ] accessibleName: Title case, no punctuation. Example: “Concentration Probe”  
- [ ] accessibleHelpText: Sentence case, with punctuation. Example: “Move probe.”  
- [ ] accessibleObjectResponse: Phrase fragments, no sentence casing, no period at end. Example: “2 kilometers from mass 1”  
- [ ] accessibleContextResponse: Full phrases, sentence casing, with punctuation. Example: “Current parabola saved to grid.”  
- [ ] accessibleParagraph: a paragraph of full sentences, with sentence case and punctuation  
- [ ] accessibleListNode: Strive for consistency (stick with natural and either all phrases or all sentences with all the same punctuation)

### **Component-Specific Criteria (recent areas of concern/confusion)**

NOTE: This section lists common problem areas for components noticed during sim design and are recognized to be redundant. See the [Core Description Design Guide](https://docs.google.com/document/d/1kCivjmuXiMzrFkYUigZFgDkssoEWGW_-OaXDk9myV00/edit?tab=t.0#heading=h.rj5etgrq1nf7) for full details and components not listed here.

#### Checkboxes

- [ ] Ensure help text always reads true (e.g., “Show or hide…” “Explore with or without…”)  
- [ ] Include an Accessible Context Response to give user context for the consequence of their actions

#### Accessible Paragraphs or Accessible Headings

- [ ] Verify that additional descriptions are clear, concise, and necessary.  
- [ ] Verify that components are grouped under related headings (nested headings in buttons don’t look like headings in A11y view right now. ERASE WHEN FIXED)  
- [ ] Paragraphs exist for text inside accordion boxes and pop-ups
