"""Herein lies the ability for distronode-runner to run the distronode-inventory command."""

from __future__ import annotations

from distronode_runner import get_inventory

from .base import Base


class DistronodeInventory(Base):
    # pylint: disable=too-many-arguments
    """Abstraction for distronode-inventory command-line."""

    def fetch_inventory(
        self,
        action: str,
        inventories: list,
        response_format: str | None = None,
        host: str | None = None,
        playbook_dir: str | None = None,
        vault_ids: str | None = None,
        vault_password_file: str | None = None,
    ) -> tuple[str, str]:
        """Run distronode-inventory command and get the inventory related details.

        :param action: Valid values are one of ``graph``, ``host``, ``list``, ``graph`` create
            inventory graph, ``host`` returns specific host info and works as inventory script
            and ``list`` output all hosts info and also works as inventory script.
        :param inventories: List of inventory host paths
        :param response_format: The output format for response. Valid values can be one of ``json``,
            ``yaml``, ``toml``. If ``action`` is ``graph`` only allowed value is ``json``.
        :param host: When ``action`` is set to ``host`` this parameter is used to get the host
            specific information.
        :param playbook_dir: This parameter is used to sets the relative path for the inventory
        :param vault_ids: The vault identity to use
        :param vault_password_file: The vault identity to use
        :returns: A tuple of response and error string (if any)
        """
        return get_inventory(
            action,
            inventories=inventories,
            response_format=response_format,
            host=host,
            playbook_dir=playbook_dir,
            vault_ids=vault_ids,
            vault_password_file=vault_password_file,
            **self._runner_args,
        )
