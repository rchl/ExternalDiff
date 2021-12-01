import sublime
import sublime_plugin
import subprocess
from typing import Optional, Tuple


def nice_platform_string() -> str:
    platform = sublime.platform()
    if platform == 'osx':
        return 'mac'
    elif platform == 'windows':
        return 'win'
    elif platform == 'linux':
        return 'linux'
    else:
        raise Exception('Unsupported platform')


class ExternalDiffCommand(sublime_plugin.TextCommand):
    def is_enabled(self) -> bool:
        return self._get_views() is not None

    def run(self, edit) -> None:
        views = self._get_views()
        if views is None:
            return
        settings = sublime.load_settings('ExternalDiff.sublime-settings')
        platform_cmd = settings.get(nice_platform_string())
        command = platform_cmd['cmd'] if platform_cmd else settings.get('cmd')
        left_filename, right_filename = views
        command = [c.replace('$left_file', left_filename) for c in command]
        command = [c.replace('$right_file', right_filename) for c in command]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode != 0 and process.stderr:
            sublime.error_message(f'Error running process: {process.stderr}')

    def _get_views(self) -> Optional[Tuple[str, str]]:
        current_view = self.view
        window = current_view.window()
        # At least two groups required.
        if not window or window.num_groups() < 2:
            return None
        current_group_index = window.active_group()
        # Find other buffer on the right or left of the current one.
        other_group_index = (current_group_index + 1) % window.num_groups()
        other_view = window.active_view_in_group(other_group_index)
        if not other_view:
            return
        current_filename = current_view.file_name()
        other_filename = other_view.file_name()
        # Return if file does not psychically exist on disk or is modified.
        if not current_filename or current_view.is_dirty() or not other_filename or other_view.is_dirty():
            return None
        return (current_filename, other_filename) if current_group_index < other_group_index else (other_filename, current_filename)
