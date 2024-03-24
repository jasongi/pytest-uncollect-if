from collections.abc import Generator
from typing import Any, Optional

import pytest
from pytest import Collector, CollectReport, hookimpl


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "uncollect_if(func(**kwargs)): tests marked with uncollect_if"
        " will not be collected if func(**kwargs) returns True - "
        "like skipif but will not output as a skipped test",
    )


@hookimpl(hookwrapper=True)
def pytest_make_collect_report(
    collector: Collector,
) -> Generator[Optional[CollectReport], Any, None]:
    outcome = yield None
    report: Optional[CollectReport] = outcome.get_result()
    if report:
        kept = []
        for item in report.result:
            m = item.get_closest_marker("uncollect_if")
            if m:
                func = m.kwargs["func"]
                if not (hasattr(item, "callspec") and hasattr(item.callspec, "params")):
                    raise ValueError(
                        "uncollect_if can only be run on parametrized tests"
                    )
                if func(**item.callspec.params):
                    continue
            kept.append(item)
        report.result = kept
        outcome.force_result(report)


uncollect_if = pytest.mark.uncollect_if
