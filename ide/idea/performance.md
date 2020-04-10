
# Optimize Performance for  WebStorm and Intellij IDEA

Jetbrains IDEs are quite "heavy" and have the habit of causing performance troubles on many computers. Here are some 
steps that can be taken to optimize the performance.

* This guide proved helpful for @zepumph, and, though much is boiled into the below comments, it may be helpful for you!
https://dev.to/adammcquiff/improve-the-performance-of-webstorm-and-other-jetbrains-ides-11bc
* Disable any live templates that you aren't using.
* Disable any plugins that you aren't using (most of the bundled ones aren't used by PhET developers).
* Exclude any web browsers that you don't want support for opening HTML (in the top right corner while editing).
* Add this line to `top menu > Help > Edit Custom Properties`: `editor.zero.latency.typing=true`
* Make sure all library files are excluded, like `node_modules`. You may also want to exclude `sherpa/lib` and perhaps 
`babel`. @samreid has this pattern excluded: `Directories > Excluded files: build;node_modules;images;sounds`
* Improving search performance:
  * Make sure that as many folders as possible are excluded (as is reasonable). See above. 
  * Use a scope! In many cases, it is enough to just look in the `js/` folders of repos, so make a scope to look there. The
  pattern looks like `file:*/js//*`.
* Optimizing VM options file:
  * Edit by opening `top menu > Help > Edit Custom VM Options`
  * zepumph's looks like:
    ```
    -Xms1024m
    -Xmx2048m
    -XX:NewRatio=2
    -XX:ReservedCodeCacheSize=512m
    -XX:+UseConcMarkSweepGC
    -ea
    -Dsun.io.useCanonCaches=false
    -Djava.net.preferIPv4Stack=true
    -Djdk.http.auth.tunneling.disabledSchemes=""
    -XX:+HeapDumpOnOutOfMemoryError
    -XX:-OmitStackTraceInFastThrow
    ```
  * the main memory related ones are explained in https://www.jetbrains.com/help/idea/tuning-the-ide.html#common-jvm-options
  * A complete documentation of JVM options can be found in https://docs.oracle.com/javase/8/docs/technotes/tools/windows/java.html
  
## Other Resources

https://stackoverflow.com/questions/29388626/how-to-speed-up-webstorm contains all of the above tips and more, including specifics on which plugins to disable. 
