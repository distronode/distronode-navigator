"""Herein lies the ability for distronode-runner to run the distronode-config command."""

from __future__ import annotations

import warnings


# Remove this catch-all once newer distronode-runner is released
# https://github.com/distronode/distronode-runner/issues/1223
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from distronode_runner import get_distronode_config

from .base import Base


class DistronodeConfig(Base):
    """Abstraction for distronode-config command-line."""

    def fetch_distronode_config(
        self,
        action: str,
        config_file: str | None = None,
        only_changed: bool | None = None,
    ) -> tuple[str, str]:
        """Run distronode-config command and get the configuration related details.

        :param action: The configuration fetch action to perform. Valid values are one of
            ``list``, ``dump``, ``view``. The ``list`` action will fetch all the config
            options along with config description, ``dump`` action will fetch all the active
            config and ``view`` action will return the active configuration file view.
        :param config_file: Path to configuration file, defaults to first file found in
            precedence. Defaults to ``None``.
        :param only_changed: The boolean value when set to ``True`` returns only the
            configurations that have changed from the default. This parameter is applicable only
            when ``action`` is set to ``dump``. Defaults to `None`.
        :returns: A tuple of response and error string (if any)
        """
        return get_distronode_config(
            action,
            config_file=config_file,
            only_changed=only_changed,
            **self._runner_args,
        )
