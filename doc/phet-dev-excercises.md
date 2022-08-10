# PhET Dev Excercises

Here you will find a list of coding excercises, they are designed for you to get the hang of PhET Sim Development alongside your mentor. Please, start by creating an issue on [Example Sim](https://github.com/phetsims/example-sim) with the title *"Coding Challenges Solution: \<Your name + favourite emoji\>"*, the idea is to report on that issue with your solutions to every challenge. Additionally, you should create a new branch of example-sim while you work on the excercises.

This is meant to be a fun learning experience, so do enjoy!

### 1. Add a second magnet to example sim
Look at the way the first magnet was created in the simulation, how should you go about at displaying a second one that shares the same logic? You'll find yourself instancing multiple objects of the same class a lot in PhET sims. Remember to read through [The Model-View coding pattern](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#model-view-controller-mvc).

<details><summary>Hint</summary>Look into `MagnetsScreenView.js` to see how the magnet is added to the screen, there'll be a model field for the magnet, so you'll have to work your way around that in `MagnetsModel.js`...</details>

### 2. Add a ball
Create a Ball class in the model, then create the corresponding BallNode class in the view, it should extend `ShadedSphereNode`. Display the ball in the simulation and make the BallNode draggable. This time, you will have to create new files for this object, in the model and in the view. When developing sims, you will do this for almost every new class of object there is on screen.

<details><summary>Hint</summary>You can make the contents of `Ball.js` (The model) very similar to `BarMagnet.js`. As for the Node, read through the constructor documentation of `ShadedSphereNode.js` to know what to add to the `super()` call.</details>

### 3. Add a checkbox that controls the Ball's visibility
Most PhET Simulations have checkboxes that control boolean aspects of the sim. Have you read about [phetmarks](https://github.com/phetsims/phet-info/blob/master/doc/new-dev-onboarding.md#phetmarks) yet? Use it to access the Sun example to see how checkboxes are implemented, remember you can use `Ctrl + Shift + H` to get details as to how components are used.

<details><summary>Hint</summary>Look into MagnetsControlPanel in example Sim, that's where you have to add the Checkbox. Also, checkboxes get a Property as their first parameter, so you should probably give it the visibilityProperty of Ball.</details>

### 4. Add a HSlider to control the ball’s diameter
Once again, you should look at Sun's implementation of Sliders and pass in the Ball's diameter or radius property. Remember to link the BallNode to changes of that property, otherwise, the shown ball will not update.


### 5. Options
Add an option to the ball constructor to control its color. Read through the [Javascript Options](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#options-and-config-javascript) design pattern, if you're using JS. Keep in mind that the options pattern is a little bit different to [the one used in TypeScript](https://github.com/phetsims/phet-info/blob/master/doc/phet-software-design-patterns.md#options-typescript) (and in most of PhET Codebase for that matter). You can look into ShadedSphereNodeOptions to know what you can play with. 

### 6. Layout
Organize the checkbox and the slider in their own control panel to the lower left of the screen. Look into implementation of Panel in other PhET sims.
