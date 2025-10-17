# Vegas Description - Quickstart Guide

@author Jesse Greenberg

A quick guide for adding Core Description to PhET game screens that use vegas components.

This guide assumes you have already implemented the patterns in
the [Core Description Quickstart Guide](https://github.com/phetsims/phet-info/blob/main/doc/core-description-quickstart-guide.md).
You should be comfortable with `accessibleName`, `accessibleHelpText`, `accessibleParagraph`, `pdomOrder`, and the
strings organization described there. The focus here is on vegas-specific structure, components, and focus management.

## Overall Process

- Disable the default `ScreenView` accessible sections that are tailored to standard sims.
- Build each game phase on the vegas screen node classes (`LevelSelectionScreenNode`, `ChallengeScreenNode`,
  `RewardScreenNode`) to get consistent structure and heading hierarchy.
- Use `pdomOrder` within each vegas screen node to organize headings, controls, and descriptive content exactly as
  specified in the design document.
- Prefer vegas UI components for default accessible names, help text, and context responses.
- Manage focus transitions whenever content hides or changes. Some of this will be automatic in `visibleProperty`
  observers.
- Verify context responses (alerts) for button actions and game outcomes, augmenting the vegas defaults with
  sim-specific behavior.

## Implementation Steps

### 1. Prepare the ScreenView

`ScreenView` includes accessible sections that work for most sims but not for vegas games. Disable them so you can control
the structure with vegas screen nodes.

```ts
const gameScreenView = new ScreenView( {
  includeAccessibleSectionNodes: false
} );
```

From this point forward, one of the vegas screen node classes should own the accessible structure for each game phase.

### 2. Level Selection Screens

Extend `LevelSelectionScreenNode`, or compose with it, for any UI where the player chooses a level or game mode.

- The node supplies headings and sections for "Choose Your Level" and (optionally) "Game Options".
- Set `accessibleIncludeOptionsDescription` if the screen includes game option controls.
- Use `pdomOrder` on the provided section nodes to arrange content as specified by the design document.

```ts
class MyLevelSelectionScreen extends LevelSelectionScreenNode {
  public constructor() {
    const levelButtons = new LevelSelectionButtonGroup();
    super( simScreenNameProperty, levelButtons, {
      accessibleIncludeOptionsDescription: true
    } );

    const infoButton = new GameInfoButton();
    const timerToggleButton = new GameTimerToggleButton();
    const resetAllButton = new ResetAllButton();

    this.accessibleLevelsSectionNode.pdomOrder = [ levelButtons, infoButton ];
    this.accessibleControlsSectionNode.pdomOrder = [ timerToggleButton, resetAllButton ];
  }
}
```

### 3. Challenge Screens

Use `ChallengeScreenNode` for gameplay challenges. It provides headings and sections for the main challenge, answer
controls, and status indicators.

- Pass level/challenge counts so vegas can describe progress.
- Populate each section via `pdomOrder`, keeping interactive elements grouped logically.
  - The game challenge content goes in the `accessibleChallengeSectionNode`.
  - Buttons and controls for submitting answers go in the `accessibleAnswerSectionNode`.
  - Status bars go in the `accessibleStatusSectionNode`.

```ts
class MyChallengeScreen extends ChallengeScreenNode {
  public constructor() {
    super( {
      challengeNumberProperty: challengeNumberProperty,
      challengeCountProperty: challengeCountProperty,
      levelNumberProperty: levelNumberProperty
    } );

    const interactionArea = new GameDiagram();
    const numberControl = new NumberControl();
    const checkAnswerButton = new CheckButton();
    const tryAgainButton = new TryAgainButton();
    const statusBar = new FiniteStatusBar();

    this.accessibleChallengeSectionNode.pdomOrder = [ interactionArea, numberControl ];
    this.accessibleAnswerSectionNode.pdomOrder = [ checkAnswerButton, tryAgainButton ];
    this.accessibleStatusSectionNode.pdomOrder = [ statusBar ];
  }
}
```

If the design calls for an accessible prompt or answer summary, populate `accessibleChallengePrompt` or
`accessibleAnswerSummary` (see options below). If your game challenge does not include one of these sections, you can
make it invisible with the `visible` setter.

### 4. Reward Screens

For end-of-level feedback, use `RewardScreenNode`. It exposes a single section for reward content.

```ts
class MyRewardScreen extends RewardScreenNode {
  public constructor() {
    super();

    const levelCompletedNode = new LevelCompletedNode();
    this.accessibleRewardSectionNode.pdomOrder = [ levelCompletedNode ];
  }
}
```

### 5. Prefer Vegas Components

Vegas buttons and controls include default labels, accessible names, accessible help text, and context responses that
match PhET game design language. Use them whenever the UI design aligns.

- GameInfoButton, GameTimerToggleButton, TryAgainButton, etc.
- Review vegas/js/buttons/ for the full list.

If you need to override defaults, supply string properties through the options, matching the naming conventions from the
core guide.

### 6. Manage Focus Transitions

Screen content in vegas games is dynamic. Ensure focus is never lost during a transition and always moves somewhere
meaningful:

- Set `visibleProperty` on `LevelSelectionScreenNode` and `ChallengeScreenNode` so those screens manage
  focus and default context responses for you when visibility changes.
- When you swap in reward content, set `visibleProperty` on `LevelCompletedNode`
  or use `show()`/`hide()` on `RewardDialog` so focus lands correctly and the built-in responses fire.
- If a button hides itself (e.g., `CheckButton`, `ShowAnswerButton`), move focus explicitly to the next logical
  control (TryAgainButton, NextButton, or ShowAnswerButton). The flow will be outlined in the game design document.
- When the `GameInfoButton` opens a dialog, focus is moved inside the dialog automatically. Make sure closing the dialog
  returns focus to the element that launched it or to a follow-up control if the design specifies one.

### 7. Context Responses and Alerts

Vegas provides standard context responses for common game states. Use them before creating custom strings:

- Example keys: `VegasFluent.checkButton.accessibleContextResponseIncorrect`,
  `VegasFluent.checkButton.accessibleContextResponseCorrectPoints`.
- For unique scenarios, implement additional alerts in your game logic with `addAccessibleContextResponse`.

### 8. Strings and Naming

Continue to store accessibility strings under the `a11y` key in the sim's strings.json. See the core guide for details.

## Vegas Accessibility Options Reference

Refer to vegas source code for information about each of these.

The design document will call out when to use these options:

- ChallengeScreenNode
  - accessibleChallengePrompt
  - accessibleAnswerSummary
- InfiniteStatusBar
  - accessibleMessageStringProperty

Additional options relating to vegas accessibility:

- LevelSelectionScreenNode
  - accessibleIncludeOptionsDescription
- LevelSelectionButton
  - accessibleBriefLevelName
- RewardDialog
  - focusAfterDismissal

## Reference Implementations

- build-an-atom
- vegas/js/demo/ (lightweight samples for most vegas components)