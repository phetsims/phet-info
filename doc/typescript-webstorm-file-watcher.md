## Configuring WebStorm/IDEA File Watchers for TypeScript Transpilation

The best supported way to transpile code is by using chipper's `node js/scripts/transpile.js --watch`. However, for
developers that want IDE integration way want to experiment with WebStorm/IDEA File Watchers. This process is not
well-vetted and should be used at your own risk.

I experimented with a configuration like so:

![image](https://user-images.githubusercontent.com/679486/143963489-ab2c1ae7-86b2-4bbf-bc29-d54cbf144353.png)

And I observed that it quickly transpiles a single file when saved. It seems to be working nicely and could be a good
solution for those who don't want to run a watch process. You can also see an indicator in the bottom bar of WebStorm
that shows when compilation starts and ends. It's pretty speedy.

My main concern about using File Watcher is my uncertainty about what's best for "Scope"--when I tried "all files"
changes to Sim.js seemed to trigger on sim mains as well (even when unchanged). Could setting scope to "all changed
files" sometimes do more or less than it should?

Also, keep in mind you need to watch both *.js and *.ts files. I'm not sure if those can be combined into one watcher or
if they have to be 2 separate watchers.

Also, should "auto save edited files to trigger the watcher" be checked? Probably.