def test_no_marker(pytester):
    """Make sure that a regular test runs."""

    pytester.makepyfile(
        """
        def test_sth():
            assert True
    """
    )
    result = pytester.runpytest("-v")
    result.stdout.fnmatch_lines(
        [
            "*::test_sth PASSED*",
        ]
    )
    assert result.ret == 0


def test_help_message(pytester):
    result = pytester.runpytest(
        "--markers",
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "@pytest.mark.uncollect_if(func(**kwargs)): tests marked with uncollect_if will not be collected if func(**kwargs) returns True - like skipif but will not output as a skipped test",
        ]
    )
