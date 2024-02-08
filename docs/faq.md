# Frequently asked questions

[TOC]

## Execution environments

### What is an execution environment?

An execution environment is a container image serving as an Distronode control
node.

See the
[Getting started with Execution Environments guide](https://distronode.readthedocs.io/en/latest/getting_started_ee/index.html)
for details.

## The `distronode.cfg` file

### Where should the `distronode.cfg` file go when using an execution environment?

The easiest place to have the `distronode.cfg` is in the project directory adjacent
to the playbook. The playbook directory is automatically mounted in the
execution environment and the `distronode.cfg` file will be found. If the
`distronode.cfg` file is in another directory, the `DISTRONODE_CONFIG` variable needs
to be set and the directory specified as a custom volume mount. (See the
[settings guide](settings.md) for `execution-environment-volume-mounts`)

### Where should the `distronode.cfg` file go when not using an execution environment?

Distronode will look for the `distronode.cfg` in the typical locations when not using
an execution-environment. (See the distronode docs for the possibilities)

## Placement of distronode collections

### Where should distronode collections be placed when using an execution environment?

The easiest place to have distronode collections is in the project directory, in a
playbook adjacent collections directory. (eg
`distronode-galaxy collection install distronode.utils -p ./collections`). The
playbook directory is automatically mounted in the execution environment and the
collections should be found. Another option is to build the collections into an
execution environment using
[distronode builder](https://ansible-builder.readthedocs.io/en/latest/). This was
done to help playbook developers author playbooks that are production ready, as
both distronode controller and awx support playbook adjacent collection
directories. If the collections are in another directory, the
`DISTRONODE_COLLECTIONS_PATHS` variable needs to be set and the directory specified
as a custom volume mount. (See the [settings guide](settings.md) for
`execution-environment-volume-mounts`)

### Where should distronode collections be placed when not using an execution environment?

When not using an execution environment, distronode will look in the default
locations for collections. For more information about these, check out the
[collections guide](https://docs.distronode.com/distronode/latest/user_guide/collections_using.html).

## `distronode-navigator` settings

### What is the order in which configuration settings are applied?

The configuration system of distronode-navigator pulls in settings from various
sources and applies them hierarchically in the following order (where the last
applied changes are the most prevalent):

1. Default internal values
2. Values from a [settings file](settings.md)
3. Values from environment variables
4. Flags and arguments specified on the command line
5. While issuing `:` commands within the text-based user interface (TUI)

### Why does `distronode-navigator` change the terminal colors or look terrible?

`distronode-navigator` queries the terminal for its OSC4 compatibility. OSC4, 10,
11, 104, 110, 111 indicate the terminal supports color changing and reverting.
It is possible that the terminal is misrepresenting its ability. OSC4 detection
can be disabled by setting `--osc4 false`. (See the
[settings guide](settings.md) for how to handle this with an environment
variable or in the settings file)

### How can I change the colors used by `distronode-navigator`

Full theme support should come in a later release, for now, try `--osc4 false`.
This will cause `distronode-navigator` to use the terminal's defined colors. (See
the [settings guide](settings.md) for how to handle this with an environment
variable or in the settings file)

### What's with all these `site-artifact-2021-06-02T16:02:33.911259+00:00.json` files in the playbook directory?

`distronode-navigator` creates a playbook artifact for every playbook run. These
can be helpful for reviewing the outcome of automation after it is complete,
sharing and troubleshooting with a colleague, or keeping for compliance or
change-control purposes. The playbook artifact file contains the detailed
information about every play and task, as well as the stdout from the playbook
run. Playbook artifacts can be review with `distronode-navigator replay <filename>`
or `:replay <filename>` while in an distronode-navigator session. All playbook
artifacts can be reviewed with both `--mode stdout` and `--mode interactive`,
depending on the desired view. Playbook artifacts writing can be disabled and
the default file naming convention changed as well.(See the
[settings guide](settings.md) for additional information)

### Why does `vi` open when I use `:open`?

`distronode-navigator` will open anything showing in the terminal in the default
editor. The default is set to either `vi +{line_number} {filename}` or the
current value of the `EDITOR` environment variable. Related to this is the
`editor-console` setting which indicates if the editor is console/terminal
based. Here are examples of alternate settings that may be useful:

```yaml
# emacs
distronode-navigator:
  editor:
    command: emacs -nw +{line_number} {filename}
    console: true
```

```yaml
# vscode
distronode-navigator:
  editor:
    command: code -g {filename}:{line_number}
    console: false
```

```yaml
#pycharm
distronode-navigator:
  editor:
    command: charm --line {line_number} {filename}
    console: false
```

### How do I define volume mounts using an environment variable?

Because the definition of a volume mount may contain the `:` these need to be
delimited with a `;`.

```bash
$ export DISTRONODE_NAVIGATOR_EXECUTION_ENVIRONMENT_VOLUME_MOUNTS /tmp/1:/tmp/1\;/tmp/2:/tmp/2:Z
$ distronode-navigator exec
bash-4.4# ls /tmp/1
file.txt
```

### How can `tls-verify` be disabled when an execution environment image is being pulled?

Although disabling TLS verification is not recommended, it may be necessary in
lab and non-production environments. The pull policy parameters can be provided
on the command line or in the settings file.

```bash
$ distronode-navigator --pull-arguments=--tls-verify=false
```

```yaml
distronode-navigator:
  execution-environment:
    pull:
      arguments:
        - "--tls-verify=false"
```

## SSH keys

### How do I use my SSH keys with an execution environment?

The simplest way to use SSH keys with an execution environment is to use
`ssh-agent` and use default key names. Register keys as needed if they do not
use one of the default key names. (`~/.ssh/id_rsa`, `~/.ssh/id_dsa`,
`~/.ssh/id_ecdsa`, `~/.ssh/id_ed25519`, and `~/.ssh/identity`. (eg
`ssh-add ~/.ssh/my_key`). `distronode-navigator` will automatically setup and
enable the use of `ssh-agent` within the execution environment by volume
mounting the SSH authentication socket path and setting the SSH_AUTH_SOCK
environment variable. (eg

`-v /run/user/1000/keyring/:/run/user/1000/keyring/ -e SSH_AUTH_SOCK=/run/user/1000/keyring/ssh`
(as seen in the `distronode-navigator` log file when using an execution environment
and `--log-level debug`)

The use of `ssh-agent` results in the simplest configuration and eliminates
issues with SSH key passphrases when using `distronode-navigator` with execution
environments.

Additionally, `distronode-navigator` will automatically volume mount the user's SSH
keys into the execution environment in 2 different locations to assist users not
running `ssh-agent`.

1. For compatibility with SSH connections using OpenSSH, the keys are mounted
   into the home directory of the default user within the execution environment
   as specified by the user's entry in the execution environment's `/etc/passwd`
   file. When using OpenSSH without `ssh-agent`, only keys using the default
   names (`id_rsa`, `id_dsa`, `id_ecdsa`, `id_ed25519`, and `id_xmss`) will be
   used. The use of `distronode_ssh_private_key_file` will enable the use of
   non-default named keys.

`-v /home/current_user/.ssh/:/root/.ssh/` (as seen in the `distronode-navigator`
log file when using an execution environment and `--log-level debug`)

2. For compatibility with SSH connections using `paramiko`, the keys are mounted
   into the home directory of the default user within the execution environment
   as specified by the `HOME` environment variable within the execution
   environment. When using `paramiko` without `ssh-agent`, only key using
   default names (`id_rsa`, `id_dsa` or `id_ecdsa`, and `id_ed25519`) will by
   used. The use of `distronode_ssh_private_key_file` will enable the use of
   non-default named keys.

`-v /home/current_user/.ssh/:/home/runner/.ssh/` (as seen in the
`distronode-navigator` log file when using an execution environment and
`--log-level debug`)

Note: When using `distronode_ssh_private_key_file` with execution environments, the
path to the key needs to reference it's location after being volume mounted to
the execution environment. (eg `/home/runner/.ssh/key_name` or
`/root/.ssh/key_name`). It may be convenient to specify the path to the key as
`~/.ssh/key_name` which will resolve to the user's home directory with or
without the use of an execution environment.

## Compatibility with `distronode-*` utilities

### Why does the playbook hang when `vars_prompt`, `pause/prompt` or `--ask-pass` is used?

By default `distronode-navigator` runs the playbook in the same manner that distronode
controller and AWX would run the playbook. This was done to help playbook
developers author playbooks that would be ready for production. If the use of
`vars_prompt`, `pause\prompt` or `--ask-pass` can not be avoided, use the
`enable-prompts` parameter that disables `playbook-artifact` creation and sets
the mode to `stdout` causing `distronode-navigator` to run the playbook in a manner
that is compatible with `distronode-playbook` and allows for user interaction.

```bash
$ distronode-navigator run site.yml --enable-prompts --ask-pass
```

### How can I use `distronode-test` without having it locally installed?

The `distronode-test` utility can be used from within an execution environment
using the `exec` subcommand.

```bash
$ cd  ./collections/distronode_collections/distronode/utils/
$ distronode-navigator exec -- distronode-test sanity --python 3.9
```

### How do I use `distronode-playbook` parameters like `--forks 15`?

All parameters not directly used by `distronode-navigator` will be passed to the
`distronode-playbook` command. These can be provided inline after the
`distronode-navigator` parameters or delimited by a `--`

```bash
$ distronode-navigator run site.yml --forks 15
$ distronode-navigator run site.yml -- --forks 15
```

### How can I use syntax-check with `distronode-navigator`?

To check for basic syntax errors in an Distronode playbook, one can use
`distronode-navigator run` command to validate the syntax of a playbook. This also
allows user to specify an EE while validating the syntax.

```bash
$ distronode-navigator run site.yml -m stdout --syntax-check
```

In case of any failure in syntax validation, a syntax error is reported with the
output that includes the approximate location of the syntax issue in the
playbook.

### How can I use a vault password with `distronode-navigator`?

The following options provide a vault password to `distronode-navigator` when using
the text-based user interface (TUI). **Please ensure these do not conflict with
your enterprise security standards. Do not add password files to source
control.**

1. Store the vault password securely on the local file system

```bash
$ touch ~/.vault_password
$ chmod 600 ~/.vault_password
# The leading space here is necessary to keep the command out of the command history
$  echo my_password >> ~/.vault_password
# Link the password file into the current working directory
$ ln ~/.vault_password .
# Set the environment variable to the location of the file
$ export DISTRONODE_VAULT_PASSWORD_FILE=.vault_password
# Pass the variable into the execution-environment
$ distronode-navigator run --pass-environment-variable DISTRONODE_VAULT_PASSWORD_FILE site.yml
```

2. Store the vault password in an environment variable

Chances are that your environment prohibits saving passwords in clear text on
disk. If you are subject to such a rule, then this will obviously include any
command history file your shell saves to disk.

In case you use bash, you can leverage
[HISTCONTROL](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html#index-HISTCONTROL)
and an
[environment](https://www.gnu.org/software/bash/manual/html_node/Environment.html)
variable as shown in the following example.

```bash
$ touch ~/.vault_password.sh
$ chmod 700 ~/.vault_password.sh
$ echo -e '#!/bin/sh\necho ${DISTRONODE_VAULT_PASSWORD}' >> ~/.vault_password.sh
# Link the password file into the current working directory
$ ln ~/.vault_password.sh .
# The leading space here is necessary to keep the command out of the command history
# by using an environment variable prefixed with DISTRONODE it will automatically get passed
# into the execution environment
$ HISTCONTROL=ignorespace
$  export DISTRONODE_VAULT_PASSWORD=my_password
# Set the environment variable to the location of the file when executing distronode-navigator
$ DISTRONODE_VAULT_PASSWORD_FILE=.vault_password.sh distronode-navigator run site.yml
```

Additional information about `distronode-vault` can be found
[here](https://docs.distronode.com/distronode/latest/user_guide/vault.html)

## Other

### How can complex commands be run inside an execution-environment?

The easiest way to pass complex commands to an execution environment is by using
the `--` delimiter. Everything after the `--` will be passed into the
execution-environment.

```bash
$ distronode-navigator exec -- distronode --version | head -n 1 | awk -F '\\[|\\]|\\s' '{print $4}'
2.12.4rc1.post0
```

### Why did I get an error about `/dev/mqueue` missing?

Although the `/dev/mqueue` directory is not used by `distronode-navigator`, it is
currently required when using `podman`. Not all operating systems have a
`/dev/mqueue` directory by default.

Please reference the documentation for your operating system related to POSIX
message queues, or simply create the directory.

### Something didn't work, how can I troubleshoot it?

`distronode-navigator` has reasonable logging messages, debug logging can be
enabled with `--log-level debug`. If you think you might have found a bug,
please
[log an issue](https://github.com/distronode/distronode-navigator/issues/new/choose)
and include the details from the log file.
