import pytest


@pytest.mark.parametrize("pkg", [
    "ca-certificates",
    "fontconfig",
    "xz-utils",
])
def test_apt_dependencies_installed(host, pkg):
    assert host.package(pkg).is_installed


def test_font_directory_populated(host):
    home = host.user().home
    d = host.file(f"{home}/.local/share/fonts/FiraCode")
    assert d.exists
    assert d.is_directory
    cmd = host.run(f"ls {home}/.local/share/fonts/FiraCode")
    assert ".ttf" in cmd.stdout or ".otf" in cmd.stdout, f"no font files: {cmd.stdout!r}"


def test_version_file_written(host):
    home = host.user().home
    f = host.file(f"{home}/.local/share/fonts/FiraCode/_version.txt")
    assert f.exists
    assert f.size > 0


def test_fontconfig_sees_firacode(host):
    cmd = host.run("fc-list")
    assert "FiraCode" in cmd.stdout, "fc-list does not report FiraCode"
