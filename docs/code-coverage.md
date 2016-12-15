
# Code Coverage

Code coverage generation can currently be used with anything built with chipper's ```grunt```. The code coverage is currently added into the require.js-processed code, so it will not be added to preloads (which is generally desired). We use [Istanbul](https://github.com/gotwarlost/istanbul) as the third-party library that handles the actual instrumentation and report generation.

First, ```grunt``` needs to be run with a flag that 'instruments' the code. This adds lines into the code that records what is executed, and significantly increases the size of the code.

Then, the code should be run to collect statistics. This can be running a sim/runnable (with or without a fuzzer), running unit tests, playing back recorded sessions, etc.

Then we use Istanbul to generate the reports in a form that can be viewed. 

# Generating Coverage Reports

1. Build with instrumentation added (preferably without minification): ```grunt --uglify=false --instrument=true```. We prevent uglification so that it isn't minified and branches aren't removed from the code.
2. Run the instrumented version from the build directory (however it is run)
3. When done, in the JS console, ```copy( __coverage__ )``` to copy JSON coverage information into your clipboard. The code coverage information is recorded in that global variable.
4. Paste it into build/instrumentation/coverage.json. In the future, multiple coverage.json files could be used.
5. Run coverage generation: ```grunt generate-coverage```
6. Browse coverage at build/coverage-report/lcov-report/ (has an index.html). In the future, other report styles could be generated (Istanbul has many options)
