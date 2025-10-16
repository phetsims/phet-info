# Vegas Description - Quickstart Guide

@author Jesse Greenberg

A quick guide for adding Core Description to a game screen in a PhET simulation using vegas.

This guide builds off of the [Core Description Quickstart Guide](https://github.com/phetsims/phet-info/blob/main/doc/core-description-quickstart-guide.md).
Most importantly, you should be familiar with `pdomOrder`, `accessibleName`, and `accessibleHelpText`.

## Overall Process

This is the overall process for instrumenting a game:

- Opt out of default ScreenView sections with `includeAccessibleSectionNodes: false`.
- Use prepared classes for level selection, challenge, and reward screens to help with `pdomOrder` and focus management.
- Use `pdomOrder` in each of the level selection, challenge, and reward screens to place game UI components into logical sections.
- Use vegas buttons and controls to get default accessibility content like `accessibleName`, `accessibleHelpText`, and `accessibleContextResponse`.
- Implement focus management to avoid loss of focus when components change visibility.

## Implementation Steps

### 1) Remove default accessibility sections from ScreenView

ScreenView includes default accessibility content that works well for PhET simulations
but does not work for games. Remove these sections with ScreenView options 
`includeAccessibleSectionNodes: false`

```ts
const myScreenView = new ScreenView( {
  includeAccessibleSectionNodes: false
} );
```

### 2) Use LevelSelectionScreenNode

Many games have a level selection screen. The implementation of this screen should extend
or be a child of a `LevelSelectionScreenNode`.

The `LevelSelectionScreenNode` provides accessible sections for UI components in the
level selection screen. Similar to how ScreenView provides "Play Area" and "Control Area"
sections, the `LevelSelectionScreenNode` provides sections for "Choose Your Level" and
"Game Options".

The `LevelSelectionScreenNode` includes a boilerplate introductory description. It can
take one of two forms, depending on if your level selection screen has game options.
If it does, provide option `accessibleIncludeOptionsDescription`.

Use `pdomOrder` with the sections in `LevelSelectionScreenNode` to place UI components
into the right section. There is a section for the level selection buttons and a section
for other game options. The design team will specify where components should go. But generally,
the level selection and info button goes in the level buttons section, and everything
else goes in the controls section.

```ts
class MyLevelSelectionScreen extends LevelSelectionScreenNode {
  public constructor() {
    const levelButtons = new LevelSelectionButtonGroup();
    super( screenNameStringProperty, levelButtons, {
      accessibleIncludeOptionsDescription: true
    } );
    
    const timerButton = new GameTimerToggleButton();
    const resetAllButton = new ResetAllButton();

    this.accessibleLevelsSectionNode.pdomOrder = [ levelButtons, infoButton ];
    this.accessibleControlsSectionNode.pdomOrder = [ timerButton, resetAllButton ];
  }
}
```

### 3) Use ChallengeScreenNode

For each game challenge screen, extend or add content as children to a `ChallengeScreenNode`.
The `ChallengeScreenNode` provides accessible sections for UI components in the challenge.
There are sections for the challenge components, answer submission components, and game
status components.

If your game has a number of levels, number of challenges, or level challenge count, include
this information in options.

Use `pdomOrder` with the sections in `ChallengeScreenNode` to place UI components
into the right section. There is a section for the "challenge" content, a section for
"answer" content, and a section for "status" content. The design team will specify
where components should go. Generally, gameplay challenge content goes into the "challenge"
section, while answer buttons and controls go into the "answer" section. The "status" section
almost always has a `FiniteStatusBar` or `InfiniteStatusBar`.

```ts
class MyGameChallenge extends ChallengeScreenNode {
  public constructor() {
    super( {
      challengeNumberProperty: challengeNumberProperty,
      challengeCountProperty: challengeCountProperty,
      levelNumberProperty: levelNumberProperty
    } );

    const gameDiagram = new GameDiagram();
    const gameNumberControl = new NumberControl();

    const checkAnswerButton = new CheckButton();
    const tryAgainButton = new TryAgainButton();
    
    const finiteStatusBar = new FiniteStatusBar();

    this.accessibleChallengeSectionNode.pdomOrder = [ gameDiagram, gameNumberControl ];
    this.accessibleAnswerSectionNode.pdomOrder = [ checkAnswerButton, tryAgainButton ];
    this.accessibleStatusSectionNode.pdomOrder = [ finiteStatusBar ];
  }
}
```

### 4) Use RewardScreenNode

Games often have a reward screen, usually with a RewardDialog or a LevelCompletedNode. Your game
screen that shows this content should extend or add content as children to the `RewardScreenNode`.
The `RewardScreenNode` provides an accessible section for all reward content.

Use `pdomOrder` with the section in RewardScreenNode to place UI components into the 
right section. There is only one section for reward content. It will usually contain
a LevelCompletedNode or a RewardDialog.

```ts
class MyRewardScreen extends RewardScreenNode {
  public constructor() {
    super();

    const levelCompletedNodde = new LevelCompletedNode()
    this.accessibleRewardSectionNode.pdomOrder = [ levelCompletedNode ];
  }
}
```

### 5) Use Vegas UI components

Vegas has some prepared buttons that should be used in games. These buttons contain
default label strings and may include accessible names, accessible help text, and
accessible context responses. The buttons do not include any visual styling or other behavior.

### 6) Focus Management

Games require extra work for focus management. You need to make sure that focus is
placed somewhere reasonable when the screen changes or UI components disappear.

- Use `show()` and `hide()` methods on the vegas screen Nodes. The vegas screen Nodes handle focus management for you.
  The `LevelSelectionScreenNode` will place focus on the most recently pressed level selection button. The `GameScreenNode` will
  put focus on its top most "Challenge" heading. These methods may also trigger designed context responses
  that should happen after the new screen becomes visible.

- When the CheckButton is pressed, focus should usually move to the TryAgainButton or the NextButton depending on the challenge results.
- When the ShowAnswerButton is pressed, focus should usually move to the NextButton.
- When the GameInfoButton is pressed, focus should move into the GameInfoDialog. This should happen automatically.

### Section on Responses when buttons are pressed
For example, when the "Check Answer" is pressed, there will be a designed response for different game cases.

### Section on using hide/show on various vegas dialogs and screens to get built-in behavior.

### Specific options like
accessibleBriefLevelName

### Reference examples
Point to build-an-atom and possibly number-pairs.