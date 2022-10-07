# Developer Resources

## Overview
This document contains miscellaneous resources, tips, and tricks that are available to PhET developers.

### Applets, extensions, and other Misc to assist in development
##### On Windows
* Ditto clipboard manager - helpful for keeping complex copy paste operation history

##### Chrome 
* Lightshot (screenshot tool)
* Tenon Check (accessibility auditing)

### Github
Most of these can be found with simple google searches, but it is nice to have a list of resources that have been 
helpful to PhET devs while learning how to superuse Github
* Mastering markdown: https://guides.github.com/features/mastering-markdown/
* Mastering search: https://help.github.com/en/articles/searching-code
* Referencing issues in commit messages can be done in the following ways:
  * If referencing the same repo as the commit, just use a hash: "I did a commit, see #32"
  * You can also use the full URL to the github issue: "The things I did in this commit are good, see https://github.com/phetsims/chipper/issues/32"
  * You can use github shorthand too: "This commit fixes a lot of stuff, see phetsims/chipper#32"

### Debugging iOS devices
##### On Mac
Mac users can use the Safari Web Inspector to debug a sim in mobile Safari. Once you device is connected to your Mac
through USB, you should be able to see your device listed under the "Develop" menu item in the Safari menu bar.
Make sure that "Show Develop in menu bar" is enabled in advanced Safari settings. For more detailed information, see
https://webdesign.tutsplus.com/articles/quick-tip-using-web-inspector-to-debug-mobile-safari--webdesign-8787

##### On Windows
There is nothing native in Windows that lets you debug mobile Apple platforms, but Weinre does a pretty good job. Weinre
is a debugger for web pages, and is designed to work remotely so you can debug mobile devices. It does not support 
`debugger` breakpoints, but it allows you to inspect the DOM, print statements, and inspect the application with
JavaScript. Please see https://people.apache.org/~pmuellr/weinre/docs/latest/Home.html for detailed information on
how to install and run Weinre. The following is a quick list that may help get it up and running faster.

1) Weinre is deployed at https://npmjs.org/package/weinre, and you can install it with
  `sudo npm -g install weinre`
2) To run the debug server, run
  `weinre -httpPort [portNumber] -boundHost -all-`
where [portNumber] is your desired http port number. `-boundHost -all-` is required for remote debugging and tells
Weinre to allow all interfaces on the current machine rather than just localhost.
3) Navigate to http://localhost:[portNumber]/client/#anonymous once the Weinre server is running. This is the Weinre
debugging interface.
4) Add this snippet somewhere in the top level sim HTML file.
  `<script src="http://[portNumber]:/target/target-script-min.js#anonymous"></script>`
  This will inject the Weinre target code into the simulation.
5) Launch the simulation from the mobile device. You should see the sim top level HTML file listed under "Targets" in
the Weinre interface.
6) The interface has a similar look and feel to the Chrome dev tools. Have fun debugging!

You can go to `http://localhost:[portNumber]/` once Weinre server is up and running for additional quick help and
information.

Please beware of the following "Gotchyas" that I have encountered while using Weinre
  * HTML Elements in the "Elements" inspector sometimes never appear, especially those that are added later
  with document.createElement().
  * Sometimes elements in the tree navigation of the "Elements" inspector don't appear when you "open" a new level
  by clicking on the triangle next to a parent element. Opening/closing the level a few times sometimes makes the
  elements appear correctly.
  * When styles are removed from an element with the "Styles" panel on the right of the "Elements" inspector, sometimes
  they are removed for good if you click a checkbox, even if you try to add them back. Reloading is the only solution.

#### Getting crash logs
Crash logs are transferred to iTunes whenever the device is synced to another computer. Just plug in your device and
launch iTunes to complete the sync. The location of the crash logs will depend on whether you are using Mac or Windows.

##### On Mac
Logs are located at `~/Library/Logs/CrashReporter/MobileDevice/`. Open the folder with your device's name. Look for files starting with "Read It LaterPro". If you don't see any, try opening a file called "Retired".

##### On Windows.
Logs are located at `~/AppData/Roaming/Apple Computer/Logs/CrashReporter\MobileDevice`. Open the folder with your device's name.

### Accessibility Resources

* The [Accessibility Developer Guide](https://www.accessibility-developer-guide.com/) is fairly comprehensive.
