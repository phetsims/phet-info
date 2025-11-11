# Interacting with PhET Simulations

## Overview

PhET simulations expose their interactive elements through the **Parallel DOM (PDOM)** - a keyboard-accessible version of the simulation that describes all interactive elements and their current state. Think of it as a text-based map of everything you can interact with in the simulation.

You can interact with simulations using the keyboard daemon API at `http://localhost:3001`, which provides programmatic control over focus, navigation, and element activation.

## Basic Workflow

### 1. Initial Orientation: Look at the Simulation

Begin every interaction by surveying the simulation's accessible structure:

```bash
curl -s -X POST http://localhost:3001/cmd \
  -H "Content-Type: application/json" \
  -d '{"commands": [{"look": true}]}' | jq
```

The `look` command returns:
- **pdom**: The full accessible DOM as text, with the currently focused element marked with `>>>`
- **focusOrder**: An array of all tab-focusable elements in order, with current focus indicated
- **focus**: Details about the currently focused element

This gives you a complete map of the simulation's interactive structure.

### 2. Open Keyboard Help

Most simulations include a "Keyboard Shortcuts" button. Find and activate it:

```bash
curl -s -X POST http://localhost:3001/cmd \
  -H "Content-Type: application/json" \
  -d '{"commands": [{"find": "Keyboard Shortcuts"}]}' | jq
```

The keyboard help dialog displays available keyboard commands for the current screen. **Read this carefully** - it documents all interaction patterns specific to this simulation.

### 3. Survey After Opening Dialog

After opening the keyboard help, call `look` again to see the dialog contents:

```bash
curl -s -X POST http://localhost:3001/cmd \
  -H "Content-Type: application/json" \
  -d '{"commands": [{"look": true}]}' | jq
```

The PDOM now includes the dialog structure, and the focusOrder shows the updated tab sequence. Parse this to understand available keyboard commands.

## Navigation Patterns

### Screen Switching

PhET simulations are often divided into multiple screens (e.g., "Intro", "Lab", "Game"). Each screen has distinct interactive elements and keyboard commands.

**When switching screens:**
1. Navigate to the desired screen button (usually in a navigation bar at the bottom)
2. Activate the screen button
3. **Immediately open and read the keyboard help dialog** on the new screen
4. Call `look` to survey the new screen's structure

```bash
curl -s -X POST http://localhost:3001/cmd \
  -H "Content-Type: application/json" \
  -d '{"commands": [
    {"find": "Lab"},
    {"wait": 200},
    {"find": "Keyboard Shortcuts"},
    {"look": true}
  ]}' | jq
```

### Focus Navigation

**Tab**: Moves focus forward through interactive elements sequentially
```json
{"tab": 5}
```

**Shift+Tab**: Moves focus backward
```json
{"shiftTab": 3}
```

**Find**: Tabs until a specific element is focused, then activates it
```json
{"find": "Reset All"}
{"find": "Values", "press": "Space"}
```

**⚠️ Important**: `find` only works for elements that are **tab stops** (elements you can directly tab to). It will NOT find:
- Text labels or headings that aren't focusable
- Radio button options inside a group (you must tab to the group first, then use arrow keys)
- Items within composite widgets (tab to the widget, then use arrow keys)

If `find` fails, check the `focusOrder` array from a `look` command to see what elements are actually tab-focusable.

### Group Navigation

Many simulation elements are organized in **radio button groups**, **composite widgets**, or **application regions**. These require a two-stage navigation pattern:

1. **Tab to the group** (or to one member of the group)
2. **Use arrow keys** to navigate within the group

Example: A current direction radio group
```bash
# Tab to the group
curl -s -X POST http://localhost:3001/cmd \
  -d '{"commands": [{"find": "Conventional"}]}' | jq

# Navigate within the group using arrow keys
curl -s -X POST http://localhost:3001/cmd \
  -d '{"commands": [{"press": "ArrowDown"}]}' | jq
```

Common group patterns:
- **Radio groups**: Tab to enter, arrow keys to select options
- **Sliders**: Tab to focus, arrow keys to adjust values
- **Draggable objects**: Tab to focus, arrow keys or WASD to move
- **Composite controls**: Tab to enter, arrow keys to navigate sub-elements

## Understanding Feedback

### ARIA Live Announcements

Many interactions trigger **aria-live** announcements that provide dynamic feedback without changing focus:

```json
{
  "success": true,
  "command": {"press": "ArrowDown"},
  "action": "Pressed ArrowDown",
  "focus": {"name": "Conventional", "role": ""},
  "ariaLive": ["Conventional current selected"]
}
```

These announcements convey state changes, values, or descriptions. **Always check the `ariaLive` field** in command responses - it often contains critical information about what happened.

### Focus Information

Every command returns the currently focused element:

```json
{
  "focus": {
    "name": "Show Current Values",
    "role": "checkbox",
    "checked": true
  }
}
```

Use this to track your position and verify successful navigation.

## Effective Interaction Strategy

1. **Survey first**: Call `look` to understand the simulation structure and see the tab order
2. **Read instructions**: Open keyboard help to learn interaction patterns
3. **Navigate deliberately**: Use `find` for known tab stops, `tab` for exploration
4. **Monitor feedback**: Check `ariaLive` and `focus` in responses
5. **Understand groups**: Identify composite controls and use arrow keys appropriately
6. **Screen transitions**: Re-read keyboard help when switching screens
7. **Verify state**: Call `look` periodically to confirm simulation state

## Common Mistakes

Avoid these common pitfalls when interacting with simulations:

### ❌ Using `find` for non-tab-stops
**Problem**: Trying to find text that isn't a focusable element
```json
{"find": "5"}  // Fails if "5" is inside a radio group
```
**Solution**: Use `look` to check `focusOrder`, tab to the group, then use arrow keys
```json
{"find": "Right Addend Choices"}
{"press": "ArrowRight"}
```

### ❌ Expecting arrow keys without tabbing to a group first
**Problem**: Pressing arrow keys before focusing the interactive region
**Solution**: Always tab to the group/widget first, then use arrow keys within it

### ❌ Not checking `ariaLive` announcements
**Problem**: Missing important feedback about state changes
**Solution**: Always examine the `ariaLive` field in command responses - it contains critical information about what happened

### ❌ Ignoring the `focusOrder` array
**Problem**: Repeatedly trying `find` commands that fail
**Solution**: Check `focusOrder` from a `look` command to see exactly what elements are tab-focusable

### ❌ Not waiting for animations/updates
**Problem**: Commands executing before the simulation updates
**Solution**: Use `{"wait": 200}` after actions that trigger animations or state changes

## Advanced Commands

**Wait for animations**: Give the simulation time to update
```json
{"wait": 500}
```

**Direct key press**: Activate or control the focused element
```json
{"press": "Space"}
{"press": "Enter"}
{"press": "ArrowRight"}
{"press": "w"}
```

**Check status**: Query the daemon state
```bash
curl -s http://localhost:3001/status | jq
```

**Reload simulation**: Reset if things go wrong
```bash
curl -s -X POST http://localhost:3001/reload | jq
```

## Key Principles

- **Use `look` to orient yourself**: The PDOM shows the accessible structure, focusOrder shows the tab sequence - survey regularly
- **`find` only works for tab stops**: Check focusOrder to see what's actually findable
- **Keyboard help is documentation**: Each screen's keyboard help defines its interaction model
- **Groups require arrow keys**: Don't just tab through everything - understand when you're in a composite control
- **ARIA live provides feedback**: Watch for these announcements to understand state changes
- **Focus tracking is essential**: The >>> markers in PDOM and focusOrder show where you are
- **Screen boundaries matter**: Different screens have different controls and keyboard commands