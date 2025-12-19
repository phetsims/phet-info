# {{SIM_NAME}} {{VERSION}} Republication Checklist

(see [Sim Checklist](https://github.com/phetsims/phet-info/blob/main/checklists/sim-checklist.md#design-pre-qa) for any items missing from this checklist that are a part of your sim update (e.g., PhET-iO))

## Design

### Prep

- [ ] Review all open issues
- [ ] Revise design doc or create new doc for updated version.

### Scope

- [ ] Kick-off meeting (Date: //)
  - [ ] Establish scope of this release (what new features are being added?)
  - [ ] Triage open issues and decide what to include or defer
- Scope of additional features for this release (Basics Sounds, Core Description, Alternative Input, Pan and Zoom, Interactive Highlights, Dynamic Locale, PhET-iO/Studio are assumed as of Nov 2025)
  - [ ] Sound & Sonification
  - [ ] Interactive Description
    - [ ] Mobile description included
  - [ ] Voicing (specify Core or Full)
  - [ ] Regional Character Sets
  - [ ] Optional: paste all issues that will be included, or list features - these will be useful for release notes
    - [{{GITHUB PLACEHOLDER LINK}}](https://github.com/phetsims/phet-info)
    - {{NEW SIM FEATURE PLACEHOLDER, e.g., Stopwatch added.}}
- [ ] Identify any common code components that do not yet have support for features, and elevate need to #planning Slack channel
- [ ] Create feature-specific milestone deadlines for simulation sub-epics in Monday. Reviewed and updated on a regular basis.

### Design (Pre-QA)

- [ ] Update (or create) design doc(s) to reflect sim updates and feature additions, as needed
- **If applicable to your update:**
  - [ ] Core Description reviewed by external designer - [CORE REVIEW CHECKLIST](https://github.com/phetsims/phet-info/blob/main/checklists/core-description-review-checklist.md)
  - [ ] Verify [color contrast](https://docs.google.com/document/d/1rlVX9DHXclCtpcFV-5YAoA0uI0Ui_H1mzPJck7v8PcM/edit?tab=t.0)
  - [ ] Add to Essential Exceptions doc ([guidelines](https://docs.google.com/document/d/1NjLGmGr2Oi9A9D9SCH5WAgOhpA7ysmuvv0Jn_batPVU/edit?tab=t.0#heading=h.c063kqhkkg))
  - [ ] Carefully review `?showPointerAreas` for mouse and touch areas
  - [ ] Check strings using `?stringTest=dynamic` for layout changes and readability
  - [ ] PhET-iO
    - [ ] Determine any custom PhET-iO needs
    - [ ] PhET-iO tree review complete
    - [ ] `phetioFeatured` elements identified/updated
    - [ ] Create/update examples.md
- [ ] Lead designer final review before QA (Date: //)
  - [ ] (if applicable) Obtain external design team/partners approval

### Publication Prep

- [ ] Update teacher tips (query parameters, new features, model simplification changes, etc.)
- [ ] Update screenshots (including screen-specific screenshots)
- [ ] Update release-notes.md with developer
- [ ] Update responsible_dev.json, as appropriate
- [ ] Verify updates to credits with team (Team, Contributors, QA, Graphic Arts, Sound Design, any Thanks - see [conventions](https://github.com/phetsims/joist/blob/main/js/CreditsNode.js))

### Post Publication

- [ ] Update Sim Page Info, including tagging any new inclusive features on website
- [ ] Create a GitHub issue for @oliver-phet to alert translators if there have been significant string changes (manual process since Nov 2024)
- [ ] Write newsletter announcement
- [ ] Update website credits
- [ ] Message #website-public to ask web devs to add the latest version to PhET Studio
- [ ] Create 2-3 example presets ([guidelines](https://docs.google.com/document/d/1gZmobd5h1VBZxjwT6ZuDhFIRWWQvQUKD_VgUDZW5-io/edit?tab=t.0))
  - [ ] If already in PhET Studio, recreate the example presets on latest ([instructions](https://docs.google.com/document/d/1gZmobd5h1VBZxjwT6ZuDhFIRWWQvQUKD_VgUDZW5-io/edit?tab=t.0#heading=h.tk5tep7h8l7a))
- [ ] Decide as a team if a postmortem is applicable, and schedule (Date: //)

## Developer Implementation

- [ ] Feature-complete (Date: //)
- [ ] Sim team sign-off (Date: //)
- [ ] Update model.md, if needed. (Date: //)
- [ ] Update implementation-notes.md, if needed. (Date: //)
- [ ] Code review completed (Date: //)
- [ ] Pre-publication items
  - [ ] Memory leak testing
  - [ ] Verify credits with lead (Team, Contributors, QA, Graphic Arts, Sound Design, any Thanks -
    see [conventions](https://github.com/phetsims/joist/blob/main/js/CreditsNode.js))
  - [ ] Finalize release-notes.md with designer.
  - [ ] Add CT tests for public query parameters that need testing. See examples
    in [listContinuousTests.js](https://github.com/phetsims/perennial/blob/main/js/listContinuousTests.js)
- [ ] Published (Date: //)

## QA

- [ ] Dev testing issue created (Date: //)
- [ ] Dev testing started (Date: //)
- [ ] Dev testing completed (Date: //)
- [ ] First RC published (Date: //)
  - [ ] Test matrices put
    in [Testing Matrices Folder](https://drive.google.com/drive/folders/0B6CMwxdP0NGYbW9fTGNCODdYVjQ)
- [ ] RC testing completed (Date: //)
