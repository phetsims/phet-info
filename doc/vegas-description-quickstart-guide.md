# Vegas Description - Quickstart Guide

@author Jesse Greenberg

A quick guide for adding Core Description to a game screen in a PhET simulation using vegas.

This guide builds off of the [Core Description Quickstart Guide](https://github.com/phetsims/phet-info/blob/main/doc/core-description-quickstart-guide.md).
Most importantly, you should be familiar with `pdomOrder`, `accessibleName`, and `accessibleHelpText`.

## Overall Process

The overall process for instrumenting a game with accessibility includes the following.
This is also the order in which we will walk through implementation steps in this guide.

- Opt out of default ScreenView sections with `includeAccessibleSectionNodes: false`.
- Use prepared classes for level selection, challenge, and reward screens to help with pdomOrder and focus management.
- Use `pdomOrder` in each the level selection, challenge, and reward screens to place game UI components into logical sections.
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

```ts
class MyLevelSelectionScreen extends LevelSelectionScreenNode {
  public constructor() {
    const levelButtons = new LevelSelectionButtonGroup();
    super( screenNameStringProperty, levelButtons, {
      accessibleIncludeOptionsDescription: true
    } );
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

```ts
class MyGameChallenge extends ChallengeScreenNode {
  public constructor() {
    super( {
      challengeNumberProperty: challengeNumberProperty,
      challengeCountProperty: challengeCountProperty,
      levelNumberProperty: levelNumberProperty
    } )
  }
}
```

### 4) Use RewardScreenNode

Games often have a reward screen, usually with a RewardDialog or a LevelCompletedNode. Your game
screen that shows this content should extend or add content as children to the `RewardScreenNode`.
The `RewardScreenNode` provides an accessible section for all reward content.

```ts
import RewardScreenNode from './RewardScreenNode.js';

class MyRewardScreen extends RewardScreenNode {
  public constructor() {
    super();
  }
}
```