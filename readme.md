# Sublime SwitchGitBranch plugin

Provides quick way to switch a git branch to existing one or create new using
fuzzy complete.


### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.


### Usage

Hit keyboard shortcut to see all available branches. Type branch name and hit
"enter" to switch to selected branch (local branch will be created when
switching to origin branch).


### Commands

| Title                         | Keyboard shortcuts | Command palette                      |
|-------------------------------|--------------------|--------------------------------------|
| Open switch branch panel      | ctrl+u, ctrl+e     | SwitchGitBranch: show local branches |
| Open switch branch panel      | ctrl+u, e          | SwitchGitBranch: show all branches   |
| Checkout to branch            | ctrl+o             |                                      |
| Create branch with given name | tab                |                                      |
| Delete selected branch        | ctrl+d             |                                      |
| Force delete selected branch  | ctrl+alt+d         |                                      |


### Dependencies

* [QuickSearchEnhanced](https://github.com/shagabutdinov/sublime-quick-search-enhanced)