**To begin a code review:**
* Copy this checklist to a GitHub issue titled "Code Review" and labeled `dev:code-review`. 
* Delete the **Table of Contents** section, since the links will be incorrect.
* Delete items and sections that are not relevant.
* Replace {{GITHUB_ISSUE_LINK}} with links to GitHub issues.
* Fill in (or delete) the **Specific Instructions** section.

---

# PhET Code-Review Checklist (a.k.a "CRC")

* The responsible dev is responsible for removing the irrelevant parts
* A checked-off item doesn't mean "no problem here", it means "it was reviewed"
* Problems can be noted in side issues that reference this issue, or through `// REVIEW` comments in the code

## Table of Contents
* [Build and Run Check](https://github.com/phetsims/phet-info/blob/master/checklists/code-review-checklist.md#build-and-run-checks)
* [Memory Leaks](https://github.com/phetsims/phet-info/blob/master/checklists/code-review-checklist.md#memory-leaks)
* [Performance](https://github.com/phetsims/phet-info/blob/master/checklists/code-review-checklist.md#performance)
* [Usability](https://github.com/phetsims/phet-info/blob/master/checklists/code-review-checklist.md#usability)
* [Internationalization](https://github.com/phetsims/phet-info/blob/master/checklists/code-review-checklist.md#internationalization)
* [Repository Structure](https://github.com/phetsims/phet-info/blob/master/checklists/code-review-checklist.md#repository-structure)
* [Coding Conventions](https://github.com/phetsims/phet-info/blob/master/checklists/code-review-checklist.md#coding-conventions)
* [Math Libraries](https://github.com/phetsims/phet-info/blob/master/checklists/code-review-checklist.md#math-libraries)
* [IE11](https://github.com/phetsims/phet-info/blob/master/checklists/code-review-checklist.md#ie11)
* [Organization, Readability, and Maintainability](https://github.com/phetsims/phet-info/blob/master/checklists/code-review-checklist.md#organization-readability-and-maintainability)
* [PhET-iO](https://github.com/phetsims/phet-info/blob/master/checklists/code-review-checklist.md#phet-io)

## Specific Instructions

_Provide specific instructions here. For example: known problems that will fail CRC items, files that can be skipped, code that is not completed, shared or common code that also needs to be reviewed,...  If there are no specific instructions, then delete this section._

## GitHub Issues

The following standard GitHub issues should exist. _If these issues are missing, or have not been completed, pause code review until the issues have been created and addressed by the responsible dev._

- [ ] model.md, see {{GITHUB_ISSUE_LINK}}. Familiarize yourself with the model by reading model.md. Does it adequately describe the model, in terms appropriate for teachers? Has it been reviewed by the sim designer?
- [ ] implementation-notes.md, see {{GITHUB_ISSUE_LINK}}. Familiarize yourself with the implementation by reading implementation-notes.md. Does it provide an overview that will be useful to future maintainers?
- [ ] results of memory testing for `brands=phet`, see {{GITHUB_ISSUE_LINK}}
- [ ] results of memory testing for `brands=phet-io` (if the sim is instrumented for PhET-iO), see {{GITHUB_ISSUE_LINK}}
- [ ] performance testing and sign-off, see {{GITHUB_ISSUE_LINK}}
- [ ] review of pointer areas, see {{GITHUB_ISSUE_LINK}}
- [ ] credits (will not be completed until after RC testing), see {{GITHUB_ISSUE_LINK}}
  
## **Build and Run Checks**

If any of these items fail, pause code review.

- [ ] Does the sim build without warnings or errors?
- [ ] Does the html file size seem reasonable, compared to other similar sims?
- [ ] Does the sim start up? (unbuilt and built versions)
- [ ] Does the sim experience any assertion failures? (run with query parameter `ea`)
- [ ] Does the sim pass a scenery fuzz test? (run with query parameters `fuzz&ea`)
- [ ] Does the sim behave correctly when listener order is shuffled? (run with query parameters `ea&listenerOrder=random` and `ea&listenerOrder=random&fuzz`)
- [ ] Does the sim output any deprecation warnings?  Run with `?deprecationWarnings`. Do not use deprecated methods in new code.

## **Memory Leaks**

- [ ] Does a heap comparison using Chrome Developer Tools indicate a memory leak? (This process is described [here](https://github.com/phetsims/QA/blob/master/documentation/qa-book.md#47-memory-leak-testing).) Test on a version built using `grunt --minify.mangle=false`. Compare to testing results done by the responsible developer. Results can be found in {{GITHUB_ISSUE_LINK}}.
- [ ] For each common-code component (sun, scenery-phet, vegas, …) that opaquely registers observers or listeners, is
there a call to that component’s `dispose` function, or is it obvious why it isn't necessary, or is there documentation
about why `dispose` isn't called?  An example of why no call to `dispose` is needed is if the component is used in
a `ScreenView` that would never be removed from the scene graph. Note that it's also acceptable (and encouraged!) to describe what needs to be disposed in implementation-notes.md. 
- [ ] Are there leaks due to registering observers or listeners? The following guidelines should be followed unless documentation (in-line or in implementation-notes.md) describes why following them is not necessary.
  * AXON: `Property.link` or `lazyLink` is accompanied by `unlink`.
  * AXON: `Multilink.multilink` is accompanied by `unmultilink`.
  * AXON: Creation of `Multilink` is accompanied by `dispose`.
  * AXON: Creation of `DerivedProperty` is accompanied by `dispose`.
  * AXON: `Emitter.addListener` is accompanied by `removeListener`.
  * AXON: `ObservableArrayDef.element*Emitter.addListener` is accompanied by `ObservableArrayDef.element*Emitter.removeListener`
  * SCENERY: `Node.addInputListener` is accompanied by `removeInputListener`
  * TANDEM: Creation of an instrumented `PhetioObject` is accompanied by `dispose`.
- [ ] Do all types that require a `dispose` function have one? This should expose a public `dispose` function that calls `this.disposeMyType()`, where `disposeMyType` is a private function declared in the constructor.  `MyType` should exactly match the filename.

## **Performance**

- [ ] Play with sim, identify any obvious performance issues. Examples: animation that slows down with large numbers of objects; animation that pauses or "hitches" during garbage collection.
- [ ] If the sim uses WebGL, does it have a fallback? Does the fallback perform reasonably well? (run with query parameter `webgl=false`)

## **Usability**

- [ ] Are UI components sufficiently responsive? (especially continuous UI components, such as sliders)
- [ ] Are pointer areas optimized, especially for touch? (run with query parameter `showPointerAreas`)
- [ ] Do pointer areas overlap? (run with query parameter `showPointerAreas`) Overlap may be OK in some cases, depending on the z-ordering (if the front-most object is supposed to occlude pointer areas) and whether objects can be moved.

## **Internationalization**
- [ ] Are there any strings that are not internationalized, and does the sim layout gracefully handle internationalized strings that are shorter than the English strings? (run with query parameter `stringTest=X`. You should see nothing but 'X' strings.)
- [ ] Does the sim layout gracefully handle internationalized strings that are longer than the English strings? (run with query parameters `stringTest=double` and `stringTest=long`)
- [ ] Does the sim stay on the sim page (doesn't redirect to an external page) when running with the query parameter
`stringTest=xss`? This test passes if sim does not redirect, OK if sim crashes or fails to fully start. Only test on one
desktop platform.  For PhET-iO sims, additionally test `?stringTest=xss` in Studio to make sure i18n strings didn't leak
to phetioDocumentation, see https://github.com/phetsims/phet-io/issues/1377
- [ ] Avoid using concatenation to create strings that will be visible in the user interface. Use `StringUtils.fillIn` and a string pattern to ensure that strings are properly localized.
- [ ] Use named placeholders (e.g. `"{{value}} {{units}}"`) instead of numbered placeholders (e.g. `"{0} {1}"`).
- [ ] Make sure the string keys are all perfect, because they are difficult to change after 1.0.0 is published. Guidelines for string keys are:

  (1) Strings keys should generally match their values. E.g.:

  ```js
  "helloWorld": {
    value: "Hello World!"
  },
  "quadraticTerms": {
    value: "Quadratic Terms"
  }
  ```

  (2) If a string key would be exceptionally long, use a key name that is an abbreviated form of the string value, or that captures the purpose/essence of the value. E.g.:

  ```js
  // key is abbreviated
  "iWentToTheStore": {
    value: "I went to the store to get milk, eggs, butter, and sugar."
  },

  // key is based on purpose
  "describeTheScreen": {
    value: "The Play Area is a small room. The Control Panel has buttons, a checkbox, and radio buttons to change conditions in the room."
  }
  ```
  (3) If string key names would collide, use your judgment to disambiguate. E.g.:

  ```js
  "simplifyTitle": {
     value: "Simplify!"
  },
  "simplifyCheckbox": {
     value: "simplify"
  }
  ```

  (4) String keys for screen names should have the general form `"screen.{{screenName}}"`. E.g.:

  ```js
    "screen.explore": {
      "value": "Explore"
    },
  ```

  (5) String patterns that contain placeholders (e.g. `"My name is {{first}} {{last}}"`) should use keys that are unlikely to conflict with strings that might be needed in the future.  For example, for `"{{price}}"` consider using key `"pricePattern"` instead of `"price"`, if you think there might be a future need for a `"price"` string.
  (6) It is acceptable to prefix families of strings with a prefix, like so:

```json
  "material.water": {
    "value": "Water"
  },
  "material.wood": {
    "value": "Wood"
  },
  "shape.block": {
    "value": "Block"
  },
  "shape.cone": {
    "value": "Cone"
  },
```

Nested substructure is not yet fully supported.

- [ ] If the sim was already released, make sure none of the original string keys have changed. If they have changed, make sure any changes have a good reason and have been discussed with @jbphet (it is likely that an issue like https://github.com/phetsims/gravity-force-lab/issues/166 should be created).

## **Repository Structure**

- [ ] The repository name should correspond to the sim title. For example, if the sim title is "Wave Interference", then the repository name should be "wave-interference".
- [ ] Are all required files and directories present?
For a sim repository named “my-repo”, the general structure should look like this (where assets/, images/, mipmaps/ or sounds/ may be omitted if the sim doesn’t have those types of resource files).

  ```
  my-repo/
    assets/
    doc/
      images/
        *see annotation
      model.md
      implementation-notes.md
    images/
      license.json
    js/
      (see section below)
    mipmaps/
      license.json
    sound/
      license.json
    dependencies.json
    .gitignore
    my-repo_en.html
    my-repo-strings_en.json
    Gruntfile.js
    LICENSE
    package.json
    README.md
  ```
  *Any images used in model.md or implementation-notes.md should be added here. Images specific to aiding with documentation do not need their own license.

- [ ] Verify that the same image file is not present in both images/ and mipmaps/. If you need a mipmap, use it for all occurrences of the image.

- [ ] Is the js/ directory properly structured?
  All JavaScript source should be in the js/ directory. There should be a subdirectory for each screen (this also applies for single-screen sims, where the subdirectory matches the repo name).  For a multi-screen sim, code shared by 2 or more screens should be in a js/common/ subdirectory. Model and view code should be in model/ and view/ subdirectories for each screen and common/.  For example, for a sim with screens “Introduction” and “Lab”, the general directory structure should look like this:

  ```
  my-repo/
    js/
    common/
      model/
      view/
    introduction/
      model/
      view/
    lab/
      model/
      view/
    my-repo-main.js
    myRepo.js
    myRepoStrings.js
  ```

- [ ] Do filenames use an appropriate prefix? Some filenames may be prefixed with the repository name,
  e.g. `MolarityConstants.js` in molarity. If the repository name is long, the developer may choose to abbreviate the
  repository name, e.g. `EEConstants.js` in expression-exchange. If the abbreviation is already used by another
  repository, then the full name must be used. For example, if the "EE" abbreviation is already used by
  expression-exchange, then it should not be used in equality-explorer. Whichever convention is used, it should be used
  consistently within a repository - don't mix abbreviations and full names.
- [ ] Is there a file in assets/ for every resource file in sound/ and images/? Note that there is *not necessarily* a
  1:1 correspondence between asset and resource files; for example, several related images may be in the same .ai file.
  Check license.json for possible documentation of why some resources might not have a corresponding asset file.
- [ ] For simulations, was the README.md generated by `grunt published-README` or `grunt unpublished-README`? Common
  code repos can have custom README files.
- [ ] Does package.json refer to any dependencies that are not used by the sim?
- [ ] Is the LICENSE file correct? (Generally GPL v3 for sims and MIT for common code,
  see [this thread](https://github.com/phetsims/tasks/issues/875#issuecomment-312168646) for additional information).
- [ ] Does .gitignore match the one in simula-rasa?
- [ ] In GitHub, verify that all non-release branches have an associated issue that describes their purpose.
- [ ] Are there any GitHub branches that are no longer needed and should be deleted?
- [ ] Sim-specific query parameters (if any) should be identified and documented in one .js file in js/common/ or js/ (
  if there is no common/). The .js file should be named `{{PREFIX}}QueryParameters.js`, for example
  ArithmeticQueryParameters.js for the arithmetic repository, or FBQueryParameters.js for Function Builder (where
  the `FB` prefix is used).
- [ ] Query parameters that are public-facing should be identified using `public: true` in the schema.
- [ ] All sims should use a color file named `MyRepoColors.js` or, if using abbreviations, `MRColors.js`, and
  use `ProfileColorProperty` where appropriate, even if they have a single (default) profile (to support color editing
  and PhET-iO Studio). The `ColorProfile` pattern was converted to `*Colors.js` files in 
  https://github.com/phetsims/scenery-phet/issues/515. Please see 
  [GasPropertiesColors.js](https://github.com/phetsims/gas-properties/blob/master/js/common/GasPropertiesColors.js)
  for a good example.

## **Coding Conventions**

- [ ] Are coding conventions outlined in [PhET's Coding Conventions Document](https://github.com/phetsims/phet-info/blob/master/doc/coding-conventions.md) followed and adhered to? This document 
deals with PhET coding conventions. You do not need to exhaustively check every item in this section, nor do you 
necessarily need to check these items one at a time. The goal is to determine whether the code generally meets PhET standards.

## **TypeScript Conventions**

- [ ] Are TypeScript conventions outlined in the [TypeScript Conventions Document](https://github.com/phetsims/phet-info/blob/master/doc/typescript-conventions.md) followed and adhered to?

## **Math Libraries**

- [ ] `DOT/Utils.toFixed` or `DOT/Utils.toFixedNumber` should be used instead of `toFixed`. JavaScript's `toFixed` is notoriously buggy. Behavior differs depending on browser, because the spec doesn't specify whether to round or floor.

## IE11
- [ ] IE is no longer supported. With that in mind remove IE-specific workarounds
- [ ] Use `string.includes` and `string.startsWith` where possible.

## **Organization, Readability, and Maintainability**

- [ ] Does the organization and structure of the code make sense? Do the model and view contain types that you would expect (or guess!) by looking at the sim? Do the names of things correspond to the names that you see in the user interface?
- [ ] Are appropriate design patterns used? See [phet-software-design-patterns.md](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md).  If new or inappropriate patterns are identified, create an issue.
- [ ] Is inheritance used where appropriate? Does the type hierarchy make sense?
- [ ] Is composition favored over inheritance where appropriate? See https://en.wikipedia.org/wiki/Composition_over_inheritance.
- [ ] Is there any unnecessary coupling? (e.g., by passing large objects to constructors, or exposing unnecessary properties/functions). In TypeScript, you can decouple by narrowing the API like so: 
```ts
  public constructor( tickMarksVisibleProperty: Property<boolean>,
                      model: Pick<IntroModel, 'changeWaterLevel'>, // <-- Note the call site can pass the whole model, but we declare we will only use this part of it
                      waterCup: WaterCup, modelViewTransform: ModelViewTransform2,
                      providedOptions?: WaterCup3DNodeOptions ) {
```
- [ ] Is there too much unnecessary decoupling? (e.g. by passing all of the properties of an object independently instead of passing the object itself)?
- [ ] Are the source files reasonable in size? Scrutinize large files with too many responsibilities - can responsibilities be broken into smaller delegates? To see file sizes for TypeScript sims, run this shell command:
```
cd {{repo}}/js ; wc -l `find . -name "*.ts" -print` | sort
```
- [ ] Are any significant chunks of code duplicated? In addition to manual identification, tools include: WebStorm _Code > Analyze Code > Locate Duplicates_ and https://github.com/danielstjules/jsinspect.
- [ ] Is there anything that should be generalized and migrated to common code?
- [ ] Are there any `TODO` or `FIXME` or `REVIEW` comments in the code?  They should be addressed or promoted to GitHub issues.
- [ ] Are there any [magic numbers](https://en.wikipedia.org/wiki/Magic_number_(programming)) that should be factored out as constants and documented?
- [ ] Are there any constants that are duplicated in multiple files that should be factored out into a `{{REPO}}Constants.js` file?
- [ ] Does the implementation rely on any specific constant values that are likely to change in the future? Identify constants that might be changed in the future. (Use your judgement about which constants are likely candidates.) Does changing the values of these constants break the sim? For example, see https://github.com/phetsims/plinko-probability/issues/84.
- [ ] Is [PhetColorScheme](https://github.com/phetsims/scenery-phet/blob/master/js/PhetColorScheme.ts) used where appropriate? Verify that the sim is not inventing/creating its own colors for things that have been standardized in `PhetColorScheme`.  Identify any colors that might be worth adding to `PhetColorScheme`.
- [ ] Are all dependent Properties modeled as `DerivedProperty` instead of `Property`?
- [ ] All dynamics should be called from Sim.step(dt), do not use window.setTimeout or window.setInterval.  This will help support Legends of Learning and PhET-iO.

## **Accessibility**

This section may be omitted if the sim has not been instrumented with accessibility features. Accessibility includes
various features, not all are always include. Ignore sections that do not apply.

### General
- [ ] Are accessibility features integrated well into the code. They should be added in a maintainable way, even if that requires upfront refactoring.

### Alternative Input
- [ ] Does the sim pass an accessibility fuzz test? (run with query parameters `fuzzBoard&ea`)
- [ ] Does this sim use specific keyboard shortcuts that overlap with global shortcuts? This includes the use of modifier keys like in https://github.com/phetsims/ratio-and-proportion/issues/287. **NOTE: There is currently no list of global shortcuts, and therefore no way to complete this checklist item. See https://github.com/phetsims/phet-info/issues/188.**

### Interactive Description
- [ ] Run the entire built sim HTML file through an [HTML validator](https://validator.w3.org/nu/#textarea), does the HTML pass?
- [ ] If applicable, are good design patterns used for interactive description, see [interactive-description-technical-guide.md](https://github.com/phetsims/phet-info/blob/master/doc/interactive-description-technical-guide.md)
- [ ] Does resetting the simulation also reset the entire PDOM?
- [ ] Is `Node.pdomOrder` used appropriately to maintain visual and PDOM layout balance?
- [ ] Make sure accessibility strings aren't being adjusted with ascii specific javascript methods like `toUpperCase()`. Remember that one day these strings will be translatable
- [ ] Make sure for accessibility strings that all end of sentence periods do not have a leading space before it. Some screen readers will read these as "dot." This can occur often when a clause is conditionally added.

## **PhET-iO**

This section may be omitted if the sim has not been instrumented for PhET-iO, but is likely good to glance at no matter.

- [ ] Does instrumentation follow the conventions described in [PhET-iO Instrumentation Guide](https://github.com/phetsims/phet-io/blob/master/doc/phet-io-instrumentation-technical-guide.md)?
This could be an extensive bullet. At the very least, be sure to know what amount of instrumentation this sim
 supports. Describing this further goes beyond the scope of this document.
- [ ] PhET-iO instantiates different objects and wires up listeners that are not present in the PhET-branded simulation.
  It needs to be tested separately for memory leaks.  To help isolate the nature of the memory leak, this test should
  be run separately from the PhET brand memory leak test.  Test with a colorized Data Stream, and Studio (easily
  accessed from phetmarks). Compare to testing results done by the responsible developer and previous releases.
- [ ] Make sure unused `PhetioObject` instances are disposed, which unregisters their tandems.
- [ ] Make sure JOIST `dt` values are used instead of `Date.now()` or other Date functions. Perhaps try
`phet.joist.elapsedTime`. Though this has already been mentioned, it is necessary for reproducible playback via input
events and deserves a comment in this PhET-iO section.
- [ ] Are random numbers using `DOT/dotRandom` as an imported module (not a global), and all doing so after modules are declared (non-statically)?  For
example, the following methods (and perhaps others) should not be used: `Math.random`, `_.shuffle`, `_.sample`, `_.random`.
This also deserves re-iteration due to its effect on record/playback for PhET-iO.
- [ ] Like JSON, keys for `undefined` values are omitted when serializing objects across frames. Consider this when
determining whether `toStateObject` should use `null` or `undefined` values.
- [ ] PhET prefers to use the term "position" to refer to the physical (x,y) position of objects.  This applies to both
brands, but is more important for the PhET-iO API.  See https://github.com/phetsims/phet-info/issues/126
- [ ] Are your IOType state methods violating the API of the core type by accessing private fields?
- [ ] When defining a boolean Property to indicate whether something is enabled, use `AXON/EnabledProperty`.  This 
should be done in both the model and the view. If you're using a DerivedProperty, skip this item.
- [ ] Do not use translated strings in `phetioDocumentaton` - it changes the PhET-iO API!
