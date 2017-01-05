import sublime
import sublime_plugin
import subprocess
import os
import time

from QuickSearchEnhanced.quick_search import panels

def show_output(text):
  panel = sublime.active_window().create_output_panel('switch_git_branch')
  panel.run_command('insert_text', {
    'point': 0,
    'text': text,
  })

  sublime.active_window().run_command('show_panel', {
    'panel': 'output.switch_git_branch',
  })

def get_path():
  return sublime.active_window().project_data()['folders'][0]['path']

def get_branches(all = False):
  command = ['git', 'branch']
  if all:
    command.append('-a')

  raw_branches = \
    subprocess \
      .check_output(command, stderr = subprocess.STDOUT, cwd = get_path()) \
      .decode('utf-8') \
      .split("\n")

  branches = []
  for index, branch in enumerate(raw_branches):
    branch = branch.strip()

    if branch == '':
      continue

    if branch.startswith('* '):
      continue

    branches.append(branch.strip())

  branches.sort()

  return branches

def run(command, close_on_success = True):
  try:
    result = subprocess.check_output(
      command,
      stderr = subprocess.STDOUT,
      cwd = get_path(),
    )

    panel = panels.get_current()
    if close_on_success and panel != None:
      panels.get_current().close(-1, False)

    show_output(result.decode('utf-8'))
    return True
  except subprocess.CalledProcessError as error:
    show_output(error.output.decode('utf-8'))
    return False

class CreateGitBranch(sublime_plugin.WindowCommand):
  def run(self):
    branch = panels.get_current().get_current_text()
    run(['git', 'checkout', '-b', branch])

class SwitchToGitBranch(sublime_plugin.WindowCommand):
  def run(self):
    branch = panels.get_current().get_current_value()
    run(['git', 'checkout', branch])

class DeleteGitBranch(sublime_plugin.WindowCommand):
  def run(self, force = False):
    panel = panels.get_current()
    branch = panel.get_current_value()
    flag = '-d'
    if force:
      flag = '-D'

    run(['git', 'branch', flag, branch], False)
    panel.get_caller('switch_git_branch').refresh()

class OpenGitBranchSwitcher(sublime_plugin.WindowCommand):

  def run(self, all = False):
    self.all = all

    try:
      panels \
        .create(
          get_branches(all),
          self.change_branch,
          callers = [['search_panel', None], ['switch_git_branch', self]],
        ) \
        .show()

    except subprocess.CalledProcessError as error:
      show_output(error.output.decode('utf-8'))

  def refresh(self):
    panels.get_current().set_values(get_branches(self.all))

  def change_branch(self, panel):
    sublime.active_window().destroy_output_panel('switch_git_branch')
    raw_branch = panel.get_current_value()
    branch = raw_branch
    if branch == None:
      return

    remotes = \
      subprocess \
        .check_output(
          ['git', 'remote'],
          stderr = subprocess.STDOUT,
          cwd = get_path(),
        ) \
        .decode('utf-8') \
        .split("\n")

    for remote in remotes:
      remote = remote.strip()
      if remote == '':
        continue

      prefix = 'remotes/' + remote + '/'
      if branch.startswith(prefix):
        branch = branch[len(prefix):]

    time.sleep(0.25)
    command = ['git', 'checkout', branch]
    if raw_branch != branch:
      command = ['git', 'checkout', '-b', branch, raw_branch]

    run(command)
