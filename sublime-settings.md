---
title: Sublime Settings
---

In case you run ActivityWatch on a different host/port, you can
configure those settings for the Sublime Text 3 watcher. 

Simply navigate to **Preferences -> Package Settings -> aw-watcher ->
Settings** and you'll be able to override the default settings.

## Settings

### `hostname`

Type: string

The hostname for your ActivityWatch server, usually `localhost`.

### `port`

Type: integer

The port for your ActivityWatch server, usually `5600`.

### `heartbeat_frequency`

Type: integer

The frequecy of heartbeats you'd wish to send to your ActivityWatch
server. Default: `10`.

### `bucket_name`

Type: string

The name of the bucket you wish data to be added to. Default:
`aw-watcher-sublimetext`.

### `debug`

Type: boolean

Whether or not to print debug logs to the Sublime Text 3 console and
status bar. Default: `false`.