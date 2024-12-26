# Changelog
## 0.1.3 2024-12-26
- support python 3.13

## 0.1.2 2024-03-24
- explicitly export uncollect_if

## 0.1.1 2024-03-24
- fix entrypoint

## 0.1.0 2024-03-24
- initial release
- added uncollect_if custom marker
- added `pytest_make_collect_report` hookwrapper to modify the collected items to exclude `Function` items when `uncollect_if` returns True
