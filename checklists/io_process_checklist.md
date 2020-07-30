# PhET-iO Instrumentation Checklist

## Initial Steps

### Gathering requirements
- [ ]  Create a google doc for documenting requirements
- [ ]  Identify internal and any client iO requirements

### Initial meeting
Prior to initial meeting:
  - [ ] If a retrofit, the developer:
    - [ ] Performs preliminary assessment of state of the code (does it conform to newer code standards)
    - [ ] Reviews open issues in the repo
  - [ ] Developer performs a "best guess" initial instrumentation to populate Studio with something. This involves at least passing tandems to all/most model Properties and  `Tandem.REQUIRED` elements.

Brief initial meeting (developer and designer):
- [ ] Identify the broad goals
- [ ] Identify which requirements/goals will be hard and most important (ie set intial bunny population)
- [ ] Are some of the requirements desirable for PhET brand (eg via query parameters)
- [ ] Create a preliminary schedule (milestones) with google calendar reminders
    
 ## Development
 If a retrofit
- [ ] Developer should perform a thorough code review
- [ ] Instrumentation and code review commits should be separate
 
 ### Intitial development
- [ ] New Sim --  build out according to initial requirements.
- [ ] Instrument enough to populate Studio
- [ ] Passing Tandem through to required tandems
- [ ] Best guess at providing tandems optional tandems
- [ ] Tricky items postponed for discussion
- [ ] Developer generates design questions to bring back to meetings
  - [ ] Is there uninstrumented common code that needs design time
            tandem structure

 ### Iteration and publication
- [ ] With working studio carefully designers carefully review tandem structure and studio tree 
- [ ] In depth design meetings (developer not always needed): 
  - [ ] Generate github issue(s) with change requests
  - [ ] Iterative back and forth with developer, github and meeting discussions as needed.
- [ ] Ready for overrides
- [ ] Review the overrides.js file to see if items need to be moved back to code
- [ ] Publish sim
