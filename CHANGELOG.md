# Changelog

## 0.1.0 2024-03-24
- initial release
- added uncollect_if custom marker
- added `pytest_make_collect_report` hookwrapper to modify the collected items to exclude `Function` items when `uncollect_if` returns True
