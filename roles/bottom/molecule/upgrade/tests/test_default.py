from pathlib import Path

import yaml

SCENARIO_DIR = Path(__file__).parents[1]

BOTTOM_VERSION = yaml.safe_load(
    (SCENARIO_DIR.parents[1] / "defaults" / "main.yml").read_text()
)["bottom_version"]


def test_dpkg_reports_the_pinned_version(host):
    cmd = host.run("dpkg-query -W -f='${Version}' bottom")
    assert cmd.rc == 0, f"dpkg-query failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    installed = cmd.stdout.strip()
    assert installed.split("-")[0] == BOTTOM_VERSION, f"dpkg reports {installed!r}, expected {BOTTOM_VERSION}"


def test_btm_upgraded_to_pinned_version(host):
    cmd = host.run("btm --version")
    assert cmd.rc == 0, f"btm --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert cmd.stdout.split() == ["bottom", BOTTOM_VERSION], f"expected pinned version, got: {cmd.stdout!r}"
