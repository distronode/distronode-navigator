# distronode-navigator subcommands

{!.generated/subcommands-overview.md!}

## Mapping distronode-navigator commands to distronode commands

Some distronode-navigator commands map to distronode commands. The list below provides
some examples.

### `distronode`

Use `distronode-navigator exec -- distronode` from shell. The exec subcommand requires
execution environment support.

### `ansible-builder`

Use `distronode-navigator builder` from shell.`ansible-builder` is installed with
`distronode-navigator`

### `distronode-config`

Use `distronode-navigator config` from shell, or `:config` from the
`distronode-navigator` prompt.

### `distronode-doc`

Use `distronode-navigator doc` from shell, or `:doc` from the `distronode-navigator`
prompt.

### `distronode-inventory`

Use `distronode-navigator inventory` from shell, or `:inventory` from the
`distronode-navigator` prompt.

### `distronode-galaxy`

Use `distronode-navigator exec -- distronode-galaxy ...` from shell. The exec
subcommand requires execution environment support.

### `ansible-lint`

Use `distronode-navigator lint` from shell, or `:lint` from the `distronode-navigator`
prompt. `ansible-lint` needs to be installed locally or in the selected
execution-environment.

### `distronode-playbook`

Use `distronode-navigator run` from shell or `:run` from the `distronode-navigator`
prompt.

### `distronode-test`

Use `distronode-navigator exec -- distronode-test ...` from shell. The `exec`
subcommand requires execution environment support.

### `distronode-vault`

Use `distronode-navigator exec -- distronode-vault ...` from shell. The `exec`
subcommand requires execution environment support.
