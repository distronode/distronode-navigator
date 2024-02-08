"""Test the use of the distronode.cfg file for inventory."""

from copy import deepcopy
from pathlib import Path

import pytest

from distronode_navigator.configuration_subsystem import Configurator
from distronode_navigator.configuration_subsystem import Constants
from distronode_navigator.configuration_subsystem import NavigatorConfiguration


ee_states = pytest.mark.parametrize(
    argnames="ee_enabled",
    argvalues=(True, False),
    ids=("ee_true", "ee_false"),
)

DISTRONODE_CFG_VALID = """
[defaults]

inventory = inventory.yml,/tmp/inventory.yaml
"""


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_from_distronode_cfg(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm inventory is used from a valid distronode.cfg.

    :param ee_enabled: Indicate if EE support is enabled
    :param tmp_path: The path to a test temporary directory
    :param monkeypatch: The monkeypatch fixture
    """
    cfg_path = tmp_path / "distronode.cfg"
    with cfg_path.open(mode="w") as fh:
        fh.write(DISTRONODE_CFG_VALID)
    monkeypatch.chdir(tmp_path)
    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = True
    configurator = Configurator(
        params=["--ee", str(ee_enabled)],
        application_configuration=application_configuration,
    )
    configurator.configure()
    entry = application_configuration.entry("inventory")
    assert entry.value.source is Constants.DISTRONODE_CFG
    assert entry.value.current == [str(tmp_path / "inventory.yml"), "/tmp/inventory.yaml"]
