===================
pytest-uncollect-if
===================

.. image:: https://img.shields.io/pypi/v/pytest-uncollect-if.svg
    :target: https://pypi.org/project/pytest-uncollect-if
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-uncollect-if.svg
    :target: https://pypi.org/project/pytest-uncollect-if
    :alt: Python versions

.. image:: https://github.com/jasongi/pytest-uncollect-if/actions/workflows/main.yml/badge.svg
    :target: https://github.com/jasongi/pytest-uncollect-if/actions/workflows/main.yml
    :alt: See Build Status on GitHub Actions

----

A pytest plugin to uncollect tests based on a condition without the tests being included in the `skipped` for `deselected` report counts. This makes it easier use the `Cartesian product`_ of two different usages of `pytest.mark.parametrize`_ where you want to disable a specific combination.

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Requirements
------------

* pytest > 6.2.0

For development requirements, run

.. code-block:: bash

    pip install -r requirements-dev.txt


Installation
------------

You can install "pytest-uncollect-if" via `pip`_ from `PyPI`_

.. code-block:: bash

    pip install pytest-uncollect-if

If you do not have `autoload`_ enabled, add the plugin to your top-level conftest.py

.. code-block:: python

    pytest_plugins = ("pytest_uncollect_if.plugin",)


Usage
-----
The marker takes a single argument :code:`func` which accepts parameters as :code:`**kwargs` and returns a boolean value. If the return value is :code:`True`, the test will be uncollected.
To avoid fragile statements that fail on extra parameters, be sure to add :code:`**kwargs` to your function signature.

.. code-block:: python

    param1_decorator = pytest.mark.parametrize("param1", [1, 2, 3, 4])
    param2_decorator = pytest.mark.parametrize("param2", [1, 2, 3, 4])


    # uncollect if param and param2 are equal
    @pytest.mark.uncollect_if(func=lambda param1, param2, **kwargs: param1 == param2)
    def test_uncollect_if(param1, param2):
        assert param != param2

A typed alias for :code:`pytest.mark.uncollect_if` is available as :code:`uncollect_if`

.. code-block:: python

    from pytest_uncollect_if import uncollect_if

    param1_decorator = pytest.mark.parametrize("param1", [1, 2, 3, 4])
    param2_decorator = pytest.mark.parametrize("param2", [1, 2, 3, 4])


    # uncollect if param and param2 are equal
    @uncollect_if(func=lambda param1, param2, **kwargs: param1 == param2)
    def test_uncollect_if(param1, param2):
        assert param != param2


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-uncollect-if" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: https://opensource.org/licenses/MIT
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/jasongi/pytest-uncollect-if/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`Cartesian product`: https://en.wikipedia.org/wiki/Cartesian_product
.. _`pytest.mark.parametrize`: https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-parametrize
.. _`autoload`: https://docs.pytest.org/en/7.1.x/reference/reference.html#envvar-PYTEST_DISABLE_PLUGIN_AUTOLOAD
