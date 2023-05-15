# PhET Development Overview

## Overview

PhET Interactive Simulations creates free, open source educational simulations in science and math, which you can find
at the PhET website. This document explains PhET’s libraries, practices and patterns for developing interactive
simulations in HTML5. This document is also available
at https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md. For discussion and feedback,
please visit
the [GitHub Discussions forum](https://github.com/orgs/phetsims/discussions).

**[Overview](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#overview)**

**[Getting Started](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#getting-started)**

**[Creating a New Sim](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#creating-a-new-sim)**

**[Building and Testing](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#building-and-testing)**

**[Source Code and Dependencies](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#source-code-and-dependencies)**

**[Checking out the HTML5 Code from GitHub](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#checking-out-the-html5-code-from-github)**

**[Master is Unstable: Accessing Rigorously-Tested Code](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#master-is-unstable-accessing-rigorously-tested-code)**

**[Original Java/Flash Source Code](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#original-javaflash-source-code)**

**[3rd-Party Dependencies](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#3rd-party-dependencies)**

**[Licensing](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#licensing)**

**[Coding Style Guidelines](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#coding-style-guidelines)**

**[Platforms](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#platforms)**

**[Modularity with ES6 Modules](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#modularity-with-es6-modules)**

**[Layout](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#layout)**

**[Compiling the Code](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#compiling-the-code)**

**[Offline Operation](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#offline-operation)**

**[Published Versions](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#published-versions)**

**[Development Process and Checklist](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#development-process-and-checklist)**

**[Utilities and Instrumentation for Development and Testing](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#utilities-and-instrumentation-for-development-and-testing)**

**[Working with GitHub Issues](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#working-with-github-issues)**

**[Embedding a Simulation in Your Website](https://github.com/phetsims/phet-info/blob/master/doc/phet-development-overview.md#embedding-a-simulation-in-your-website)**

## Getting Started

### Prerequisites

* You will need to be able to use the command line. This is called Terminal on macOS and Command Prompt on Windows.
* `git` is necessary to check out PhET code from GitHub. You can download and install git
  from http://git-scm.com/downloads. On macOS, the preferred way of getting git is by installing Xcode command-line
  tools. The instructions for that are at
  https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.
* `node` and `npm` are necessary to install dependencies and run build code processes. Download & install node+npm
  from https://nodejs.org/en/
  * After installing, run `npm config set save false` and `npm config set package-lock false` so that
    package-lock.json files are not created.
* Create a directory where you intend to check out the PhET source code: `mkdir phetsims`
* For building the simulations, install the grunt command line utility: `npm install -g grunt-cli` (May require `sudo`
  if you don't have sufficient permissions).
* An HTTP Server is necessary to launch the simulations during development (though not necessary for built simulations).
  Some systems already have Apache, or you can install something like `npm install http-server -g`. (May require `sudo`
  if you don't have sufficient permissions).
* Serve files from the `phetsims/` directory. For `http-server` this can be done like so:
  * Change into the phetsims directory `cd phetsims/`
  * Run the http server program (with caching turned off to help with iteration) `http-server -c-1`

### Checking out the code

Method 1 (recommended): Get all PhET repos

* Change directory to phetsims: `cd phetsims`
* Get [phetsims/perennial](https://github.com/phetsims/perennial): `git clone https://github.com/phetsims/perennial`
* Run "clone-missing-repos.sh": `./perennial/bin/clone-missing-repos.sh`

Method 2: Manually get specific PhET repos

* Change directory to phetsims: `cd phetsims`
* Run the `git clone` commands listed in a simulation README.md file, such
  as https://github.com/phetsims/example-sim/blob/master/README.md

When running the first `git clone` command, macOS may show a dialog that says: The “git” command requires the command
line developer tools. Would you like to install the tools now? In this case, press “Install”.

### Installing Dev Dependencies

Install dev dependencies via `npm install` in the following directories:

```
cd chipper
npm install
cd ../perennial-alias
npm install
cd ../perennial
npm install
cd ../${directory of the sim you are working on}
npm install
```

### Transpile TypeScript

* Change directory to the build tools: `cd chipper/`
* Run the TypeScript transpiler: `node js/scripts/transpile.js --watch` which starts a process that will auto-transpile
  when files change.
* For more details about TypeScript, please
  see [PhET's TypeScript Quick Start Guide](https://github.com/phetsims/phet-info/blob/master/doc/typescript-quick-start.md)

### View in the Browser

* Open a browser to the path for one of the
  simulations: http://localhost:8080/example-sim/example-sim_en.html?brand=adapted-from-phet (port or path may depend on
  your HTTP server configuration)
  Now you can test modifying the simulation code and see the changes by refreshing the browser.
* You can also use this to test on remote devices after looking up your ip address. If developing on Chrome, note that
  it can be helpful to set "Disable cache (while DevTools is open)" (see the devtools settings).

### Build Standalone Simulations

* Change to the directory of the simulation you are working on, such as `cd example-sim/`
* Run `grunt --brands=adapted-from-phet`
* Open a browser to the path for one of the
  simulations: http://localhost:8080/example-sim/build/adapted-from-phet/example-sim_en_adapted-from-phet.html (port or
  path may depend on your HTTP server configuration)

### Questions

* Questions should be directed to the [Developing Interactive Simulations in HTML5 Google
  Group](https://groups.google.com/g/developing-interactive-simulations-in-html5).

## Creating a New Sim

After checking out the dependencies and installing grunt-cli in the preceding instructions, you can create your own
simulation using the template.

1. Check out the template sim, called ‘simula-rasa’ using this git clone command:
   `cd phetsims`
   `git clone https://github.com/phetsims/simula-rasa.git`
2. Install the chipper dependencies:
   `cd chipper`
   `npm install`
3. Install the perennial dependencies:
   `cd ../perennial`
   `npm install`
4. Install the perennial-alias dependencies:
   `cd ../perennial-alias`
   `npm install`
5. Use the perennial ‘grunt’ task to create a new sim, like so (still in the perennial directory):
   `grunt create-sim --repo=NAME --author=AUTHOR`
   For instance, if the simulation is going to be named Acceleration Lab and the author is Jane Doe, then you could put:
   `grunt create-sim --repo=acceleration-lab --author="Jane Doe"`
6. In chipper, run the transpiler watch process and specify your new repo as a target:
   `cd ../chipper`
   `node js/scripts/transpile.js --watch --repos=acceleration-lab`
7. Test the created simulation in the browser and make sure it launches. It should be a blank simulation. Write to the
   Developing Interactive Simulations in HTML5 Google Group if you run into problems.

## Building and Testing

The process described above is sufficient for iterating during development. When you are ready to build the source
code (including images, sounds and other assets) into an optimized HTML file suitable for student or client usage,
you can build the simulation using the chipper grunt build process.

### Building the Simulation with chipper

1. Open Git Bash (Windows) or Terminal (macOS) and type:

```
cd example-sim
npm install
npm prune
npm update
npm install grunt-cli -g
cd ../chipper
npm update
cd ../example-sim
grunt
```

2. Open a browser to the path to test it:
   http://localhost:8080/example-sim/build/phet/example-sim_en_phet.html

### Working with Git and GitHub

* Pulling the latest changes
* Creating an issue
* Committing
* Submitting a pull request

## Source Code and Dependencies

Our simulations and dependencies are hosted publicly on GitHub: https://github.com/phetsims

We have 150+ repositories for the simulations and their dependencies, listed
at: https://github.com/orgs/phetsims/repositories.

PhET Simulations are based on a Model/View separation pattern. This pattern and others used in PhET Simulations are
described at https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md

The tables below depict the most significant common code libraries used by PhET Simulations. The simulations provide
their own model and view implementations often building with common code components. Salient relationships between repos
are identified, but many repos are cross-cutting. For instance, nearly every repo
uses [tandem](https://github.com/phetsims/tandem/) for PhET-iO support and [axon](https://github.com/phetsims/axon/) for
Observer/Listeners patterns. The LOC reports the total lines of code (includes comments and blank lines) to give a rough
sense of the size. Please note the LOC is not directly correlated to complexity--for
instance, [scenery-phet](https://github.com/phetsims/scenery-phet/) has many lines of code, but is less complex because
it is made up of many separate, modular components.

### View - Common Code

| Repository  | LOC | Description |
| ------------- | ------------- | ---------- |
| [joist](https://github.com/phetsims/joist/)  | 10,000  | Simulation loading, homescreen + navigation bar, screen management. Uses some user interface components from [sun](https://github.com/phetsims/sun/). Uses [scenery](https://github.com/phetsims/scenery/) to render and process input. Runs the animation loop.
| [sun](https://github.com/phetsims/sun/) | 13,000  | Graphical user interface components, such as buttons and checkboxes which could be useful in any application context. Built using [scenery](https://github.com/phetsims/scenery/).
| [scenery-phet](https://github.com/phetsims/scenery-phet/)  | 25,000  | Simulation-specific components, such as probes, sensors, buckets, magnifying glasses, etc. Built using [scenery](https://github.com/phetsims/scenery/).
| [scenery](https://github.com/phetsims/scenery/)  | 86,000  | Foundational library for representing graphics (rendering to SVG, canvas or WebGL), handling input and generally abstraction for the browser and cross-platform support. Shapes are represented using [kite](https://github.com/phetsims/kite/). Observer and emitter patterns use [axon](https://github.com/phetsims/axon/). Support for alternative input and accessibility features.
| [tambo](https://github.com/phetsims/tambo/)  | 6,000  | Sound effects and sonification. Uses [axon](https://github.com/phetsims/axon/) for some observer/listeners support.
| [brand](https://github.com/phetsims/brand/)  | 100  | Provides support for the main supported brands "PhET" and "PhET-iO" and hooks for clients to develop their own branding.
| [twixt](https://github.com/phetsims/brand/)  | 2,000  | Support for tweening and animation. Can be used to animate user interface components or artwork in the view or model elements directly.

### Model - Common Code

| Repository  | LOC | Description |
| ------------- | ------------- | ---------- |
| [kite](https://github.com/phetsims/kite/)  | 16,000  | Shapes and geometry. Mathematics implemented using [dot](https://github.com/phetsims/dot/)
| [dot](https://github.com/phetsims/dot/)  | 21,000  | Mathematical objects such as Vector, Matrix, and corresponding numerical algorithms
| [axon](https://github.com/phetsims/axon/)  | 8,000  | Data structures for the observer pattern (Property) and listener pattern (Emitters).
| [phet-core](https://github.com/phetsims/phet-core/)  | 4,000  | Basic utility & support data structures and algorithms
| [tandem](https://github.com/phetsims/tandem/)  | 5,000  | Simulation-side code to support PhET-iO instrumentation.

### Tooling & Other

| Repository  | LOC | Description |
| ------------- | ------------- | ---------- |
| [chipper](https://github.com/phetsims/chipper/)  | 10,000  | Tools for developing and building simulations. Uses code in [perennial-alias](https://github.com/phetsims/perennial-alias/) for some tasks.
| [perennial](https://github.com/phetsims/perennial/)  | 11,000  | Maintenance tools that won't change with different versions of chipper checked out (always runs in master).
| [perennial-alias](https://github.com/phetsims/perennial/)  | 11,000  | Copy of perennial that can run on non-master SHAs.
| [sherpa](https://github.com/phetsims/sherpa/)  | -  | All of our 3rd-party dependencies. Some such as font-awesome or lodash are used in every simulation and some such as numeric or three.js are sim-specific.

## Checking out the HTML5 Code from GitHub

Our example-sim repository README.md includes a list of git clone commands that will check out the example simulation
and all of its dependencies: https://github.com/phetsims/example-sim

And to clone some of our in-development sims:
`git clone git://github.com/phetsims/forces-and-motion-basics.git`
`git clone git://github.com/phetsims/build-an-atom.git`

All repositories should be cloned into the same directory so that relative paths will work.

Here is a full list of all phetsims repositories. If the sim won’t launch due to a missing dependency, you may need to
check out some more of these repos: https://github.com/phetsims?tab=repositories

Also note that this will check out the ‘master’ branch of all of our dependencies, which may create breaking changes
intermittently if you remain up-to-date with them. If you run into any breaking changes, please notify us immediately.
Also, we recommend developing your code on a public repo such as GitHub to enable us to test and update your simulations
as common dependencies are changed.

## Master is Unstable: Accessing Rigorously-Tested Code

The master branch of the PhET simulation and library repositories is constantly under development and not guaranteed to
be stable. It is our intent that the master branch of simulations + libraries will build and run properly, but sometimes
the code goes through intermediate states where errors can be introduced. On the other hand, our published simulations
have been rigorously tested across 18+ platforms and are the most stable option. If you are adapting a PhET simulation,
or would like to access simulation code that corresponds directly to one of our published versions, then you will need
to check out specific SHA revisions in all of the appropriate repositories. Checking out these fixed, tested revisions
is also important when working on a release-candidate branch of a simulation. Here are the instructions:

1. First, identify the version for which you want to check out the source code, for
   example: https://phet.colorado.edu/sims/html/area-builder/latest/area-builder_en.html
2. Navigate to a file named dependencies.json at the same path, for
   example: https://phet.colorado.edu/sims/html/area-builder/latest/dependencies.json
3. Download the dependencies.json file to the root of the simulation directory.
4. Open a command prompt and cd into the root of the simulation directory.
5. Run `grunt checkout-shas`. This step will read from the dependencies.json file and check out all of the SHAs
   corresponding to the entries in the file.
6. To checkout the SHA for the simulation itself, first look up the SHA in the dependencies file, move the dependencies
   file to some other location or delete it, and use `git checkout` to check it out the appropriate SHA. (Note future
   version of `grunt checkout-shas` may handle this last step).
7. Inspect the simulation and its dependencies to make sure `grunt checkout-shas` had the intended effect of getting the
   right SHA for each repo.

Now you can use the published source code. To restore each branch to master, you can run `grunt checkout-master`.

### Exceptions and Caveats:

1. Running `grunt checkout-shas` gives errors when the working copy is not committed. These grunt commands are currently
   only supported for clean git repos. Stashing may be a way around this problem. Also, if you want to use dependencies
   from a different version than in the SHAs, that will have to be done as an additional manual step.
2. When working in a branch, `grunt checkout-master` will check out the master branch and additional manual steps will
   be required to get back to the desired branch(es). For instance, this is an issue when working with the
   “adapted-from-phet” branch of brand.

## Original Java/Flash Source Code

Follow the directions at this link to get the source code for original Java and Flash version of the
simulations: https://phet.colorado.edu/en/about/source-code

After checking it out (could take 30+ minutes), the source code for the simulations are located in (for example):
svn-checkout/trunk/simulations-java/simulations/forces-and-motion-basics

## 3rd-Party Dependencies

PhET Simulations use around 3 open source 3rd-party dependencies for the deployed source code, and more for the build
phase. They are all included with the source code checkouts in the sherpa repository. The libraries and licenses are
described in this 3rd-party dependency licensing document.

## Licensing

New simulations should be published under GPLv3 and reusable library dependencies should be published as MIT.

## Coding Style Guidelines

To improve the readability and maintainability of PhET Simulation code, we have identified several style recommendations
for writing code and documentation:

* The PhET Code Review Checklist is available
  at https://github.com/phetsims/phet-info/blob/master/checklists/code-review-checklist.md provides additional steps to
  make sure a simulation is well written. This checklist is used for publication of any new PhET simulation to make sure
  they are consistent and maintainable. It enumerates steps including but not limited to coding style.

* We use ESLint to lint our code. See https://github.com/phetsims/chipper/blob/master/eslint/README.md.

*

An [IntelliJ IDEA formatting XML file](https://github.com/phetsims/phet-info/blob/master/ide/idea/phet-idea-codestyle.xml)
to automatically format code. This is the ground truth for how PhET code should be formatted. Our example-sim also shows
how to use our libraries idiomatically as well as a good example of code commenting + documentation.

We also tend to agree with most of the guidelines set out in [idiomatic.js](https://github.com/rwldrn/idiomatic.js/).

## Platforms

The simulation should be tested and run on the platforms linked below. In our experience to date, some optimization is
often required to obtain acceptable performance on tablets such as the iPad.

System requirements: https://phet.colorado.edu/en/help-center/running-sims/general#q11-header

## Modularity with ES6 Modules

The current iteration of PhET's simulation codebase uses native Javascript modules, which were introduced in ECMAScript

6. For PhET specifically, default exports are only used (as opposed to named exports). ES6 Modules are used to support
   modularization of the JavaScript code. Information about ES6 Modules can be
   found [here](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules). Examples of how it will be used
   by
   PhET can be seen in the [Example Simulation](https://github.com/phetsims/example-sim) (specifically the source files
   in
   the js directory).

## Layout

### Design:

Minimum width x height: 768x504 (1.52:1, inside Mobile Safari)

The simulation should scale isometrically such that all portions are visible at any resolution. An example of this type
of scaling can be seen in the example simulation.

## Compiling the Code

A minification and unification process is implemented in our repo https://github.com/phetsims/chipper. This can be used
to create a single-file HTML that contains all images and audio, and is suitable for download for offline usage.

Here's an example of how to compile example-sim into a single HTML file. Other sims would be compiled similarly. This
assumes that you have all of example-sim's dependencies checked out in your local working copy.

```
% cd example-sim
% npm install
% grunt build --brands=adapted-from-phet
% cd build/adapted-from-phet
% ls
dependencies.json
example-sim-128.png
example-sim-600.png
example-sim_all_adapted-from-phet_debug.html
example-sim_en_adapted-from-phet.html
xhtml/
```

## Offline Operation

It is a requirement that all PhET simulations can be downloaded and run off line in all identified browsers from the
file:// URL. PhET’s chipper build process (described above) produces a single file that can be downloaded for offline
use. Please make sure you are not using any APIs that prevent launching and running properly when offline using file://
URL., and test that offline operation works properly for your simulation.

## Published Versions

Here is a link to some published sims, so that you can see a demonstration of how some things should look and behave:
https://phet.colorado.edu/en/simulations/category/html

## Development Process and Checklist

The steps to create a fully functional PhET simulation, given an existing Java/Flash version or development
specification:

1. The simulation and its code:
   a. must use the appropriate libraries in the correct fashion b. must be adequately commented c. must contain no dead
   code (i.e. commented out code that does nothing)
   d. must be maintainable e. reusable components should be polished and moved to the appropriate libraries f. should
   pass all jshint tests when running chipper, and should be compiled into a single file HTML file h. original vector
   artwork for anything appearing in the images/ directory should be checked into the assets/ directory. i. must run
   with ?ea (assertions) enabled without any assertion errors being triggered
2. Simulation & User Interface Testing a. Testing on our supported platforms and identification of problems on different
   browsers b. Performance must be sufficiently fast on all supported platforms. i. The simulation should start in <8
   seconds on iPad3 ii. We strive for a steady 60fps on iPad3 when possible c. The simulation should be tested with
   assertions enabled: `?ea`
   d. The simulation should be tested for touch areas: `?showPointerAreas`
3. Code review a. The code will be reviewed by one or more PhET developers in order to identify possible bugs or
   maintenance problems b. Issues raised in the review will be addressed
4. Release candidate testing a. Before publication, a release candidate branch is created so that the branch can be
   thoroughly tested and, if no significant bugs are found, published
5. Publication a. The simulation is made available on the PhET website
6. Maintenance a. the simulation is published and any bugs reported by students or teachers will be resolved

## Utilities and Instrumentation for Development and Testing

Many aspects of a simulation must be developed properly and working well in order for the simulation to behave properly
across our many supported platforms. PhET has developed several utilities and instruments to make this development and
testing easier. The most up-to-date documentation for the query parameters is available here:
https://github.com/phetsims/chipper/blob/master/js/initialize-globals.js

1. Query parameter: `?screenIndex`. This query parameter may be used to specify the initial screen of the simulation. It
   can be paired with standalone above to launch just a specific screen of the simulation. For instance:
   http://localhost:8080/energy-skate-park-basics/energy-skate-park-basics_en.html?screenIndex=1&standalone launches
   Energy Skate Park: Basics using only the 2nd screen.
2. Phet Allocations: Object instance allocation tracking, so we can cut down on garbage collection.
   See https://github.com/phetsims/phet-core/blob/master/js/phetAllocation.js
   Sample usage:
   a. Run the sim and set up the scenario that you wish to profile b. In the JS console, type: window.alloc={} c. Wait
   until you have taken enough data d. Type x = window.alloc; delete window.alloc; Now you can inspect the x variable
   which contains the allocation information.
3. Run with query parameter `?ea` to enable assertions in the code. The sim should run without any assertion errors. (
   Assertions are predicates about what should be true at specific points in the code. They are used to identify
   programming errors.)
4. Query parameter: `?showPointerAreas`. This query parameter shows the areas for mouse and touch input events. On
   mobile devices (and sometimes for mouse) it is essential to increase the interaction region for a scenery node. Touch
   areas are shown in red and custom mouse areas are shown in blue.
5. makeRandomSlowness(). This method can be called after the simulation is started to simulate an intermittently slow
   system. This can be used to help replicate bugs that only happen intermittently or only on slow platforms. To call
   this method, launch the sim, show the developer console, and type the command as above.
6. makeEverythingSlow(). This method can be called after the simulation is started to simulate a slow system. This can
   be used to help replicate bugs that only happen intermittently or only on slow platforms. To call this method, launch
   the sim, show the developer console, and type the command as above.
7. Query parameter: `?profiler`. Launching a sim with ?profiler will print out the time to create each screen, and will
   show a histogram which updates every 60 frames depicting how long the frames are taking (in ms). Note: just showing
   the average FPS or ms/frame is not sufficient, since we need to see when garbage collections happen, which are
   typically a spike in a single frame. Hence, the data is shown as a histogram. After the first 30ms slots, there is a
   ++= showing the times of longer frames (in ms)
8. Usage of Unit Tests: After making changes in one of the repos with unit tests (see if tests/qunit exists), run the
   unit tests afterwards (tests/qunit/unit-tests.html) to see if anything is broken. We highly recommend checking "Hide
   passed tests", and wait until all tests are complete (it may pause at 0 tests complete at the start).
9. Adding Unit Tests: If you want to add a test, add it to one of the tests/qunit/js/* files that have a QUnit module( '
   ...' ) declaration, and read the QUnit tutorials to understand how it works. You can add new files with more tests by
   creating the file and referencing it in tests/qunit/js/unit-tests.js (whose purpose is to load those files).
10. Namespaces for Unit Tests and Playground: Each unit-tests.html makes certain namespaces global (e.g. Scenery's makes
    window.scenery/kite/dot/axon/core for Scenery/Kite/Dot/Axon/phet-core respectively).
11. Playground: If it exists, it will be a tests/playground.html, and allows testing code in the console. To make code
    available in the console, check the 'main' file used by the playground and add a reference there. For instance,
    Scenery's playground.html loads 'scenery/js/main.js', and saves it to window.scenery.
12. Run `grunt lint` on the command line to check for lint errors. All code should be free of lint errors. (lint is a
    tool that analyzes source code to flag programming errors, bugs, stylistic errors, and suspicious constructs. PhET
    uses the eslint variant of lint.)
13. Install PhET's git hooks to run basic checks as part of the git lifecycle. Run this from the root of your
    checkout. First it clears any pre-existing commit hooks, then installs the new hooks.

```
perennial/bin/for-each.sh perennial/data/active-repos "rm .git/hooks/pre-commit; git init --template=../phet-info/git-template-dir"
```

Getting to optimal performance on all supported platforms can be tricky--this section enumerates possible optimizations
strategies:

1. Consider using WebGL.
2. Reduce allocations (including but not limited to closures) during animation.
3. Eliminate closures and move values to properties and prototypes, see https://github.com/phetsims/scenery/issues/664.
4. Consider replacing color strings with color constants, see https://github.com/phetsims/sun/issues/312.

## Working with GitHub Issues

When the problem described in a GitHub issue is solved, a description of the solution should be made in the issue and
the issue should be reassigned to the original reporter of the GitHub issue for verification and closing. Commits that
address the GitHub issue should also reference the issue in the commit message, so the change set can be easily
reviewed.

Here are some example issues that show creation of an issue, solving it with a commit message that references the issue,
an explanation of the solution and reassignment to the reporter for verification and closing:
https://github.com/phetsims/color-vision/issues/15
https://github.com/phetsims/fraction-matcher/issues/56
https://github.com/phetsims/color-vision/issues/37

## Embedding a Simulation in Your Website

To embed a simulation in your website, use an iframe like so:

<iframe src="https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_en.html" width="834" height="504"></iframe>

The aspect ratio 834x504 is used for new simulations, because it matches the aspect ratio available on popular devices.

To see a full embedding example in context, view the source for this page:
https://phet-dev.colorado.edu/html/acid-base-solutions/1.1.0/acid-base-solutions_en-iframe.html
