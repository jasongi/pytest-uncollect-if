from collections.abc import Generator
from typing import Any, Callable, Optional, Union

import pytest
from pytest import Collector, CollectReport, Function, Item, MarkDecorator, hookimpl


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
        kept: list[Union[Collector, Item]] = []
        for item in report.result:
            if isinstance(item, Function):
                m = item.get_closest_marker("uncollect_if")
                if m:
                    try:
                        func = m.kwargs["func"]
                    except KeyError:
                        raise ValueError(
                            "uncollect_if marker must have a func argument"
                        )
                    if not (
                        hasattr(item, "callspec") and hasattr(item.callspec, "params")
                    ):
                        if m.kwargs.get("raise_when_not_parametrized", True):
                            raise ValueError(
                                "uncollect_if can only be run on parametrized tests"
                            )
                    elif func(**item.callspec.params):
                        continue
            kept.append(item)
        report.result = kept
        outcome.force_result(report)
    return  # pragma: no cover - report being None is difficult to test and doesn't matter


class _UncollectIfMarkDecorator(MarkDecorator):
    def __call__(  # type: ignore[override,empty-body]
        self,
        func: Callable[..., bool],
        raise_when_not_parametrized: bool = True,
    ) -> MarkDecorator:
        """
        Mark a test to be uncollected if `func(**params)` returns True.

        Keyword arguments:
        :param Function func: function to determine if the test should be uncollected
        :param bool raise_when_not_parametrized: raise an error if the mark is applied on a test that is not parametrized defaults to True - but you may want to disable it if marking test classes while only the test methods are parametrized
        """
        ...  # pragma: no cover - it's just type hints


uncollect_if: _UncollectIfMarkDecorator = pytest.mark.uncollect_if  # type: ignore[assignment]
