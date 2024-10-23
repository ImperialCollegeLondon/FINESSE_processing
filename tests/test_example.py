"""This file contains an example unit test.

pytest will search for tests in any file whose name begins with "test_". Tests are just
functions containing assert statements; their names must also start with "test_".

Feel free to delete this file when there are actual unit tests in this folder.
"""

from finesse_processing import __version__


def test_version():
    """Check that the version is acceptable."""
    assert __version__ == "0.1.0"
