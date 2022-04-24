"""docs command for osxphotos CLI """

import pathlib
import shutil
import zipfile
from typing import Optional

import click

from osxphotos._version import __version__

from .common import get_config_dir


@click.command()
@click.pass_obj
@click.pass_context
def docs(ctx, cli_obj):
    """Open osxphotos documentation in your browser."""

    docs_dir = get_config_dir() / "docs"
    docs_version = get_docs_version(docs_dir)
    if not docs_version or docs_version != __version__:
        click.echo(f"Copying docs for osxphotos version {__version__}")
        shutil.rmtree(str(docs_dir), ignore_errors=True)
        copy_docs()

    cli_docs = docs_dir / "index.html"
    click.echo(f"Opening {cli_docs}")
    click.launch(str(cli_docs))


def get_docs_version(docs_dir: pathlib.Path) -> Optional[str]:
    """Get the version of the docs directory"""

    if not docs_dir.exists():
        return None

    version_file = docs_dir / ".version"
    if not version_file.exists():
        return None

    with version_file.open() as f:
        return f.read().strip()


def copy_docs():
    """Copy the latest docs to the config directory"""
    # there must be a better way to do this
    # docs are in osxphotos/docs and this file is in osxphotos/cli
    src_dir = pathlib.Path(__file__).parent.parent / "docs"
    docs_zip = src_dir / "docs.zip"
    config_dir = get_config_dir()
    with zipfile.ZipFile(str(docs_zip), "r") as zf:
        zf.extractall(path=str(config_dir))
    set_docs_version(config_dir / "docs", __version__)


def set_docs_version(docs_dir: pathlib.Path, version: str):
    """Set the version of the docs directory"""
    if not docs_dir.exists():
        docs_dir.mkdir(parents=True)
    version_file = docs_dir / ".version"
    if version_file.exists():
        version_file.unlink()
    with version_file.open("w") as f:
        f.write(version)