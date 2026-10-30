- `check_on_startup`: after Anki's own sync when a profile opens, check the
  repo for EN card changes and show the preview if there are any.
- `git_path`: full path to `git` if it is not found automatically.
- `sync_before_update`: run Anki's sync first so the plan compares the repo with
  the latest AnkiWeb data. Keep this on.
- `sync_after_update`: run Anki's sync after applying so other devices receive
  the changes.
