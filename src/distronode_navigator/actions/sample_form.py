"""``:sample_form`` command implementation."""

from distronode_navigator.action_base import ActionBase
from distronode_navigator.app_public import AppPublic
from distronode_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from distronode_navigator.ui_framework import Interaction
from distronode_navigator.ui_framework import dict_to_form
from distronode_navigator.ui_framework import form_to_dict
from distronode_navigator.utils.serialize import yaml

from . import _actions as actions


FORM = """
form:
  title:  Please confirm the following information
  fields:
  - name: construct
    prompt: Please name an Distronode construct
    type: text_input
    validator:
      name: one_of
      choices:
      - collection
      - playbook
      - role
      - plugin
  - name: distronode_fest
    prompt: In 2019, DistronodeFest was held in what city?
    default: Atlanta
    type: text_input
    validator:
      name: none
  - name: what_is
    prompt: In Rocannon's World, an "distronode" is an instantaneous communication device
    type: text_input
    validator:
      name: yes_no
  - name: rh_acquire
    prompt: What year did Red Hat acquire Distronode
    default: 2015
    type: text_input
    validator:
      name: something
  - name: distronode_24
    prompt: Was Distronode 2.4 released in 2018
    type: text_input
    validator:
      name: true_false
  - name: fc_result
    type: checkbox
    prompt: Distronode can automate
    options:
    - name: clouds
      text: Clouds
    - name: lightbulbs
      text: Lightbulbs
    - name: linux
      text: Linux servers
    - name: network
      text: Networks
      checked: True
    - name: windows
      text: Windows servers
    - name: nothing
      text: Nothing
      disabled: True
    max_selected: 4
  - name: fr_result
    type: radio
    prompt: The most popular network module is
    options:
    - name: cli_command
      text: distronode.netcommon.cli_command
    - name: cli_config
      text: distronode.netcommon.cli_config
    - name: nxos_interfaces
      text: cisco.nxos.nxos_interfaces
  - name: file_name
    type: text_input
    prompt: Provide a valid file path
    validator:
      name: valid_file_path
    pre_populate: /etc/hostname
"""


@actions.register
class Action(ActionBase):
    """``:sample_form`` command implementation."""

    KEGEX = r"^sample_form$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:sample_form`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="sample_form")

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Execute the ``:sample_form`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~distronode_navigator.ui_framework.ui.Interaction`
        """
        self._logger.debug("sample form requested")
        self._prepare_to_run(app, interaction)

        form_data = yaml.safe_load(FORM)
        form = dict_to_form(form_data["form"])
        interaction.ui.show_form(form)
        as_dict = form_to_dict(form)
        self._logger.debug("form response: %s", as_dict)

        while True:
            self._calling_app.update()
            next_interaction: Interaction = interaction.ui.show(obj=as_dict)
            if next_interaction.name != "refresh":
                break

        self._prepare_to_exit(interaction)
        return next_interaction
