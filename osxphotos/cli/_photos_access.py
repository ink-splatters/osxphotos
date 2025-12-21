"""Track which CLI commands require Photos library access for selective disclaim()."""

from __future__ import annotations

# Commands that require direct Photos library access and thus need disclaim()
# These commands interact with the Photos database or use PhotoScript
PHOTOS_ACCESS_COMMANDS = {
    "add-locations",
    "albums",
    "batch-edit",
    "dump",
    "export",
    "import",
    "info",
    "keywords",
    "labels",
    "list",  
    "libraries",
    "orphans",
    "persons",
    "photo-inspect",
    "places",
    "push-exif",
    "query",
    "repl",
    "show",
    "snap",
    "diff",  # diff might need access to compare snapshots
    "sync",
    "timewarp",
    "uuid",
}


def command_needs_photos_access(command_name: str) -> bool:
    """Check if a command needs Photos library access."""
    return command_name in PHOTOS_ACCESS_COMMANDS


def invoke_disclaim_if_needed(ctx) -> None:
    """Invoke disclaim() only if the current command needs Photos access."""
    from osxphotos.disclaim import disclaim, pyapp, pyinstaller
    
    if not (pyinstaller() or pyapp()):
        # Not running from executable, no need to disclaim
        return
    
    # Get the command name from context
    if ctx.invoked_subcommand and command_needs_photos_access(ctx.invoked_subcommand):
        disclaim()
    elif hasattr(ctx, 'info_name') and command_needs_photos_access(ctx.info_name):
        disclaim()

