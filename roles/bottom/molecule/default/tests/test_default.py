from pathlib import Path

import yaml

BOTTOM_VERSION = yaml.safe_load(
    (Path(__file__).parents[3] / "defaults" / "main.yml").read_text()
)["bottom_version"]


def test_bottom_package_installed(host):
    assert host.package("bottom").is_installed


def test_btm_binary_exists(host):
    btm = host.file("/usr/bin/btm")
    assert btm.exists
    assert btm.is_file
    assert btm.mode & 0o111


def test_btm_version(host):
    cmd = host.run("btm --version")
    assert cmd.rc == 0, f"btm --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert cmd.stdout.split() == ["bottom", BOTTOM_VERSION], f"unexpected btm version output: {cmd.stdout!r}"

