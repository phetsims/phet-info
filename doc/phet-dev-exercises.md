# 💪 PhET Dev Exercises

Here you will find a list of coding exercises that are designed to provide insight into the fundamentals of PhET Sim
Development. If you ever get stuck or have questions reach out to your mentor for guidance. Please start by creating an
issue on [Example Sim](https://github.com/phetsims/example-sim) with the title *"Dev Exercises Solution: \<Your name +
favourite emoji\>"*. Use this issue to track your progress and solutions to every challenge. Additionally, you should
create a new branch of example-sim while you work on the exercises. This branch should be named: *"
dev-exercises-{{username}}"*.

This is meant to be a fun learning experience, so do enjoy!

### 1. Add a second magnet to example sim 🧲

Look at the way the first magnet was created in the simulation. How should you go about displaying a second one that
shares the same logic? You will frequently find yourself instantiating multiple objects of the same class in PhET sims.
Keeping the code organized, and minimizing repetition is something to consider. Remember to read
through [The Model-View coding pattern](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#model-view-controller-mvc)
.

<details><summary>Hint</summary>Look into `MagnetsScreenView.js` to see how the magnet is added to the screen. There will be a model field for the magnet, so you'll have to work your way around that in `MagnetsModel.js`...</details>

### 2. Add a ball ⚽️

Create a Ball class in the model, then create the corresponding BallNode class in the view ( it should
extend `ShadedSphereNode` ). Display the ball in the simulation and make the BallNode draggable. This time, you will
have to create new files for the object, in both the model and the view directories. When developing sims, you will do
this for almost every new class of an object there is on the screen.

<details><summary>Hint</summary>You can make the contents of `Ball.js` (The model) very similar to `BarMagnet.js`. As for the Node, read through the constructor documentation of `ShadedSphereNode.js` to know what to add to the `super()` call.</details>

### 3. Add a checkbox that controls the Ball's visibility ☑️

Most PhET Simulations have checkboxes that control boolean aspects of the sim. Have you read
about [phetmarks](https://github.com/phetsims/phet-info/blob/master/doc/new-dev-onboarding.md#phetmarks) yet? Use it to
access the Sun example to see how checkboxes are implemented, remember you can use `Ctrl + Shift + H` to get details as
to how components are used.

<details><summary>Hint</summary>Look into `MagnetsControlPanel` in example-sim, that's where you have to add the Checkbox. Also, checkboxes get a Property as their first parameter, so you should probably give it the `visibleProperty` of Ball.</details>

### 4. Add a HSlider to control the ball’s diameter 🎚

Sliders are frequently used as a way for users to interact with the components, physics, or data on the screen. Once
again, you should refer to Sun's implementation of Sliders as a starting point to control your ball's diameter.

<details><summary>Hint</summary>Try passing in the BallNode's radius or diameter properties to the slider, and don't forget to use `link` to ensure these changes are being communicated between the components.</details>

### 5. Options 🎨

Add an option to the ball constructor to control its color. Read through
the [Javascript Options](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#options-and-config-javascript)
design pattern, if you're using JS. Keep in mind that the Javascript options pattern is different
than [the TypeScript options pattern](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#options-typescript)
.

<details><summary>Hint</summary> You can look into `ShadedSphereNodeOptions` to know what options you can play with.</details>

### 6. Layout 🖼

Proper layout is a big part of ensuring users have the best experience possible when interacting with PhET sims.
Organize the checkbox and slider in their own control panel to the lower left of the screen. Look into the
implementation of control panels in other PhET sims. You might find a variety of ways this is done and all of them are
right! Be inspired to take from the examples you see, or implement your own approach.

<details><summary>Hint</summary> In PhETmarks, Scenery/layout-documentation is the best place to learn about all the amazing tools that have been built for layout management. Start there to discover what tools you have at your disposal, and narrow down the approach you want to use.</details>

### 7. You did it! 🎉

Great job you got through all the exercises! Give yourself a pat on the back, you just learned a lot. To get feedback on
your solutions, make sure to assign the corresponding issue to your mentor for review. Once you've done that and both
you and your mentor feel satisfied, close the issue and delete the branch. 
