from pathlib import Path

import yaml

SCENARIO_DIR = Path(__file__).parents[1]

BOTTOM_REVERTED_VERSION = yaml.safe_load((SCENARIO_DIR / "converge.yml").read_text())[0][
    "vars"
]["bottom_version"]


def test_dpkg_reports_the_reverted_version(host):
    cmd = host.run("dpkg-query -W -f='${Version}' bottom")
    assert cmd.rc == 0, f"dpkg-query failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    installed = cmd.stdout.strip()
    assert installed.split("-")[0] == BOTTOM_REVERTED_VERSION, f"dpkg reports {installed!r}, expected {BOTTOM_REVERTED_VERSION}"


def test_btm_downgraded_to_reverted_version(host):
    cmd = host.run("btm --version")
    assert cmd.rc == 0, f"btm --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert cmd.stdout.split() == ["bottom", BOTTOM_REVERTED_VERSION], f"expected reverted version, got: {cmd.stdout!r}"
