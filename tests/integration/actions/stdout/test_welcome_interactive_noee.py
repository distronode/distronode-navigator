"""Tests for stdout from welcome, interactive, without an EE."""

import pytest

from .base import DISTRONODE_PLAYBOOK
from .base import BaseClass


CLI = "distronode-navigator --execution-environment false"

testdata = [
    (0, CLI, "welcome", ":help help"),
    (1, f":run {DISTRONODE_PLAYBOOK}", "Play list", "Successful"),
    (2, ":st", "Check stdout", ":help help"),
    (3, ":back", "Return to play list", ":help help"),
    (4, ":stdout", "Check stdout", ":help help"),
    (5, ":back", "Return to playlist", ":help help"),
]


@pytest.mark.parametrize("index, user_input, comment, search_within_response", testdata)
class Test(BaseClass):
    """Run the tests for stdout from welcome, interactive, without an EE."""

    UPDATE_FIXTURES = False
