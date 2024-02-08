"""Tests for inventory from CLI, interactive, without an EE."""

import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id_padded

from .base import DISTRONODE_INVENTORY_FIXTURE_DIR
from .base import BaseClass
from .base import base_steps


cmdline = f"-i {DISTRONODE_INVENTORY_FIXTURE_DIR}"
CLI = Command(subcommand="inventory", cmdline=cmdline, execution_environment=False).join()

initial_steps = (
    UiTestStep(user_input=CLI, comment="distronode-navigator inventory command top window"),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id_padded)
class Test(BaseClass):
    """Run the tests for inventory from CLI, interactive, without an EE."""

    UPDATE_FIXTURES = False
