# PhET Dev Excercises

Here you will find a list of coding excercises, they are designed for you to get the hang of PhET Sim Development alongside your mentor. Please, start by creating an issue on [Example Sim](https://github.com/phetsims/example-sim) with the title *"Coding Challenges Solution: \<Your name + favourite emoji\>"*, the idea is to report on that issue with your solutions to every challenge. Additionally, you should create a new branch of example-sim while you work on the excercises.

This is meant to be a fun learning experience, so do enjoy!

### 1. Add a second magnet to example sim
Look at the way the first magnet was created in the simulation, how should you go about at displaying a second one that shares the same logic?

<details><summary>Hint</summary>Look into `MagnetsScreenView.js` to see how the magnet is added to the screen, then change some things in `MagnetsModel.js`...</details>

<details><summary>Solution Snippet</summary>
```
// Inside MagnetsModel.js:
// @public {OtherBarMagnet} second bar magnet model element, different position
    this.otherBarMagnet = new BarMagnet( new Dimension2( 250, 50 ), new Vector2( 300, 0 ), 0 );

// Inside MagnetsScreenView.js:
// Add a second magnet. The model determines its position.
    this.addChild( new BarMagnetNode( model.otherBarMagnet, modelViewTransform ) );
```
</details>

### 2. Add a ball
Create a Ball class in the model, then create the corresponding BallNode class in the view. Display the ball in the simulation and make the BallNode draggable.

<details><summary>Hint</summary>You can make `Ball.js` (The model) very similar to `BarMagnet.js`. As for the Node, try to extend `ShadedSphereNode.js`</details>

<details><summary>Solution Snippet</summary>
  Also using much of the BarMagnetNode code for similar logic
```
import ShadedSphereNode from '../../../../scenery-phet/js/ShadedSphereNode.js';

class BallNode extends ShadedSphereNode {

  /**
   * @param {Ball} ball - the model of the ball
   * @param {ModelViewTransform2} modelViewTransform - the transform between model coordinates and view coordinates
   */
  constructor( ball, modelViewTransform ) {
    super( ball.size, {

      // Show a cursor hand over the ball
      cursor: 'pointer'
    } );

    // Scale this Node, so that it matches the model width and height.
    const scaleX = modelViewTransform.modelToViewDeltaX( ball.size ) / this.width;
    this.scale( scaleX, scaleX );

    // Move the magnet by dragging it.
    this.addInputListener( new DragListener( {
      allowTouchSnag: true, // When dragging across it on a touch device, pick it up
      positionProperty: ball.positionProperty,
      transform: modelViewTransform
    } ) );

    // Observe changes in model position, and move this Node to the new position in the view.
    // This Property exists for the lifetime of the simulation, so this listener does not need to be unlinked.
    ball.positionProperty.link( position => {
      this.translation = modelViewTransform.modelToViewPosition( position );
    } );

    // Observe changes in model orientation, and update the orientation in the view.
    // This Property exists for the lifetime of the simulation, so this listener does not need to be unlinked.
    ball.orientationProperty.link( orientation => {
      this.rotation = orientation;
    } );
  }
}
```
</details>

### 3. Adding checkboxes
Look at the Sun example and add a checkbox to control the ball visibility.

<details><summary>Hint</summary>Look into MagnetsControlPanel and add a Checkbox to its contents</details>

### 4. A second ball!
Add a second ball and prevent both of them from overlapping when released from dragging. Either ball can move to avoid overlapping.
### 5. Sliders!
Add a slider to control the balls’ diameters. The overlapping rule should still apply.
### 6. Options
Add an option to the ball constructor to control its color. The two balls should be different colors.
### 7. Layout
Organize the checkbox and the slider in their own control panel to the lower left of the screen.
