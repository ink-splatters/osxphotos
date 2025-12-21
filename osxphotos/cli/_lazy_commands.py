"""Lazy loading command registry for CLI to improve startup time."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import click


# Map of command name -> (module_path, function_name)
# This allows lazy loading of commands only when invoked
COMMAND_REGISTRY = {
    "about": (".about", "about"),
    "albums": (".albums", "albums"),
    "compare": (".compare", "compare"),
    "debug-dump": (".debug_dump", "debug_dump"),
    "diff": (".snap_diff", "diff"),
    "docs": (".docs", "docs_command"),
    "dump": (".dump", "dump"),
    "exiftool": (".exiftool_cli", "exiftool"),
    "export": (".export", "export"),
    "exportdb": (".exportdb", "exportdb"),
    "grep": (".grep", "grep"),
    "help": (".help", "help"),
    "info": (".info", "info"),
    "install": (".install_uninstall_run", "install"),
    "keywords": (".keywords", "keywords"),
    "labels": (".labels", "labels"),
    "libraries": (".list", "list_libraries"),
    "orphans": (".orphans", "orphans"),
    "persons": (".persons", "persons"),
    "places": (".places", "places"),
    "query": (".query", "query"),
    "repl": (".repl", "repl"),
    "run": (".install_uninstall_run", "run"),
    "snap": (".snap_diff", "snap"),
    "theme": (".theme", "theme"),
    "tutorial": (".tutorial", "tutorial"),
    "template": (".template_repl", "template_repl"),
    "uninstall": (".install_uninstall_run", "uninstall"),
    "version": (".version", "version"),
    "update": (".update_command", "update_command"),
}

# macOS-only commands
MACOS_COMMANDS = {
    "add-locations": (".add_locations", "add_locations"),
    "batch-edit": (".batch_edit", "batch_edit"),
    "import": (".import_cli", "import_main"),
    "photo-inspect": (".photo_inspect", "photo_inspect"),
    "push-exif": (".push_exif", "push_exif"),
    "show": (".show_command", "show"),
    "sync": (".sync", "sync"),
    "timewarp": (".timewarp", "timewarp"),
    "uuid": (".uuid", "uuid"),
}


class LazyGroup(click.Group):
    """A Click Group that lazy-loads subcommands."""

    def __init__(self, *args, lazy_commands=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.lazy_commands = lazy_commands or {}

    def list_commands(self, ctx):
        """List all available commands."""
        return sorted(self.lazy_commands.keys())

    def get_command(self, ctx, cmd_name):
        """Lazy load and return the command."""
        # Check if already loaded
        if cmd_name in self.commands:
            return self.commands[cmd_name]

        # Check if it's in our lazy registry
        if cmd_name not in self.lazy_commands:
            return None

        # Invoke disclaim() if this command needs Photos access
        from ._photos_access import command_needs_photos_access
        from osxphotos.disclaim import disclaim, pyapp, pyinstaller
        
        if (pyinstaller() or pyapp()) and command_needs_photos_access(cmd_name):
            disclaim()

        module_path, func_name = self.lazy_commands[cmd_name]
        
        # Import the module and get the command
        try:
            # Import relative to osxphotos.cli
            module = importlib.import_module(module_path, package="osxphotos.cli")
            cmd = getattr(module, func_name)
            
            # Cache it for future use
            self.add_command(cmd, name=cmd_name)
            return cmd
        except (ImportError, AttributeError) as e:
            # If import fails, return None (command not found)
            return None


def create_lazy_cli_group():
    """Create a lazy-loading CLI group with all commands registered."""
    from osxphotos.platform import is_macos
    
    commands = dict(COMMAND_REGISTRY)
    if is_macos:
        commands.update(MACOS_COMMANDS)
    
    return commands

