import sublime
import sublime_plugin
import subprocess
import sys


def nice_platform_string():
    if sublime.platform() == 'osx':
        return 'mac'
    elif sublime.platform() == 'windows':
        return 'win'
    elif sublime.platform() == 'linux':
        return 'linux'
    else:
        raise Exception('Unsupported platform')


class ExternalDiffCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        window = view.window()

        '''Find other buffer on the right or left of the current one.'''
        other_group_index = (window.active_group() + 1) % window.num_groups()
        other_view = window.active_view_in_group(other_group_index)

        current_file = view.file_name()
        other_file = other_view.file_name()

        settings = sublime.load_settings('ExternalDiff.sublime-settings')
        platform_cmd = settings.get(nice_platform_string())
        command = platform_cmd['cmd'] if platform_cmd else settings.get('cmd')
        command = [c.replace('$file1', current_file) for c in command]
        command = [c.replace('$file2', other_file) for c in command]
        subprocess.Popen(command, stdout=None, stderr=None)

    def is_enabled(self):
        view = self.view
        window = view.window()

        '''Return if file does not psychically exist on disk or is modified.'''
        if not view.file_name() or view.is_dirty():
            return False

        '''At least two groups required.'''
        if window.num_groups() < 2:
            return False

        '''Find other buffer on the right or left of the current one.'''
        other_group_index = (window.active_group() + 1) % window.num_groups()
        other_view = window.active_view_in_group(other_group_index)

        '''Return if file does not psychically exist on disk or is modified.'''
        if not other_view or not other_view.file_name() or other_view.is_dirty():
            return False

        return True
