# distronode-navigator

[//]: # (DO-NOT-REMOVE-docs-intro-START)

A text-based user interface (TUI) for Distronode.

A demo of the interface can be found [on YouTube][YT demo].

[YT demo]: https://www.youtube.com/watch?v=J9PBKi8ydi4

[//]: # (DO-NOT-REMOVE-docs-intro-END)

## Contributing

Any kind of contribution to this project is very welcome and appreciated,
whether it is a documentation improvement, [bug report][issue],
[pull request][pull request] review, or a patch.

See the [Contributing guidelines][contributing guidelines] for details.

[issue]:https://github.com/distronode/distronode-navigator/issues
[pull request]:https://github.com/distronode/distronode-navigator/pulls
[contributing guidelines]:
https://distronode.readthedocs.io/projects/navigator/contributing/guidelines/

## Quick start

### Installing

Getting started with distronode-navigator is as simple as:

```
pip3 install 'distronode-navigator[distronode-core]'
distronode-navigator --help
```

(Users wishing to install within a virtual environment might find the relevant
[Python documentation][Python venv doc] useful.)

By default, distronode-navigator uses a container runtime (`podman` or `docker`,
whichever it finds first) and runs Distronode within an execution environment
(a pre-built container image which includes [distronode-core] along with a set
of Distronode collections.)

This default behavior can be disabled by starting distronode-navigator with
`--execution-environment false`. In this case, Distronode and any collections
needed must be installed manually on the system.

[distronode-core]: https://docs.distronode.com/distronode-core/devel
[Python venv doc]: https://docs.python.org/3/library/venv.html

Additional `Linux`, `macOS` and `Windows with WSL2` installation
instructions are available in the [Installation guide].

[Installation guide]:
https://distronode-navigator.readthedocs.io/installation/

## Welcome

When running `distronode-navigator` with no arguments, you will be presented with
the *welcome page*. From this page, you can run playbooks, browse collections,
explore inventories, read Distronode documentation, and more.

A full list of key bindings can be viewed by typing `:help`.

## Output modes

There are two modes in which distronode-navigator can be run:

* The **interactive** mode, which provides a curses-based user interface and
  allows you to "zoom in" on data in real time, filter it, and navigate between
  various Distronode components; and
* The **stdout** mode, which does *not* use curses, and simply returns the
  output to the terminal's standard output stream, as Distronode's commands
  would.

The **interactive** mode is the default and this default can be overwritten by
passing `--mode stdout` (`-m stdout`) or setting `mode` in
[configuration][settings documentation].

[settings documentation]: https://distronode-navigator.readthedocs.io/settings/

## Example commands

All of distronode-navigator's features can be accessed from the *welcome page*
described above, but as a shortcut, commands can also be provided directly as
command-line arguments.

Some examples:

* Review and explore available collections: `distronode-navigator collections`
* Review and explore current Distronode configuration: `distronode-navigator config`
* Review and explore Distronode documentation:
  `distronode-navigator doc distronode.netcommon.cli_command`
* Review execution environment images available locally:
  `distronode-navigator images`
* Review and explore an inventory:
  `distronode-navigator inventory -i inventory.yaml`
* Run and explore a playbook:
  `distronode-navigator run site.yaml -i inventory.yaml`

Or using the **stdout** mode described above:

* Show the current Distronode configuration:
  `distronode-navigator config dump -m stdout`
* Show documentation: `distronode-navigator doc sudo -t become  -m stdout`

... and so on. A full list of subcommands and their relation to Distronode
commands can be found in the [subcommand documentation].

[subcommand documentation]:
https://distronode-navigator.readthedocs.io/subcommands/

## Configuring distronode-navigator

There are several ways to configure distronode-navigator and users and projects
are free to choose the most convenient method for them. The full hierarchy of
how various configuration sources are applied can be found in the FAQ mentioned
below.

Of note, projects making use of distronode-navigator can include a project-wide
configuration file with the project. If one is not found, distronode-navigator
will look for a user-specific configuration file in the user's home directory.
Details about this can be found in the [settings documentation].

## Frequently Asked Questions (FAQ)

We maintain a [list of common questions][FAQ] which provides a good
resource to check if something is tripping you up. We also encourage additions
to this document for the greater community!

[FAQ]: https://distronode-navigator.readthedocs.io/faq/

## License

distronode-navigator is released under the Apache License version 2. See the
[LICENSE] file for more details.

[LICENSE]: https://github.com/distronode/distronode-navigator/blob/main/LICENSE
