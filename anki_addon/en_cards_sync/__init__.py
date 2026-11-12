"""EN Cards Sync: update the EN decks from the GitHub repo inside the Anki app.

Tools > Update EN cards from GitHub runs:
  1. Anki's own sync, so the local collection matches AnkiWeb first;
  2. git pull in the EN repo this add-on lives in;
  3. a plan (scripts/anki/anki_sync.py), shown before applying;
  4. the changes as one undoable step ("Update EN cards");
  5. Anki's own sync again, so AnkiWeb and other devices receive them.

Note renames and removals come from the cards/anki_changes.json record of every
commit since the last applied one. That commit is remembered in the collection
config, which syncs, so every computer continues from the same point.

Deck-root renames are planned separately and applied through Anki's native deck API.
Only the official Anki client talks to AnkiWeb. The planner never changes a
note type's fields and deletes only notes a change record names.
"""
from __future__ import annotations

import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

from aqt import gui_hooks, mw
from aqt.operations import CollectionOp, QueryOp
from aqt.qt import QAction, QDialog, QDialogButtonBox, QTextBrowser, QVBoxLayout
from aqt.utils import showWarning, tooltip

ADDON_DIR = Path(__file__).resolve().parent
REPO = ADDON_DIR.parents[1]
ENGINE_DIR = REPO / 'scripts' / 'anki'
UNDO_LABEL = 'Update EN cards'
LAST_COMMIT_KEY = 'enCardsSync.lastCommit'
_startup_check_done = False


def config() -> dict:
    return mw.addonManager.getConfig(__name__) or {}


def git_binary() -> str:
    configured = config().get('git_path', '').strip()
    candidates = [configured, str(Path.home() / '.local/bin/git'), '/opt/homebrew/bin/git',
                  '/usr/local/bin/git', shutil.which('git') or '']
    for candidate in candidates:
        if candidate and os.access(candidate, os.X_OK):
            return candidate
    raise RuntimeError('git was not found; set "git_path" in this add-on\'s config')


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
    env['PATH'] = os.pathsep.join([str(Path.home() / '.local/bin'), '/opt/homebrew/bin', '/usr/local/bin',
                                   env.get('PATH', '')])
    result = subprocess.run([git_binary(), '-C', str(REPO), *args],
                            capture_output=True, text=True, env=env, timeout=120)
    if check and result.returncode != 0:
        raise RuntimeError(f'git {args[0]} failed:\n{result.stderr or result.stdout}')
    return result





def engine():
    """Load the planner from the repo, reloading it in case git pull changed it."""
    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))
    modules = [importlib.import_module(name) for name in ('exports', 'anki_sync')]
    for module in modules:
        importlib.reload(module)
    return modules[-1]


class PreviewDialog(QDialog):
    def __init__(self, report: str, can_apply: bool) -> None:
        super().__init__(mw)
        self.setWindowTitle('Update EN cards')
        self.resize(760, 520)
        layout = QVBoxLayout(self)
        browser = QTextBrowser(self)
        browser.setMarkdown(report)
        layout.addWidget(browser)
        buttons = QDialogButtonBox(self)
        if can_apply:
            buttons.addButton('Apply and sync', QDialogButtonBox.ButtonRole.AcceptRole)
        buttons.addButton(QDialogButtonBox.StandardButton.Close if not can_apply
                          else QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


def sync_then(after) -> None:
    """Run Anki's own collection+media sync, then call `after` once it finishes."""
    if not mw.pm.sync_auth():
        showWarning('Log in to AnkiWeb in Anki (the Sync button) before updating EN cards.')
        return
    mw._sync_collection_and_media(after)


def start_update(sync_first: bool = True) -> None:
    global _startup_check_done
    _startup_check_done = True  # a manual run makes the startup check unnecessary
    if sync_first and config().get('sync_before_update', True):
        sync_then(lambda: plan_update())
    else:
        plan_update()


def plan_update() -> None:
    def op(col):
        pulled = git('pull', '--ff-only').stdout.strip()
        head = git('rev-parse', 'HEAD').stdout.strip()
        sync = engine()
        exports = sys.modules['exports']
        records, history = exports.change_records(git, col.get_config(LAST_COMMIT_KEY, None), head)
        cfg = sync.load_config(REPO / 'cards' / 'anki_sync.json')
        changes = sync.merge_changes(records)
        return pulled, head, history, sync, cfg, sync.build_plan(col, cfg, REPO, changes)

    def on_success(result) -> None:
        pulled, head, history, sync, cfg, plan = result
        if plan.empty:
            mw.col.set_config(LAST_COMMIT_KEY, head)
            tooltip(f'EN cards are already up to date ({sum(plan.unchanged.values())} notes checked).')
            return
        report = f'_git pull:_ {pulled}  \n_{history}_\n\n' + sync.render_report(plan, applied=False)
        if not config().get('confirm_before_apply', True) or PreviewDialog(report, can_apply=True).exec():
            apply_update(sync, cfg, plan, head)

    def on_failure(error: Exception) -> None:
        showWarning(f'EN cards were not updated.\n\n{error}')

    QueryOp(parent=mw, op=op, success=on_success).failure(on_failure).with_progress(
        'Checking EN cards…').run_in_background()


def apply_update(sync, cfg: dict, plan, head: str) -> None:
    def op(col):
        position = col.add_custom_undo_entry(UNDO_LABEL)
        try:
            sync.apply_plan(col, plan, cfg, REPO)
            col.set_config(LAST_COMMIT_KEY, head, undoable=True)
        except Exception:
            col.merge_undo_entries(position)
            col.undo()
            raise
        return col.merge_undo_entries(position)

    def on_success(_changes) -> None:
        tooltip(f'EN cards updated: {len(plan.additions)} added, {len(plan.updates)} updated, '
                f'{len(plan.renames)} notes renamed, {len(plan.deck_renames)} decks renamed, '
                f'{len(plan.removals)} removed. Syncing…')
        if config().get('sync_after_update', True):
            sync_then(lambda: mw.toolbar.redraw())

    CollectionOp(parent=mw, op=op).success(on_success).failure(
        lambda error: showWarning(f'EN cards update was rolled back.\n\n{error}')).run_in_background()


def on_sync_did_finish() -> None:
    """Optional: check once after Anki's own startup sync."""
    global _startup_check_done
    if _startup_check_done or not config().get('check_on_startup', False):
        return
    _startup_check_done = True
    mw.progress.single_shot(500, lambda: start_update(sync_first=False))


def setup() -> None:
    action = QAction('Update EN cards from GitHub', mw)
    action.triggered.connect(lambda: start_update())
    mw.form.menuTools.addAction(action)
    gui_hooks.sync_did_finish.append(on_sync_did_finish)


setup()
