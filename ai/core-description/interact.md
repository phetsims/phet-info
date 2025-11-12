# Interact CLI - Simplified Simulation Control

The `interact` command provides a human-friendly interface to the keyboard daemon, eliminating curl/JSON complexity.

## Setup

Add to `~/.zshrc` (adjust path for your system):
```bash
alias interact='sage run ~/phet/root/chipper/js/grunt/tasks/interact.ts'
```

Reload: `source ~/.zshrc`

## Prerequisites

Start the keyboard daemon in a separate terminal:
```bash
cd your-sim-repo
grunt interact-daemon --screens=2
```

This is a "blocking" process that runs until you stop it (Ctrl+C).

NOTE: It may already be running from a prior session. Check `interact status` to see if it is active.

## Core Commands

### Observing State

```bash
interact peek                    # Show PDOM (doesn't change focus)
interact look                    # Show PDOM + focus order (WARNING: changes focus)
interact getFocus                # Show currently focused element
interact status                  # Check daemon status
```

**Important:** `look` generates the focus order by tabbing through all elements, which may hide popups or dialogs if focus leaves them. Use `peek` for non-invasive PDOM inspection.

### Navigation

```bash
interact tab 5                   # Tab forward 5 times
interact tab "Reset All"         # Tab to element named "Reset All" (doesn't activate)
interact shiftTab 1              # Shift+Tab once (tab backward)
interact shiftTab 3              # Shift+Tab three times (tab backward)
```

The `tab "name"` command tabs until it finds the named element and stops without pressing any keys.

**Note:** To tab backward, use `shiftTab`, not `press Shift+Tab`. The `press` command is for activating or controlling the currently focused element.

### Activation

```bash
interact press Space             # Press Space on focused element
interact press Enter             # Press Enter on focused element
interact press ArrowDown         # Press ArrowDown on focused element
```

Common pattern - tab to element, then activate:
```bash
interact tab "Reset All" + press Space
interact tab "Submit" + press Enter
```

### Timing & Control

```bash
interact wait 200                # Wait 200ms (useful after actions)
interact reload                  # Reload simulation (recovery)
```

### Navigation Between Sims

```bash
interact navigate "http://localhost/number-pairs/number-pairs_en.html?brand=phet-io&ea&debugger&screens=5"
```

## Command Sequences

Chain commands with `+`:
```bash
# Open keyboard help
interact tab "Keyboard Shortcuts" + press Space + wait 200 + peek

# Navigate to Lab screen and survey
interact tab "Lab" + press Space + wait 300 + look

# Multi-step interaction
interact tab 5 + press ArrowDown + wait 100 + peek
```

## Options

```bash
--daemonPort=3001       # Daemon port (default: 3001)
--daemonHost=localhost  # Daemon host (default: localhost)
--continueOnError       # Continue on command failure
--raw / --json          # Output raw JSON (for LLMs)
--debug                 # Show debug info
```

## Output

Default output is human-readable with:
- Focus information (name, role, checked state, value)
- ARIA live announcements (prefixed with 🔊)
- PDOM tree (with `>>>` marking focused element)
- Focus order (numbered list of tab stops)

Use `--json` for machine-readable output suitable for LLM agents.

## Common Patterns

### Initial Orientation
```bash
# Quick survey without disrupting focus
interact peek

# Full survey (if you don't mind focus changes)
interact look
```

### Opening and Reading Keyboard Help
```bash
interact tab "Keyboard Shortcuts" + press Space + wait 200 + peek
```

### Screen Switching
```bash
interact tab "Lab" + press Space + wait 300 + tab "Keyboard Shortcuts" + press Space + peek
```

### Group Navigation
Many controls are composite widgets (radio groups, sliders, draggables). Tab to them, then use arrow keys:
```bash
# Tab to radio group, then navigate within it
interact tab "Current Direction" + press ArrowDown + peek
```

### Error Recovery
```bash
# If something goes wrong
interact reload
```

## Understanding Tab Behavior

The `tab` command has two modes:

1. **Numeric**: `interact tab 5` - Tabs forward 5 times sequentially
2. **Named**: `interact tab "Reset All"` - Tabs until "Reset All" is focused, then stops (doesn't press)

Named tabbing only works for **tab stops** (focusable elements). It won't find:
- Plain text or headings
- Radio button options (tab to the group, then use arrow keys)
- Items inside composite widgets

Check `focusOrder` from `interact look` to see what's actually tab-focusable.

## Focus Order Side Effects

When you run `interact look`, it generates the focus order by tabbing through the entire focus loop. This means:
- Focus will move through all elements
- Popups/dialogs may close if they require focus to stay visible
- The simulation may briefly appear to "flash through" all interactive elements

Use `interact peek` instead when you need to inspect the PDOM without these side effects.

## Design Philosophy

**Composability**: Chain simple operations to build complex interactions
**Clarity**: Clear command names that match keyboard concepts
**Efficiency**: Minimal JSON overhead (~50-200 tokens per command)
**Debuggability**: Same commands work manually and in scripts

## For LLM Agents

The tool is optimized for AI usage:
- Simple, parseable syntax
- Structured JSON output with `--json`
- All daemon features accessible
- Composable command sequences
- Minimal token overhead
- Clear error messages

Example LLM workflow:
```bash
# Discover structure
interact peek --json | parse_pdom

# Open help to understand controls
interact tab "Keyboard Shortcuts" --json

# Interact based on discovered structure
interact tab "Show Current Values" + press Space --json
```
