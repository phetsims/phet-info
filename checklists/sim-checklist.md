# {{SIM_NAME}} 1.0 main checklist

## Design

### **Prep**

- [ ] **Sim folder and design doc created** (Date: //)
  - [ ] Create sim folder in PhET Sim Design Folder on [Google Drive]((<https://drive.google.com/drive/folders/0B6CMwxdP0NGYUUhvZnlCUDF0bGc>) AND [Microsoft Sharepoint](https://o365coloradoedu.sharepoint.com/sites/PHYS-phet-pilot/PhET%20Files/Forms/AllItems.aspx?id=%2Fsites%2FPHYS%2Dphet%2Dpilot%2FPhET%20Files%2FPhET%20Files%2FPhET%20Sim%20Design&viewid=3aa550f4%2Df9ef%2D4871%2Dbcb3%2Da192486a9aaa)
    - [ ] In the SharePoint folder, add link to Google Drive folder
  - [ ] Create design doc in the sim folder on Google Drive

### Scope

- [ ] **Review user feedback**
  - [ ] *If a
    Port:* [Google Form suggestions reviewed](https://docs.google.com/spreadsheets/d/1KkvutfIVwZLi5-jz_DVP3zC8jXkzF32-hzMI4ztB1uY/edit?resourcekey#gid=324007787&fvid=677625918)
    - Ask developer to move tickets from Unfuddle to GitHub (and create the new repo if not done)
  - [ ] *If a new
    sim:* [Google Form suggestions reviewed](https://docs.google.com/spreadsheets/d/1KkvutfIVwZLi5-jz_DVP3zC8jXkzF32-hzMI4ztB1uY/edit?resourcekey#gid=324007787&fvid=898967246)
- [ ] Schedule kick-off meeting
- Scope of additional features for this release (Basics Sounds, Core Description, Alternative Input, Pan and Zoom, Interactive Highlights, Dynamic Locale, PhET-iO/Studio are assumed as of Nov 2025)
  - [ ] Sound & Sonification
  - [ ] Interactive Description
    - [ ] Mobile description included
  - [ ] Voicing (specify Core or Full)
  - [ ] Regional Character Sets
- [ ] *For Ports*: Paste all issues that will be included OR list features (useful for release notes):
  - [{{GITHUB PLACEHOLDER LINK}}](https://github.com/phetsims/phet-info)
  - {{NEW SIM FEATURE PLACEHOLDER, e.g., Stopwatch added.}}
- [ ] Create feature-specific milestone deadlines for simulation sub-epics in Monday. Reviewed and updated on a regular basis.

### Design (Pre-QA)

- [ ] Ensure design doc has sections for relevant features or create feature-specific design docs
- [ ] Learning goals and standards identified
- [ ] Design concept complete
- [ ] Wireframes complete
- [ ] Mockups complete
  - [ ] Mockups checked for [color contrast](https://docs.google.com/document/d/1rlVX9DHXclCtpcFV-5YAoA0uI0Ui_H1mzPJck7v8PcM/edit?tab=t.0)
  - [ ] [Essential Exceptions](https://docs.google.com/document/d/1buKmqjn9hiYrUpPjcEeAmgX0HDd-KO2G87aKBq5Gjjw/edit?usp=sharing) noted
- [ ] Carefully review `?showPointerAreas` for mouse and touch areas
- [ ] Check strings using `?stringTest=dynamic` for layout changes and readability
- [ ] Core Description reviewed by external designer - [CORE REVIEW CHECKLIST](https://github.com/phetsims/phet-info/blob/main/checklists/core-description-review-checklist.md)
- [ ] PhET-iO
  - [ ] Determine any custom PhET-iO needs
  - [ ] PhET-iO tree review complete
  - [ ] `phetioFeatured` elements identified
  - [ ] Create examples.md
- [ ] [Interviews](https://drive.google.com/drive/folders/0B6CMwxdP0NGYVkYyOTZBVk8tdDA?resourcekey=0-rOMQFMdLt8biIpZ5iooCnQ) complete (Date: //)
  - [ ] Results reported to team
  - [ ] Notes pasted into design doc
  - [ ] Interview recordings backed up to Sharepoint
- [ ] No more feature requests (Date: //)
- [ ] Lead designer final review before QA (Date: //)
  - [ ] (if applicable) Obtain external design team/partners approval

### Publication Prep

- [ ] *If a Port:* If the legacy sim or project name differs from HTML5, notify the website team at least on month prior to publication ([example](https://github.com/phetsims/models-of-the-hydrogen-atom/issues/161))
- [ ] Teacher Tips created, uploaded, and added to sim design folder on SharePoint
- [ ] Verify credits with team (Team, Contributors, QA, Graphic Arts, Sound Design, any Thanks - see [conventions](https://github.com/phetsims/joist/blob/main/js/CreditsNode.js))
- [ ] Create Main screenshot and Auxiliary screenshots (up to 3 additional) for sim assets folder (read [this](https://github.com/phetsims/QA/blob/main/documentation/qa-book.md#screenshots))
- [ ] Create Screen-specific screenshots for metadata service (
  see [naming convention](https://github.com/phetsims/website/issues/1322#issuecomment-1010320827))
- [ ] [Prepare and Update Sim Page Info](https://docs.google.com/document/d/1JtFR0paPJIU19ybn3SwkMO-ZvRCr2a_KRMPUe-OikAc/edit?tab=t.0#heading=h.94p3cgxenan4) (keywords, (filter) categories, description, learning goals, related sims, inclusive features)
- [ ] **Make sim visible on website (Invisible -> Published)**
  - [ ] Clear "Metadata caches" on
  the [Basic Administration Caches](https://phet.colorado.edu/?wicket:bookmarkablePage=:edu.colorado.phet.website.admin.AdminCachesPage)
  page

### Post Publication

- [ ] *If a Port:* Review legacy gold star activities. For appropriate activities, tag the HTML5 version and UNTAG the deprecated version. Contact Diana for support.
- [ ] Draft newsletter entry
- [ ] Ask web devs to add to PhET Studio (#website-public Slack channel)
- [ ] Create 2-3 example PhET Studio presets ([guidelines](https://docs.google.com/document/d/1gZmobd5h1VBZxjwT6ZuDhFIRWWQvQUKD_VgUDZW5-io/edit?tab=t.0))
- [ ] Announce sim publication in #general Slack channel and celebrate!
- [ ] Create a GitHub issue for Oliver `@oliver-phet` to alert translators that a new sim is available for translation for new sim publications OR if there have been significant string changes (manual process since Nov 2024)
- Legends of Learning (LoL) Partnership Tasks
  - [ ] [Icons](https://docs.google.com/document/d/1GmLNE31gs8hQYGze3xwmN9k7B6gu7lQ7wJe2phqdH9Y/edit) for each
  screen created and uploaded to Drive
  - [ ] [Metadata](https://docs.google.com/spreadsheets/d/1umIAmhn89WN1nzcHKhYJcv-n3Oj6ps1wITc-CjWYytE/edit#gid=562591429)
  for each screen (description, vocab words, questions for before/after sim use)
  - [ ] [Deliver](https://docs.google.com/spreadsheets/d/1umIAmhn89WN1nzcHKhYJcv-n3Oj6ps1wITc-CjWYytE/edit#gid=0)
- ~~Send Simulation Notification from the Admin page (to alert translators)~~
- [ ] Decide as a team if a postmortem is applicable, and schedule (Date: //)
<!-- If this todo comes back into focus for new sims, leaving here for now: - [ ] Create "sim primer" issue~~ (out of scope for 2024 onward) -->

## Developer Implementation

- [ ] Repository created by
  following [new-repo-checklist.md](https://github.com/phetsims/phet-info/blob/main/checklists/new-repo-checklist.md) (
  Date: //)
- [ ] Development started (Date: //)
- [ ] Sim is "feature complete" (Date: //)
- [ ] QA team "first look" (Date: //)
- [ ] Interviews may happen around here (see above)
- [ ] Sim team sign-off (Date: //)
- [ ] Code review completed (Date: //)
- [ ] Sim dev test completed (Date: //)
- [ ] Sim RC tests completed (Date: //)
- [ ] Pre-publication items
  - [ ] Add CT tests for public query parameters that need testing. See examples
    in [listContinuousTests.js](https://github.com/phetsims/perennial/blob/main/js/listContinuousTests.js)
- [ ] Published (Date: //)

## QA

- [ ] *If a Port:* Legacy sim tested for bugs; issues reported in repo
- [ ] Dev testing issue created (Date: //)
- [ ] Dev testing started (Date: //)
- [ ] Dev testing completed (Date: //)
- [ ] First RC published (Date: //)
  - [ ] Test matrices put
    in [Testing Matrices Folder](https://drive.google.com/drive/folders/0B6CMwxdP0NGYbW9fTGNCODdYVjQ)
- [ ] RC testing completed (Date: //)
