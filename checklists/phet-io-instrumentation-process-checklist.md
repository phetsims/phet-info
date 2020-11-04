# PhET-iO Instrumentation Process Checklist

## Initial Steps

### Gathering requirements
- [ ]  Create a google doc for documenting requirements
- [ ]  Identify internal and any client iO requirements
- [ ]  Determine the developer that will be instrumenting the simulation. It is best for the simulation's responsible 
developer to perform the PhET-iO instrumentation. They have important
insight into the structure, history, trade-offs, and other important details of the simulation implementation
that will facilitate the instrumentation.  If the responsible developer is not available for instrumentation, even a 
consulting role would be helpful.

### Before touching any code
- [ ] Create a "PhET-iO Instrumentation Process Checklist" GitHub issue in the simulation repository. Copy this checklist/guide to the issue
description (top issue comment) for tracking. Link back to this checklist via `/blob/<SHA>/` so that the specific guide
you used is preserved.
- [ ] If this is a retrofit, create a baseline dev version. This can be useful for identifying whether bugs or memory issues 
have been introduced during instrumentation, or were pre-existing.  This also creates a benchmark to reference against  
for memory-leaks, sim size, performance, etc. Document the dev version in the sim's PhET-iO Github issue.
- [ ] Developer to gather knowledge about the instrumentation process. These topics are crucial to understanding before
 attempting to outfit a simulation with PhET-iO:
  - [ ] A general overview of PhET-iO, please read the [Overview section](https://github.com/phetsims/phet-io/blob/master/doc/phet-io-instrumentation-technical-guide.md#overview).
  - [ ] Make sure you understand what is contained in PhET-iO API, see [API Management](https://github.com/phetsims/phet-io/blob/master/doc/phet-io-instrumentation-technical-guide.md#api-management).
- [ ] Design review: PhET-iO instrumentation provides an opportunity to review the condition of the sim, and make improvements to both the UX and code base.  With a designer:
  - [ ] Review open GitHub issues. Identify issues that should be addressed during instrumentation.
  - [ ] Identify places where the sim should be brought up to PhET UX standards.
  - [ ] Identify sim-specific UI components that should be replaced with common-code UI components. Using common-code where possible allows us to leverage common-code instrumentation, and provide a consistent UX across sims. 

  
### Initial meeting

#### Prior to initial meeting:
- [ ] If a retrofit, the developer:
    - [ ] Performs preliminary assessment of state of the code (does it conform to newer code standards)
    - [ ] Reviews open issues in the repo
- [ ] Developer performs a "best guess" initial instrumentation to populate Studio with something. This involves at least passing tandems to many model Properties and  `Tandem.REQUIRED` elements.

#### Brief initial meeting (developer and designer):
For example, see [how-to-design-phet-io-features-for-a-simulation.md](https://github.com/phetsims/phet-io/blob/master/doc/how-to-design-phet-io-features-for-a-simulation.md).
Think about how a researcher or 3rd party may wish to configure the simulation or collect data from it, and make sure
that is supported by the instrumentation. For example, some simulations will need custom higher-level events (such as
whether the user created a parallel circuit), for events that are useful, easy to compute in simulation code and
difficult to compute in wrapper code.  Or a simulation may need to be configurable in a way that is not already supported
by the instrumentation you have already completed.  These features should be determined in the PhET-iO design meeting. 
Sometimes it is preferred to have a skeleton, or developer's "best guess" before this meeting so that there is more to 
play with in Studio. Use your judgement! 
- [ ] Identify the broad goals
- [ ] Identify which requirements/goals will be hard and most important (ie set intial bunny population)
- [ ] Are some of the requirements desirable for PhET brand (eg via query parameters)
- [ ] Create a preliminary schedule (milestones) with google calendar reminders
- [ ] Evaluate any client requirements, and work these into the design document.
    
## Development

### If a retrofit
- [ ] Developer should perform a thorough code review. 
  - [ ] Bring the sim up to PhET code standards, including conversion to ES6 (classes, arrow functions, etc.)
  - [ ] Prefer common code UI to custom implementations
  - [ ] Deprecated code should not be used; use latest common code components instead. Most likely these have better PhET-iO instrumentation.
  - [ ] If there is a branch with significant changes, consider merging before instrumentation.
  - [ ] Complete any planned refactorings.
  - [ ] Address TODOs in the code.
  - [ ] Identify opportunities to use/improve PhET design patterns. Consulting [phet design patterns](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md) may be helpful.
  - [ ] If the sim uses vibe for sound, consider porting to tambo.
  - [ ] If significant changes were required as the result of code review, publish a new benchmark dev version.
  - [ ] Instrumentation and code review commits should be separate
 
### Initial development

- [ ] During this step, please consult with the [PhET-iO Instrumentation Guide](https://github.com/phetsims/phet-io/blob/master/doc/phet-io-instrumentation-technical-guide.md)
 to do the sim instrumentation. Create a separate github issue called "PhET-iO Instrumentation Implementation" and copy 
 the appropriate checklist from that guide into it.
- [ ] New Sim --  build out according to initial requirements.
- [ ] Tricky items postponed for discussion
- [ ] Developer generates design questions to bring back to meetings
  - [ ] Is there uninstrumented common code that needs design time
  - [ ] Is the Studio tree structure acceptable

### Iteration during development
- [ ] With working studio carefully designers carefully review tandem structure and studio tree 
- [ ] In depth design meetings (developer not always needed): 
  - [ ] Generate github issue(s) with change requests
  - [ ] Iterative back and forth with developer, github and meeting discussions as needed.
  
### Review 
- [ ] If you turned off validation via `?phetioValidation=false` or specify the package.json flag "phet.phet-io.validation: false", 
time to turn validation back on (by removing the query paramater or package.json entry) and address any issues discovered.
- [ ] Review the "overrides" file, and potentially move phetioDocumentation over to the sim from the file. All 
      `phetioFeatured` metadata should be in overrides file, and not in sim-specific code. `phetioFeatured` can be declared in
      common code to factor out duplication. See overrides convention decision in https://github.com/phetsims/states-of-matter/issues/303#issuecomment-653139520
- [ ] The PhET-iO instrumentation process should be code reviewed
- [ ] The PhET-iO instrumentation should be code reviewed. Please create a new issue for this.
- [ ] Compare performance and memory with pre-instrumentation dev version(s).

### Publication
- [ ] Conduct a dev test with QA. The PhET-iO publication process is often quite different because it can be client-driven. 
- [ ] After initial dev test, further publications may be necessary depending on the specific use. Talk to the designer or project lead for more information. 
- [ ] If delivering a dev version to the client see 
[Initial dev release to client](https://github.com/phetsims/phet-io/blob/master/doc/phet-io-instrumentation-technical-guide.md#initial-dev-release-to-client) 
(Note: you may be able to combine the initial dev test with one needed for this step). 
- [ ] If moving on to RC, create a QA RC test template issue and include the PhET-iO section.
- [ ] Please make changes or create an issue if you find these instructions to be incomplete, inconsistent, or incorrect.
- [ ] After publishing, add your instrumented simulation to the spreadsheet here: https://docs.google.com/spreadsheets/d/1pU9izdNQkd9vr8TvLAfXe_v68yh-7potH-y712FBPr8/edit#gid=0

