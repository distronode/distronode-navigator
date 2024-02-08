"""``:help`` command implementation."""

from distronode_navigator.action_base import ActionBase
from distronode_navigator.app_public import AppPublic
from distronode_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from distronode_navigator.content_defs import ContentFormat
from distronode_navigator.ui_framework import Interaction
from distronode_navigator.utils.packaged_data import retrieve_content

from . import _actions as actions


@actions.register
class Action(ActionBase):
    """``:help`` command implementation."""

    KEGEX = r"^h(?:elp)?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:help`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="help")

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Execute the ``:help`` request.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~distronode_navigator.ui_framework.ui.Interaction`
        """
        self._logger.debug("help requested")
        self._prepare_to_run(app, interaction)

        help_md = retrieve_content(filename="help.md")
        while True:
            interaction = interaction.ui.show(
                obj=help_md,
                content_format=ContentFormat.MARKDOWN,
            )
            app.update()
            if interaction.name != "refresh":
                break

        self._prepare_to_exit(interaction)
        return interaction
