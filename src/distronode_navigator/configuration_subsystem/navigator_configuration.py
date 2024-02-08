"""The distronode-navigator configuration."""

from __future__ import annotations

import logging
import os

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

from distronode_navigator.utils.definitions import ExitMessage
from distronode_navigator.utils.definitions import LogMessage
from distronode_navigator.utils.functions import abs_user_path
from distronode_navigator.utils.functions import generate_cache_path
from distronode_navigator.utils.functions import oxfordcomma
from distronode_navigator.utils.key_value_store import KeyValueStore
from distronode_navigator.utils.packaged_data import ImageEntry

from .definitions import ApplicationConfiguration
from .definitions import CliParameters
from .definitions import Constants as C
from .definitions import SettingsEntry
from .definitions import SettingsEntryValue
from .definitions import SubCommand
from .navigator_post_processor import NavigatorPostProcessor
from .utils import DistronodeConfiguration


APP_NAME = "distronode_navigator"

initialization_messages: list[LogMessage] = []
initialization_exit_messages: list[ExitMessage] = []

PLUGIN_TYPES = (
    "become",
    "cache",
    "callback",
    "cliconf",
    "connection",
    "filter",
    "httpapi",
    "inventory",
    "keyword",
    "lookup",
    "module",
    "netconf",
    "role",
    "shell",
    "strategy",
    "test",
    "vars",
)


def generate_editor_command() -> str:
    """Generate a default for editor_command if EDITOR is set.

    :returns: command to be run by specific editor
    """
    editor = os.environ.get("EDITOR")
    if editor is None:
        message = "EDITOR environment variable not set"
        initialization_messages.append(LogMessage(level=logging.DEBUG, message=message))
        command = "vi +{line_number} {filename}"
    else:
        message = f"EDITOR environment variable set as '{editor}'"
        initialization_messages.append(LogMessage(level=logging.DEBUG, message=message))
        command = f"{editor!s} {{filename}}"
    message = f"Default editor_command set to: {command}"
    initialization_messages.append(LogMessage(level=logging.DEBUG, message=message))
    return command


def _generate_doc_cache_path() -> str:
    """Generate a path for the collection cache.

    :returns: Collection cache path
    """
    file_name = "collection_doc_cache.db"
    cache_dir = generate_cache_path(APP_NAME.replace("_", "-"))
    cache_path = cache_dir / file_name
    message = f"Default collection_doc_cache_path set to: {cache_path}"
    initialization_messages.append(LogMessage(level=logging.DEBUG, message=message))
    return str(cache_path)


@dataclass
class Internals:
    """Place to hold an object that needs to be used from app initiation through whole app."""

    distronode_configuration: DistronodeConfiguration = field(default_factory=DistronodeConfiguration)
    action_packages: tuple[str] = ("distronode_navigator.actions",)
    cache_path: Path = generate_cache_path(APP_NAME.replace("_", "-"))
    collection_doc_cache: C | KeyValueStore = C.NOT_SET
    initializing: bool = False
    """This is an initial run (app starting for the first time)."""
    initialization_exit_messages = initialization_exit_messages
    initialization_messages = initialization_messages
    settings_file_path: str | None = None
    settings_source: C = C.NOT_SET


navigator_subcommands = [
    SubCommand(
        name="builder",
        description=(
            "Build [execution environment]"
            "(https://distronode.readthedocs.io/en/latest/getting_started_ee/index.html) "
            "(container image)"
        ),
        epilog=(
            "Note: 'distronode-navigator builder' additionally supports"
            " the same parameters as the 'distronode-builder' command."
            " For more information about these, try "
            " 'distronode-navigator builder --help-builder --mode stdout'"
        ),
        version_added="v2.0",
    ),
    SubCommand(
        name="collections",
        description="Explore available collections",
        version_added="v1.0",
    ),
    SubCommand(
        name="config",
        description="Explore the current distronode configuration",
        epilog=(
            "Note: With '--mode stdout', 'distronode-navigator config' additionally supports"
            " the same parameters as the 'distronode-config' command."
            " For more information about these, try "
            " 'distronode-navigator config --help-config --mode stdout'"
        ),
        version_added="v1.0",
    ),
    SubCommand(
        name="doc",
        description="Review documentation for a module or plugin",
        epilog=(
            "Note: With '--mode stdout', 'distronode-navigator doc' additionally supports"
            " the same parameters as the 'distronode-doc' command."
            " For more information about these, try "
            " 'distronode-navigator doc --help-doc --mode stdout'"
        ),
        version_added="v1.0",
    ),
    SubCommand(
        name="exec",
        description="Run a command within an execution environment",
        epilog=(
            "Note: During development, it may become necessary to interact"
            " directly with the execution environment to review and confirm"
            " its build and behavior. All navigator settings will be applied"
            " when starting the execution environment."
        ),
        version_added="v2.0",
    ),
    SubCommand(
        name="images",
        description="Explore execution environment images",
        version_added="v1.0",
    ),
    SubCommand(
        name="inventory",
        description="Explore an inventory",
        epilog=(
            "Note: With '--mode stdout', 'distronode-navigator inventory' additionally supports"
            " the same parameters as the 'distronode-inventory' command."
            " For more information about these, try "
            " 'distronode-navigator inventory --help-inventory --mode stdout'"
        ),
        version_added="v1.0",
    ),
    SubCommand(
        name="lint",
        description="Lint a file or directory for common errors and issues",
        epilog=(
            "Note: Defaults to the current working directory."
            " If using an execution environment, distronode-lint must be installed"
            " in it. If not using an execution environment, distronode-lint must"
            " be installed on your system."
        ),
        version_added="v2.0",
    ),
    SubCommand(
        name="replay",
        description="Explore a previous run using a playbook artifact",
        version_added="v1.0",
    ),
    SubCommand(
        name="run",
        description="Run a playbook",
        epilog=(
            "Note: 'distronode-navigator run' additionally supports"
            " the same parameters as the 'distronode-playbook' command."
            " For more information about these, try "
            " 'distronode-navigator run --help-playbook --mode stdout'"
        ),
        version_added="v1.0",
    ),
    SubCommand(
        name="settings",
        description="Review the current distronode-navigator settings",
        version_added="v2.0",
    ),
    SubCommand(
        name="welcome",
        description="Start at the welcome page",
        version_added="v1.0",
    ),
]

NavigatorConfiguration = ApplicationConfiguration(
    application_name=APP_NAME,
    application_version=C.NOT_SET,
    internals=Internals(),
    post_processor=NavigatorPostProcessor(),
    subcommands=navigator_subcommands,
    entries=[
        SettingsEntry(
            name="distronode_runner_artifact_dir",
            cli_parameters=CliParameters(short="--rad"),
            settings_file_path_override="distronode-runner.artifact-dir",
            short_description="The directory path to store artifacts generated by distronode-runner",
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="distronode_runner_rotate_artifacts_count",
            cli_parameters=CliParameters(short="--rac"),
            settings_file_path_override="distronode-runner.rotate-artifacts-count",
            short_description="Keep distronode-runner artifact directories, "
            "for last n runs, if set to 0 artifact directories "
            "won't be deleted",
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="distronode_runner_timeout",
            cli_parameters=CliParameters(short="--rt"),
            settings_file_path_override="distronode-runner.timeout",
            short_description=(
                "The timeout value after which distronode-runner will forcefully stop the execution"
            ),
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="distronode_runner_write_job_events",
            choices=[True, False],
            cli_parameters=CliParameters(short="--rwje", action="store_true"),
            settings_file_path_override="distronode-runner.job-events",
            short_description="Write distronode-runner job_events in the artifact directory",
            value=SettingsEntryValue(default=False),
            version_added="v2.3",
        ),
        SettingsEntry(
            name="app",
            apply_to_subsequent_cli=C.NONE,
            choices=[subcommand.name for subcommand in navigator_subcommands],
            short_description="Subcommands",
            subcommand_value=True,
            value=SettingsEntryValue(default="welcome"),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="cmdline",
            apply_to_subsequent_cli=C.SAME_SUBCOMMAND,
            settings_file_path_override="distronode.cmdline",
            short_description="Extra parameters passed to the underlying distronode command"
            " (e.g. distronode-playbook, distronode-doc, etc)",
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="collection_doc_cache_path",
            cli_parameters=CliParameters(short="--cdcp"),
            short_description="The path to collection doc cache",
            value=SettingsEntryValue(
                default=_generate_doc_cache_path(),
                schema_default="~/.cache/distronode-navigator/collection_doc_cache.db",
            ),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="config",
            cli_parameters=CliParameters(short="-c"),
            environment_variable_override="distronode_config",
            settings_file_path_override="distronode.config.path",
            short_description="Specify the path to the distronode configuration file",
            subcommands=["config"],
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="container_engine",
            choices=["auto", "podman", "docker"],
            cli_parameters=CliParameters(short="--ce"),
            settings_file_path_override="execution-environment.container-engine",
            short_description="Specify the container engine (auto=podman then docker)",
            value=SettingsEntryValue(default="auto"),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="container_options",
            cli_parameters=CliParameters(action="append", nargs="+", short="--co"),
            environment_variable_override="distronode_navigator_container_options",
            settings_file_path_override="execution-environment.container-options",
            short_description="Extra parameters passed to the container engine command",
            value=SettingsEntryValue(),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="display_color",
            change_after_initial=False,
            choices=[True, False],
            cli_parameters=CliParameters(short="--dc"),
            environment_variable_override="no_color",
            settings_file_path_override="color.enable",
            short_description="Enable the use of color for mode interactive and stdout",
            value=SettingsEntryValue(default=True),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="editor_command",
            cli_parameters=CliParameters(short="--ecmd"),
            settings_file_path_override="editor.command",
            short_description="Specify the editor command",
            value=SettingsEntryValue(
                default=generate_editor_command(),
                schema_default="vi +{line_number} {filename}",
            ),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="editor_console",
            choices=[True, False],
            cli_parameters=CliParameters(short="--econ"),
            settings_file_path_override="editor.console",
            short_description="Specify if the editor is console based",
            value=SettingsEntryValue(default=True),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="enable_prompts",
            choices=[True, False],
            cli_parameters=CliParameters(short="--ep", action="store_true"),
            short_description="Enable prompts for password and in playbooks. This will set"
            " mode to stdout and disable playbook artifact creation",
            subcommands=["run"],
            value=SettingsEntryValue(default=False),
            version_added="v2.3",
        ),
        SettingsEntry(
            name="exec_command",
            cli_parameters=CliParameters(positional=True),
            settings_file_path_override="exec.command",
            short_description="Specify the command to run within the execution environment",
            subcommands=["exec"],
            value=SettingsEntryValue(default="/bin/bash"),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="exec_shell",
            choices=[True, False],
            cli_parameters=CliParameters(short="--exshell"),
            settings_file_path_override="exec.shell",
            short_description="Specify the exec command should be run in a shell",
            subcommands=["exec"],
            value=SettingsEntryValue(default=True),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="execution_environment",
            choices=[True, False],
            cli_parameters=CliParameters(short="--ee"),
            settings_file_path_override="execution-environment.enabled",
            short_description="Enable or disable the use of an execution environment",
            value=SettingsEntryValue(default=True),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="execution_environment_image",
            cli_parameters=CliParameters(short="--eei"),
            settings_file_path_override="execution-environment.image",
            short_description="Specify the name of the execution environment image",
            value=SettingsEntryValue(
                default=ImageEntry.DEFAULT_EE.get(app_name=APP_NAME),
                schema_default=C.NONE,
            ),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="execution_environment_volume_mounts",
            cli_parameters=CliParameters(action="append", nargs="+", short="--eev"),
            delay_post_process=True,
            environment_variable_split_char=";",
            settings_file_path_override="execution-environment.volume-mounts",
            short_description=(
                "Specify volume to be bind mounted within an execution environment"
                " (--eev /home/user/test:/home/user/test:Z)"
            ),
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="format",
            choices=["json", "yaml"],
            cli_parameters=CliParameters(short="--fmt"),
            short_description="Specify the format for stdout output.",
            subcommands=["collections", "images"],
            value=SettingsEntryValue(default="yaml"),
            version_added="v2.3",
        ),
        SettingsEntry(
            name="help_builder",
            choices=[True, False],
            cli_parameters=CliParameters(short="--hb", action="store_true"),
            settings_file_path_override="distronode-builder.help",
            short_description="Help options for distronode-builder command in stdout mode",
            subcommands=["builder"],
            value=SettingsEntryValue(default=False),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="help_config",
            choices=[True, False],
            cli_parameters=CliParameters(short="--hc", action="store_true"),
            settings_file_path_override="distronode.config.help",
            short_description="Help options for distronode-config command in stdout mode",
            subcommands=["config"],
            value=SettingsEntryValue(default=False),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="help_doc",
            choices=[True, False],
            cli_parameters=CliParameters(short="--hd", action="store_true"),
            settings_file_path_override="distronode.doc.help",
            short_description="Help options for distronode-doc command in stdout mode",
            subcommands=["doc"],
            value=SettingsEntryValue(default=False),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="help_inventory",
            choices=[True, False],
            cli_parameters=CliParameters(short="--hi", action="store_true"),
            settings_file_path_override="distronode.inventory.help",
            short_description="Help options for distronode-inventory command in stdout mode",
            subcommands=["inventory"],
            value=SettingsEntryValue(default=False),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="help_playbook",
            choices=[True, False],
            cli_parameters=CliParameters(short="--hp", action="store_true"),
            settings_file_path_override="distronode.playbook.help",
            short_description="Help options for distronode-playbook command in stdout mode",
            subcommands=["run"],
            value=SettingsEntryValue(default=False),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="images_details",
            choices=[
                "distronode_collections",
                "distronode_version",
                "everything",
                "os_release",
                "python_packages",
                "python_version",
                "redhat_release",
                "system_packages",
            ],
            cli_parameters=CliParameters(
                action="append",
                nargs="*",
                short="-d",
                long_override="--details",
            ),
            settings_file_path_override="images.details",
            short_description=(
                "Provide detailed information about the selected execution environment image"
            ),
            subcommands=["images"],
            value=SettingsEntryValue(default=["everything"]),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="inventory",
            cli_parameters=CliParameters(action="append", nargs="*", short="-i"),
            environment_variable_override="distronode_inventory",
            settings_file_path_override="distronode.inventory.entries",
            short_description="Specify an inventory file path or comma separated host list",
            subcommands=["inventory", "run"],
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="inventory_column",
            cli_parameters=CliParameters(action="append", nargs="+", short="--ic"),
            environment_variable_override="distronode_navigator_inventory_columns",
            settings_file_path_override="inventory-columns",
            short_description="Specify a host attribute to show in the inventory view",
            subcommands=["inventory", "run"],
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="lint_config",
            cli_parameters=CliParameters(short="--lic"),
            environment_variable_override="distronode_lint_config",
            settings_file_path_override="distronode-lint.config",
            short_description="Specify the path to the distronode-lint configuration file",
            subcommands=["lint"],
            value=SettingsEntryValue(),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="lintables",
            cli_parameters=CliParameters(positional=True),
            short_description="Path to files on which to run distronode-lint",
            settings_file_path_override="distronode-lint.lintables",
            subcommands=["lint"],
            value=SettingsEntryValue(),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="log_append",
            choices=[True, False],
            cli_parameters=CliParameters(short="--la"),
            short_description=(
                "Specify if log messages should be appended to an existing log file,"
                " otherwise a new log file will be created per session"
            ),
            settings_file_path_override="logging.append",
            value=SettingsEntryValue(default=True),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="log_file",
            cli_parameters=CliParameters(short="--lf"),
            short_description="Specify the full path for the distronode-navigator log file",
            settings_file_path_override="logging.file",
            value=SettingsEntryValue(
                default=abs_user_path("./distronode-navigator.log"),
                schema_default="./distronode-navigator.log",
            ),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="log_level",
            choices=["debug", "info", "warning", "error", "critical"],
            cli_parameters=CliParameters(short="--ll"),
            short_description="Specify the distronode-navigator log level",
            settings_file_path_override="logging.level",
            value=SettingsEntryValue(default="warning"),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="mode",
            change_after_initial=False,
            delay_post_process=True,
            choices=["stdout", "interactive"],
            cli_parameters=CliParameters(short="-m"),
            short_description="Specify the user-interface mode",
            value=SettingsEntryValue(default="interactive"),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="osc4",
            choices=[True, False],
            cli_parameters=CliParameters(short="--osc4"),
            settings_file_path_override="color.osc4",
            short_description="Enable or disable terminal color changing support with OSC 4",
            value=SettingsEntryValue(default=True),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="pass_environment_variable",
            cli_parameters=CliParameters(action="append", nargs="+", short="--penv"),
            environment_variable_override="distronode_navigator_pass_environment_variables",
            settings_file_path_override="execution-environment.environment-variables.pass",
            short_description=(
                "Specify an existing environment variable to be passed through"
                " to and set within the execution environment (--penv MY_VAR)"
            ),
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="playbook",
            cli_parameters=CliParameters(positional=True),
            short_description="Specify the playbook name",
            settings_file_path_override="distronode.playbook.path",
            subcommands=["run"],
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="playbook_artifact_enable",
            choices=[True, False],
            cli_parameters=CliParameters(short="--pae"),
            delay_post_process=True,
            settings_file_path_override="playbook-artifact.enable",
            short_description="Enable or disable the creation of artifacts for"
            " completed playbooks. Note: not compatible with '--mode stdout' when playbooks"
            " require user input",
            subcommands=["run"],
            value=SettingsEntryValue(default=True),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="playbook_artifact_replay",
            cli_parameters=CliParameters(positional=True),
            settings_file_path_override="playbook-artifact.replay",
            short_description="Specify the path for the playbook artifact to replay",
            subcommands=["replay"],
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="playbook_artifact_save_as",
            cli_parameters=CliParameters(short="--pas"),
            settings_file_path_override="playbook-artifact.save-as",
            short_description=(
                "Specify the name for artifacts created from completed playbooks."
                " The following placeholders are available: {playbook_dir}, {playbook_name},"
                " {playbook_status}, and {time_stamp}"
            ),
            subcommands=["run"],
            value=SettingsEntryValue(
                default="{playbook_dir}/{playbook_name}-artifact-{time_stamp}.json",
            ),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="plugin_name",
            cli_parameters=CliParameters(positional=True),
            settings_file_path_override="distronode.doc.plugin.name",
            short_description="Specify the plugin name",
            subcommands=["doc"],
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="plugin_type",
            choices=PLUGIN_TYPES,
            cli_parameters=CliParameters(short="-t", long_override="--type"),
            settings_file_path_override="distronode.doc.plugin.type",
            short_description=f"Specify the plugin type, {oxfordcomma(PLUGIN_TYPES, 'or')}",
            subcommands=["doc"],
            value=SettingsEntryValue(default="module"),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="pull_arguments",
            cli_parameters=CliParameters(action="append", nargs="+", short="--pa"),
            settings_file_path_override="execution-environment.pull.arguments",
            short_description=(
                "Specify any additional parameters that should be added to the"
                " pull command when pulling an execution environment from a container"
                " registry. e.g. --pa='--tls-verify=false'"
            ),
            value=SettingsEntryValue(),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="pull_policy",
            choices=["always", "missing", "never", "tag"],
            cli_parameters=CliParameters(short="--pp"),
            settings_file_path_override="execution-environment.pull.policy",
            short_description=(
                "Specify the image pull policy"
                " always:Always pull the image,"
                " missing:Pull if not locally available,"
                " never:Never pull the image,"
                " tag:if the image tag is 'latest', always pull the image,"
                " otherwise pull if not locally available"
            ),
            value=SettingsEntryValue(default="tag"),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="set_environment_variable",
            cli_parameters=CliParameters(action="append", nargs="+", short="--senv"),
            environment_variable_override="distronode_navigator_set_environment_variables",
            settings_file_path_override="execution-environment.environment-variables.set",
            short_description=(
                "Specify an environment variable and a value to be set within the"
                " execution environment (--senv MY_VAR=42)"
            ),
            value=SettingsEntryValue(),
            version_added="v1.0",
        ),
        SettingsEntry(
            name="settings_effective",
            cli_parameters=CliParameters(
                short="--se",
                long_override="--effective",
                action="store_true",
            ),
            settings_file_path_override="settings.effective",
            short_description=(
                "Show the effective settings. Defaults, CLI parameters, environment variables,"
                " and the settings file will be combined"
            ),
            subcommands=["settings"],
            value=SettingsEntryValue(default=False),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="settings_sample",
            cli_parameters=CliParameters(
                short="--gs",
                long_override="--sample",
                action="store_true",
            ),
            settings_file_path_override="settings.sample",
            short_description=("Generate a sample settings file"),
            subcommands=["settings"],
            value=SettingsEntryValue(default=False),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="settings_schema",
            choices=["json"],
            cli_parameters=CliParameters(
                short="--ss",
                long_override="--schema",
                const="json",
                nargs="?",
            ),
            settings_file_path_override="settings.schema",
            short_description=(
                "Generate a schema for the settings file ('json'= draft-07 JSON Schema)"
            ),
            subcommands=["settings"],
            value=SettingsEntryValue(default="json"),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="settings_sources",
            cli_parameters=CliParameters(
                short="--so",
                long_override="--sources",
                action="store_true",
            ),
            settings_file_path_override="settings.sources",
            short_description=("Show the source of each current settings entry"),
            subcommands=["settings"],
            value=SettingsEntryValue(default=False),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="time_zone",
            cli_parameters=CliParameters(short="--tz"),
            environment_variable_override="TZ",
            short_description=(
                "Specify the IANA time zone to use or 'local' to use the system time zone"
            ),
            value=SettingsEntryValue(default="UTC"),
            version_added="v2.0",
        ),
        SettingsEntry(
            name="workdir",
            cli_parameters=CliParameters(short="--bwd"),
            settings_file_path_override="distronode-builder.workdir",
            short_description="Specify the path that contains distronode-builder manifest files",
            subcommands=["builder"],
            value=SettingsEntryValue(
                default=os.getcwd(),
                schema_default=".",
            ),
            version_added="v2.0",
        ),
    ],
)
