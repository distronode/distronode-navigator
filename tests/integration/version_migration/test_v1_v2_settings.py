"""Check migration output."""

import filecmp
import os
import shutil

from pathlib import Path

import pytest

from tests.integration._tmux_session import TmuxSession


files = [
    "distronode-navigator_all.yml",
    "distronode-navigator_some.yml",
    "distronode-navigator_1.1.yaml",
    "distronode-navigator_1.1.json",
]


@pytest.mark.parametrize("file", files)
def test_all(
    file: str,
    request: pytest.FixtureRequest,
    test_dir_fixture_dir: Path,
    tmp_path: Path,
):
    """Test migration with a file of all changes.

    :param file: The file to test
    :param request: The pytest fixture request
    :param test_dir_fixture_dir: Path to the test directory
    :param tmp_path: The pytest tmp_path fixture
    :raises AssertionError: When tests fails
    """
    file_path = Path(file)
    file_stem = file_path.stem
    file_suffix = file_path.suffix

    source = test_dir_fixture_dir / file
    destination = tmp_path / ("distronode-navigator" + file_suffix)
    backup = tmp_path / "distronode-navigator.v1"
    corrected = test_dir_fixture_dir / (file_stem + "_corrected" + file_suffix)
    shutil.copy(source, destination)

    with TmuxSession(
        request=request,
        config_path=destination,
        cwd=tmp_path,
    ) as session:
        session.interaction(
            value="distronode-navigator --version",
            search_within_response="Do you want to run them all?",
            send_clear=False,
        )
        session.interaction(
            value="y\n",
            search_within_response="Press Enter to continue:",
            send_clear=False,
        )
        result = session.interaction(
            value="\n",
            search_within_response="distronode-navigator",
            send_clear=False,
        )

    if os.environ.get("DISTRONODE_NAVIGATOR_UPDATE_TEST_FIXTURES") == "true":
        shutil.copy(destination, corrected)

    assert any(
        "distronode-navigator 24." in line for line in result
    ), "(Note: requires recent tags, `git fetch --all`)"
    assert filecmp.cmp(destination, corrected)
    assert filecmp.cmp(source, backup)
