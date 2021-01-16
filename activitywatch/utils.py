import sublime


def log(msg):
	msg = '[aw-watcher-sublimetext] {}'.format(msg)
	print(msg)
	sublime.status_message(msg)
