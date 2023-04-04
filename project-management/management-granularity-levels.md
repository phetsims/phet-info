# Granularity Levels in Project Management Software

As we explore project management software, it has become clear that there are different levels of interest in github issue integration as well as management usage with these softwares. This document's goal is to first and foremost identify and define the different levels of project management granularity in our organization, discuss the diferring opinions related to Github integration, as well as identify the relationship between github and a project management software at the different levels.

## Github Integration Main Arguments
Below you will find the two main arguments that have arisen when talking about Github integration. Obviously there is much more nuance to these discussions that cannot be captured here, but the opinions are summarized to give context around processes that may develop as well as inform the levels of granularity identified later on in this document.

### Github Integration is Necessary

Main Points:
- Integration will reduce duplication for day-to-day workflows
- It is difficult to separate github level issues from iteration specific goals
- Integration will reduce space for errors
- Integration will reduce project maintenance work

Overall, proponents of this argument see difficulty in separating our day-to-day workflows in Github from planning work done in a project management tool. They also see increased value to members across departments who may not rely on Github as much as the development team. Many decisions are already made at the Github issue level. If the project management tool is not integrated with Github it may not reflect these decisions, and lead to erroneous planning down the line. It is most beneficial to know that all workflows are synced up so that we can truly visualize all the work being completed and how the progress of a task rolls up into its associated epic. 

### Github Integration is Unnecessary

Main Points:
- Github issues are too granular for high level overviews
- Proper integration takes time to set up and maintain
- Hidden integration errors could lead to confusion and miscommunication
- Planning workflows exist that would not rely on github issue integration for management

It is important to note that it is not that proponents of this argument see no value in Github integration, rather they do not see it as a critical element of successful project management tool adoption. Proponents of this argument believe that high level project planning, focusing on epics, grant deliverables, etc. does not require the granular view of github issues. Most importantly they believe that the project would still receive a high amount of benefit from adopting project management tools focused solely on high level planning, and that issue level granularity is covered by our workflows in Github. There is also concern that integration could negatively tamper with our current Github workflows. Lag in one or both tools, as well as erroneous syncing could make our granular level issue management worse rather than better. Thorough research and testing would be required to ensure integration would not hamper already positive experiences.

## Levels of Granularity
This document identifies four levels of granularity from an Epic level, to a Subtask level. This is not to indicate that there is no spectrum between all these levels, but rather to provide concrete points to assess our workflow needs along the spectrum.

### :weight_lifting: Epic Level 
Example: Epics, grant deliverables, releases

#### Summary
The Epic level is only focused on the due dates, and timeline for sim releases, publications, and other grant/client deliverables. It can be helpful to think of this level on a quarter-to-quarter, or even year-to-year basis. This level requires high input from administrative and management positions, but is only used as a reference for developers, designers, QA, etc.

#### Github's Role
Benefits could potentially come from task roll up, but other than that zero github input needed. Task roll up would only require a one-way sync.

### :woman_scientist: Phase Level
Example: Iteration planning, epic milestones

#### Summary
The Phase level is focused on scheduling epics and epic milestones (design complete, development complete, etc.) inside of two week chunks. This level of planning requires prioritization of epics, when we plan to work on epics within our iteration schedule, as well as the amount of effort we can put in towards each epic. A high amount of input is needed from administrative and management positions, with a medium amount of input needed from others. This is mostly used as a reference for the majority of team members with iteration planning being the highest point of contribution.

#### Github Role
It is not uncommon for epic milestones to have associated github issues ( dev tests, initial screen development, etc.). Integration for these epic milestone issues would be necessary, however can be filtered by a label. These issues would require one way sync only. It is not expected that team members will comment or update cards from the management end, rather the Github issue would drive the progress in management tooling we choose.

### :microscope: Task Level
Example: Iteration goals, iteration task tracking

#### Summary
The Task level is focused on the specific tasks and goals we wish to accomplish during an iteration. This level would help us track the status of an iteration, as well as add emergent work that was unexpected and may delay an iteration goal (and perhaps even an epic). Teams may reference this level daily to discuss work for the day during standups, as well as update task status, add new goals, move tasks into and out of the backlog. This level requires a medium amount of input from administrative and management positions, with a high amount of input needed from others. Team members consistently contribute and reference this level.

#### Github's Role
Currently PhET uses a mixture of issues and draft issues (cards) to organize this work. These issues must be integrated with a two-way sync. Team members are allowed to update issues both in github as well as in management tooling, reducing the need to jump back and forth between tools. Labels would need to be used to sync issues appropriately, as well as filter which issues are synced and which are not.

### :dna: Subtask Level
Example: Issues, bugs, commits

#### Summary
The Subtask Level is focused on the incremental work that gets done on a day-to-day and sometimes hour-to-hour basis. This level includes tracking commits, designer feedback/comments, discussions, bug reports, and any issues that may be worked on at any time wether they are directly related to an epic or not. Team members may reference this level multiple times throughout a work day to track their own contributions, as well as the current work status of team members. This level requires very little input from administrative and management positions, with almost all input coming from the individual. This level is critical to an individual's workflow and in many cases is unique and specific to the individual.

#### Github's Role
This level requires the largest amount of integration with Github. All issues will be synced over. Team members can work seamlessly in either tool and expect efficiency and updates both ways. Labels may be used to organize issues on project boards, but will not be used to filter. Two-way sync is critical at this level, as is flexibility or a large cap on the amount of monthly syncs we are allowed.
