from pathlib import Path

import yaml

SCENARIO_DIR = Path(__file__).parents[1]

YAZI_PIN = yaml.safe_load(
    (SCENARIO_DIR.parents[1] / "defaults" / "main.yml").read_text()
)["yazi_version"].lstrip("v")

YAZI_REVERTED_VERSION = yaml.safe_load((SCENARIO_DIR / "converge.yml").read_text())[0][
    "vars"
]["yazi_version"].lstrip("v")


def test_dpkg_reports_the_reverted_version(host):
    cmd = host.run("dpkg-query -W -f='${Version}' yazi")
    assert cmd.rc == 0, f"dpkg-query failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    installed = cmd.stdout.strip()
    assert installed.split("-")[0] == YAZI_REVERTED_VERSION, f"dpkg reports {installed!r}, expected {YAZI_REVERTED_VERSION}"


def test_yazi_downgraded_to_reverted_version(host):
    cmd = host.run("yazi --version")
    assert cmd.rc == 0, f"yazi --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert f"Version: {YAZI_REVERTED_VERSION} " in cmd.stdout, f"expected reverted version, got: {cmd.stdout!r}"
    assert YAZI_PIN not in cmd.stdout, f"seeded pin still present: {cmd.stdout!r}"
