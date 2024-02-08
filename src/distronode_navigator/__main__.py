"""A runpy entry point for distronode-navigator.

This makes it possible to invoke CLI
via :command:`python -m distronode_navigator`.
"""

from .cli import main


if __name__ == "__main__":
    main()
