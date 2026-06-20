from pathlib import Path

import yaml

# expected version comes from the role's pin, so a bump edits one place
AWS_CLI_VERSION = yaml.safe_load(
    (Path(__file__).parents[3] / "defaults" / "main.yml").read_text()
)["aws_cli_version"]

# the older version prepare.yml seeds; keep in sync with prepare.yml
AWS_CLI_OLD_VERSION = "2.30.0"


def test_aws_upgraded_to_pinned_version(host):
    # prepare.yml seeded AWS_CLI_OLD_VERSION; converge should have upgraded it.
    cmd = host.run("aws --version")
    assert cmd.rc == 0, f"aws --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    combined = cmd.stdout + cmd.stderr
    assert AWS_CLI_VERSION in combined, f"expected pinned version, got: {combined!r}"
    assert AWS_CLI_OLD_VERSION not in combined, f"old version still present: {combined!r}"
