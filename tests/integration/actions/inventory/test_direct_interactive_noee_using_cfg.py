"""Tests for inventory from CLI, interactive, without an EE, using distronode.cfg."""

import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id

from .base import TEST_FIXTURE_DIR
from .base import BaseClass


CLI = Command(
    subcommand="inventory",
    execution_environment=True,
    precommand=f"cd {TEST_FIXTURE_DIR}/using_distronode_cfg && ",
).join()

initial_steps = (
    UiTestStep(user_input=CLI, comment="distronode-navigator inventory command top window"),
    UiTestStep(
        user_input=":1",
        comment="visit host from inventory specified in distronode.cfg",
        present=["from.distronode.cfg"],
    ),
)

steps = add_indices(initial_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for inventory from CLI, interactive, without an EE, using distronode.cfg."""

    UPDATE_FIXTURES = False
