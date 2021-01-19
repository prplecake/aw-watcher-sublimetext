# aw-watcher-sublimetext

[Sublime Text 3][st3] plugin that acts as a watcher for
[Activity Watch][activity-watch]. It tracks files, languages, and
projects.

[st3]:https://sublimetext.com
[activity-watch]:https://activitywatch.net/

This project was based off [aw-watcher-sublime][aw-watcher-sublime] by 
[kostasdizas][kostasdizas], however, that project hasn't been updated
since May 2020, and improvements have been identified and made.

[aw-watcher-sublime]:https://github.com/kostasdizas/aw-watcher-sublime
[kostasdizas]:https://github.com/kostasdizas

## Notable Changes

This is a mostly complete list of difference between this
aw-watcher-sublimetext and the old aw-watcher-sublime.

* File paths all follow Unix-style conventions. Forward slashes, et al.
* Configuration is loaded and available at plugin initialization.

## Installation

### From Source

[Download the latest release][releases] and extract the archive to your
Sublime Text 3 Packages directory.

Navigate to **Preferences -> Browse Packages** to find out where your
Packages directory is.

[releases]:https://git.sr.ht/~mjorgensen/aw-watcher-sublimetext/refs
