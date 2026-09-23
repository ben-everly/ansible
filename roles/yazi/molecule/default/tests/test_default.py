from pathlib import Path

import pytest
import yaml

DEFAULTS = yaml.safe_load(
    (Path(__file__).parents[3] / "defaults" / "main.yml").read_text()
)
YAZI_VERSION = DEFAULTS["yazi_version"].lstrip("v")
RECOMMENDED_PACKAGES = DEFAULTS["yazi_recommended_packages"]


def test_yazi_package_installed(host):
    assert host.package("yazi").is_installed


def test_hard_dependency_installed(host):
    assert host.package("file").is_installed


@pytest.mark.parametrize("package", RECOMMENDED_PACKAGES)
def test_recommended_packages_installed(host, package):
    assert host.package(package).is_installed


def test_fd_find_installed(host):
    # Deliberately not in RECOMMENDED_PACKAGES: the role installs it directly,
    # so it needs coverage the parametrized test no longer gives it.
    assert host.package("fd-find").is_installed


def test_yazi_binary(host):
    f = host.file("/usr/bin/yazi")
    assert f.exists
    assert f.is_file
    assert f.mode & 0o111


def test_ya_binary(host):
    f = host.file("/usr/bin/ya")
    assert f.exists
    assert f.is_file
    assert f.mode & 0o111


def test_fd_resolvable_by_the_name_yazi_spawns(host):
    # linked_to canonicalizes, and /usr/bin/fdfind is itself a link into
    # /usr/lib/cargo/bin, so assert behavior rather than the link target.
    assert host.file("/usr/local/bin/fd").is_symlink
    cmd = host.run("fd --version")
    assert cmd.rc == 0, f"fd --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    fdfind = host.run("fdfind --version")
    assert cmd.stdout.strip() == fdfind.stdout.strip(), (
        f"fd resolves to something other than fd-find: {cmd.stdout!r} vs {fdfind.stdout!r}"
    )


def test_yazi_version(host):
    cmd = host.run("yazi --version")
    assert cmd.rc == 0, f"yazi --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert f"Version: {YAZI_VERSION} " in cmd.stdout, f"unexpected yazi version output: {cmd.stdout!r}"


def test_ya_version(host):
    cmd = host.run("ya --version")
    assert cmd.rc == 0, f"ya --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert f"Version: {YAZI_VERSION} " in cmd.stdout, f"unexpected ya version output: {cmd.stdout!r}"


def test_no_staging_dir_left_behind(host):
    cmd = host.run("find /tmp -maxdepth 1 -name 'ansible.*'")
    assert not cmd.stdout.strip(), f"staging dir survived cleanup: {cmd.stdout!r}"
