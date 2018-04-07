# External Diff

Sublime Text plugin. Provides a way to trigger diff tool between two adjacent panes. Configuration file allows specifying platform specific command to invoke.

## Configuration

Package does not define any keyboard shortcuts by default. Add your own in user's keymap or use Command Palette to invoke `External Diff` command.

Use package settings to define the command to use when invoking diff. Default settings use p4merge.

### Suggested keyboard shortcuts:

Mac: `{ "keys": ["super+shift+c"], "command": "external_diff" }`

Other platforms: `{ "keys": ["ctrl+shift+c"], "command": "external_diff" }`
