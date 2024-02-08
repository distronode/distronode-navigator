"""Test the basic parsing of an distronode.cfg file."""

from copy import deepcopy
from pathlib import Path

import pytest

from distronode_navigator.command_runner import Command
from distronode_navigator.command_runner.command_runner import run_command
from distronode_navigator.configuration_subsystem import Configurator
from distronode_navigator.configuration_subsystem import Constants
from distronode_navigator.configuration_subsystem import NavigatorConfiguration
from distronode_navigator.configuration_subsystem.utils import parse_distronode_cfg


ee_states = pytest.mark.parametrize(
    argnames="ee_enabled",
    argvalues=(True, False),
    ids=("ee_true", "ee_false"),
)

DISTRONODE_CFG_VALID = """
[defaults]

cow_selection = milk
inventory = inventory.yml
"""


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_valid_config(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm a valid distronode.cfg is parsed.

    :param ee_enabled: Indicate if EE support is enabled
    :param tmp_path: The path to a test temporary directory
    :param monkeypatch: The monkeypatch fixture
    """
    cfg_path = tmp_path / "distronode.cfg"
    with cfg_path.open(mode="w") as fh:
        fh.write(DISTRONODE_CFG_VALID)
    monkeypatch.chdir(tmp_path)
    parsed_cfg = parse_distronode_cfg(ee_enabled=ee_enabled)

    assert parsed_cfg.config.contents == {
        "defaults": {"cow_selection": "milk", "inventory": "inventory.yml"},
    }
    assert parsed_cfg.config.path == cfg_path
    assert parsed_cfg.config.text == DISTRONODE_CFG_VALID.splitlines()


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_valid_configurator(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm a valid distronode.cfg is parsed using configurator.

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

    assert application_configuration.internals.distronode_configuration.contents == {
        "defaults": {"cow_selection": "milk", "inventory": "inventory.yml"},
    }
    assert application_configuration.internals.distronode_configuration.path == cfg_path
    assert (
        application_configuration.internals.distronode_configuration.text
        == DISTRONODE_CFG_VALID.splitlines()
    )


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_valid_home(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm a valid .distronode.cfg is parsed when in the home directory.

    When EE support is enabled, the .distronode.cfg file is not used
    When EE support is disabled the .distronode.cfg file is used

    :param ee_enabled: Indicate if EE support is enabled
    :param tmp_path: The path to a test temporary directory
    :param monkeypatch: The monkeypatch fixture
    """
    cfg_path = tmp_path / ".distronode.cfg"
    with cfg_path.open(mode="w") as fh:
        fh.write(DISTRONODE_CFG_VALID)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))

    parsed_cfg = parse_distronode_cfg(ee_enabled=ee_enabled)

    if ee_enabled:
        assert parsed_cfg.config.contents is Constants.NONE
        assert parsed_cfg.config.path is Constants.NONE
        assert parsed_cfg.config.text is Constants.NONE
    else:
        assert parsed_cfg.config.contents == {
            "defaults": {"cow_selection": "milk", "inventory": "inventory.yml"},
        }
        assert parsed_cfg.config.path == cfg_path
        assert parsed_cfg.config.text == DISTRONODE_CFG_VALID.splitlines()


DISTRONODE_CFG_INVALID = """
[defaults]

12345
"""


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_invalid_config(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm a invalid distronode.cfg raises errors.

    :param ee_enabled: Indicate if EE support is enabled
    :param tmp_path: The path to a test temporary directory
    :param monkeypatch: The monkeypatch fixture
    """
    cfg_path = tmp_path / "distronode.cfg"
    with cfg_path.open(mode="w") as fh:
        fh.write(DISTRONODE_CFG_INVALID)
    monkeypatch.chdir(tmp_path)
    parsed_cfg = parse_distronode_cfg(ee_enabled=ee_enabled)

    assert parsed_cfg.config.contents is Constants.NONE
    assert parsed_cfg.config.path is Constants.NONE
    assert parsed_cfg.config.text is Constants.NONE
    assert "12345" in parsed_cfg.exit_messages[1].message


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_invalid_configurator(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm a invalid distronode.cfg raises errors using configurator.

    :param ee_enabled: Indicate if EE support is enabled
    :param tmp_path: The path to a test temporary directory
    :param monkeypatch: The monkeypatch fixture
    """
    cfg_path = tmp_path / "distronode.cfg"
    with cfg_path.open(mode="w") as fh:
        fh.write(DISTRONODE_CFG_INVALID)
    monkeypatch.chdir(tmp_path)
    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = True
    configurator = Configurator(
        params=["--ee", str(ee_enabled)],
        application_configuration=application_configuration,
    )
    _messages, exit_messages = configurator.configure()

    assert application_configuration.internals.distronode_configuration.contents is Constants.NONE
    assert application_configuration.internals.distronode_configuration.path is Constants.NONE
    assert application_configuration.internals.distronode_configuration.text is Constants.NONE
    assert "12345" in exit_messages[3].message


@pytest.mark.usefixtures("distronode_version")
@ee_states
def test_config_none(ee_enabled):
    """Confirm a invalid distronode.cfg raises errors.

    :param ee_enabled: Indicate if EE support is enabled
    """
    parsed_cfg = parse_distronode_cfg(ee_enabled=ee_enabled)

    assert parsed_cfg.config.contents is Constants.NONE
    assert parsed_cfg.config.path is Constants.NONE
    assert parsed_cfg.config.text is Constants.NONE
    if ee_enabled:
        assert (
            "no 'distronode.cfg' found in current working directory." in parsed_cfg.messages[1].message
        )
    else:
        assert "'distronode --version' reports no config file" in parsed_cfg.messages[2].message


@ee_states
def test_invalid_path(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm an invalid path to distronode.cfg is handled.

    :param ee_enabled: Indicate if EE support is enabled
    :param tmp_path: The path to a test temporary directory
    :param monkeypatch: The monkeypatch fixture
    """
    original_run_command = run_command

    def static_distronode_version(command: Command):
        if command.command == "distronode --version":
            command.return_code = 0
            command.stdout = f"distronode [core 2.12.3]\nconfig file = {(tmp_path / 'distronode.cfg')!s}"
        else:
            original_run_command(command)

    monkeypatch.setattr(
        "distronode_navigator.command_runner.command_runner.run_command",
        static_distronode_version,
    )

    parsed_cfg = parse_distronode_cfg(ee_enabled=ee_enabled)
    assert parsed_cfg.config.contents is Constants.NONE
    assert parsed_cfg.config.path is Constants.NONE
    assert parsed_cfg.config.text is Constants.NONE
    if ee_enabled:
        assert (
            "no 'distronode.cfg' found in current working directory." in parsed_cfg.messages[1].message
        )
    else:
        assert "does not exist" in parsed_cfg.messages[2].message
