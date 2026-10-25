from pathlib import Path

import yaml

BOTTOM_VERSION = yaml.safe_load(
    (Path(__file__).parents[3] / "defaults" / "main.yml").read_text()
)["bottom_version"]


def test_deb_binary_at_pinned_version(host):
    cmd = host.run("/usr/bin/btm --version")
    assert cmd.rc == 0, f"/usr/bin/btm --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert cmd.stdout.split() == ["bottom", BOTTOM_VERSION], f"unexpected btm version output: {cmd.stdout!r}"


def test_shadowing_btm_untouched(host):
    assert host.file("/usr/local/bin/btm").content_string == "#!/bin/sh\necho bottom 0.9.0\n"
