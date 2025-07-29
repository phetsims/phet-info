# {{SIM_NAME}} {{VERSION}} checklist

## Prep
- [ ] **Review all open issues** 
- [ ] **Schedule kick-off meeting** 
  - [ ] Establish scope of this release 
  - [ ] Triage open issues and decide what to include or defer 
- [ ] **Ensure design doc has sections for relevant features and/or create feature-specific design docs**
- [ ] **Scope of this release**
  - [ ] Verify [color contrast](https://docs.google.com/document/d/1rlVX9DHXclCtpcFV-5YAoA0uI0Ui_H1mzPJck7v8PcM/edit?tab=t.0)
  - [ ] Optional: paste all issues that will be included, or list features - these will be useful for release notes

## Design

- [ ] **Update design doc to reflect sim updates, as needed** 
- [ ] **Pre-publication items**
  - [ ] Update teacher tips (query parameters, new features, model simplification changes, etc.)
  - [ ] Update screenshots
  - [ ] Update release notes with developer
  - [ ] Add to Essential Exceptions doc ([guidelines](https://docs.google.com/document/d/1NjLGmGr2Oi9A9D9SCH5WAgOhpA7ysmuvv0Jn_batPVU/edit?tab=t.0#heading=h.c063kqhkkg))
- [ ] **Post-publication items**
  - [ ] Tag new inclusive features on website
  - [ ] Alert translators if there have been significant string changes
  - [ ] Write newsletter announcement
  - [ ] Update website credits
  - [ ] Ask web devs to add to PhET Studio
  - [ ] Create 2-3 example presets ([guidelines](https://docs.google.com/document/d/1gZmobd5h1VBZxjwT6ZuDhFIRWWQvQUKD_VgUDZW5-io/edit?tab=t.0))
  - [ ] Decide as a team if a postmortem is applicable, and schedule (Date: //)

## Implementation

- [ ] **Release Notes completed**
  - [ ] Copy [release notes template](https://github.com/phetsims/simula-rasa/blob/main/doc/release-notes.md) into sim repo
  - [ ] Finalize with designer
- [ ] **Sim team sign-off** (Date: //)
- [ ] **Code review completed** (Date: //)
- [ ] **Pre-publication items**
  - [ ] Verify credits with lead (Team, Contributors, QA, Graphic Arts, Sound Design, any Thanks -
    see [conventions](https://github.com/phetsims/joist/blob/main/js/CreditsNode.js))
  - [ ] Add CT tests for public query parameters that need testing. See examples
    in [listContinuousTests.js](https://github.com/phetsims/perennial/blob/main/js/listContinuousTests.js)
- [ ] **Published** (Date: //)

## QA

- [ ] **Dev testing started** (Date: //)
- [ ] **Dev testing completed** (Date: //)
- [ ] **First RC published** (Date: //)
  - [ ] Test matrices put
    in [Testing Matrices Folder](https://drive.google.com/drive/folders/0B6CMwxdP0NGYbW9fTGNCODdYVjQ)
- [ ] **RC testing completed** (Date: //)
