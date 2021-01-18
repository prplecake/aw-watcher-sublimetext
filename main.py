import sublime
import sublime_plugin

from .activitywatch.api import ActivityWatchAPI
from .activitywatch import utils

# globals
CLIENT_ID = "aw-watcher-sublimetext"
SETTINGS_FILE = "aw-watcher.sublime-settings"
SETTINGS = {}
DEBUG = False
CONNECTED = False
api = ActivityWatchAPI()


def plugin_loaded():
	global SETTINGS
	SETTINGS = sublime.load_settings(SETTINGS_FILE)

	utils.log("Initializing ActivityWatch plugin.")

	after_loaded()


def after_loaded():
	global CONNECTED, DEBUG
	if DEBUG:
		utils.log("after_loaded() called")
	global api
	api.setup(
		CLIENT_ID, SETTINGS.get("hostname"),
		SETTINGS.get("port"), SETTINGS.get("heartbeat_frequency"))
	CONNECTED = api.check()
	DEBUG = SETTINGS.get("debug")
	if DEBUG:
		api.enable_debugging()

		utils.log("hostname: {}\n\tport: {}\n\theartbeat_freq: {}\n\tbucket_name: {}\n\tdebug: {}".format(
			SETTINGS.get("hostname"), SETTINGS.get("port"),
			SETTINGS.get("heartbeat_freq"), SETTINGS.get("bucket_name"),
			SETTINGS.get("debug")))
		utils.log("Connected? {}".format(CONNECTED))


def get_file_name(view):
	return view.file_name() or view.name() or "untitled"


def get_project_name(view):
	window = view.window()
	project = "unknown"
	if hasattr(window, "project_data"):
		project = window.project_data()
	if not project:
		project = "unknown"
	if "name" in project:
		project = project.get("name")
	elif "folders" in project:
		for folder in project.get("folders"):
			if get_file_name(view).startswith(folder.get("path")):
				project = folder.get("path")
				break
	return project


def get_language(view):
	try:
		point = view.sel()[0].begin()
	except IndexError:
		return
	scopes = view.scope_name(point).strip().split(" ")
	return scopes[0]


def handle_activity(view):
	if DEBUG:
		utils.log("handle_activity() fired")
	if CONNECTED:
		api.ensure_bucket(SETTINGS.get("bucket_name"))
	else:
		active_window = sublime.active_window()
		if active_window:
			for view in active_window.views():
				view.set_status(
					CLIENT_ID,
					"[aw-watcher-sublimetext] Could not connect "
					"to aw-server")
	event_data = {
		"file": get_file_name(view),
		"project": get_project_name(view),
		"language": get_language(view),
	}
	if DEBUG:
		utils.log("file: {}\n\tproject: {}\n\tlanguage: {}".format(
			event_data["file"],
			event_data["project"],
			event_data["language"]))
	api.heartbeat(SETTINGS.get("bucket_name"), event_data)


class ActivityWatchListener(sublime_plugin.EventListener):

	def on_selection_modified_async(self, view):
		if DEBUG:
			utils.log("on_selection_modified_async fired")
		if CONNECTED:
			handle_activity(view)

	def on_modified_async(self, view):
		if DEBUG:
			utils.log("on_modified_async fired")
		if CONNECTED:
			handle_activity(view)
