# PhET Dev Excercises

Here you will find a list of coding excercises, they are designed for you to get the hang of PhET Sim Development alongside your mentor. Please, start by creating an issue on [Example Sim](https://github.com/phetsims/example-sim) with the title *"Coding Challenges Solution: \<Your name + favourite emoji\>"*, the idea is to report on that issue with your solutions to every challenge. Additionaly, you should fork and clone Example Sim while you solve the challenges.

How to fork and clone:
- Fork example-sim (place fork under your personal github ownership)
- Git clone in phetsims root directory changing the directory name to {{GITHUB}}-example-sim (ex. `git clone git clone https://github.com/marlitas/example-sim.git {{GITHUB}}-example-sim`)
- Launch server ( from phetsims root directory) and transpile as normal
- Visit http://localhost/{{REPO_NAME}}/example-sim_en.html to access forked example-sim. 
- Make sure that any changes and commits for the purpose of the tutorial are being made inside the {{GITHUB}}-example-sim directory. 

This is meant to be a fun exercise and a learning experience, so enjoy!

### 1. Add a second magnet to example sim
Look at the way the first magnet was created in the simulation, how should you go about at displaying a second one that shares the same logic?
### 2. Add a ball
Create a Ball class in the model, then create the corresponding BallNode class in the view. Display the ball in the simulation and make the BallNode draggable.
### 3. Adding checkboxes
Look at the Sun example and add a checkbox to control the ball visibility.
### 4. A second ball!
Add a second ball and prevent both of them from overlapping when released from dragging. Either ball can move to avoid overlapping.
### 5. Sliders!
Add a slider to control the balls’ diameters. The overlapping rule should still apply.
### 6. Options
Add an option to the ball constructor to control its color. The two balls should be different colors.
### 7. Layout
Organize the checkbox and the slider in their own control panel to the lower left of the screen.
