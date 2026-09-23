from pathlib import Path

import yaml

SCENARIO_DIR = Path(__file__).parents[1]

YAZI_VERSION = yaml.safe_load(
    (SCENARIO_DIR.parents[1] / "defaults" / "main.yml").read_text()
)["yazi_version"].lstrip("v")

YAZI_OLD_VERSION = yaml.safe_load((SCENARIO_DIR / "prepare.yml").read_text())[0][
    "vars"
]["yazi_version"].lstrip("v")


def test_dpkg_reports_the_pinned_version(host):
    cmd = host.run("dpkg-query -W -f='${Version}' yazi")
    assert cmd.rc == 0, f"dpkg-query failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    installed = cmd.stdout.strip()
    assert installed.split("-")[0] == YAZI_VERSION, f"dpkg reports {installed!r}, expected {YAZI_VERSION}"


def test_yazi_upgraded_to_pinned_version(host):
    cmd = host.run("yazi --version")
    assert cmd.rc == 0, f"yazi --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert f"Version: {YAZI_VERSION} " in cmd.stdout, f"expected pinned version, got: {cmd.stdout!r}"
    assert YAZI_OLD_VERSION not in cmd.stdout, f"old version still present: {cmd.stdout!r}"
