from pathlib import Path

import yaml

SCENARIO_DIR = Path(__file__).parents[1]

# expected version comes from the role's pin, so a bump edits one place
AWS_CLI_VERSION = yaml.safe_load(
    (SCENARIO_DIR.parents[1] / "defaults" / "main.yml").read_text()
)["aws_cli_version"]

# the older version prepare.yml seeds, read from prepare.yml itself so the two
# can never drift apart
AWS_CLI_OLD_VERSION = yaml.safe_load((SCENARIO_DIR / "prepare.yml").read_text())[0][
    "vars"
]["aws_cli_version"]


def test_fixture_seeds_an_older_version():
    # Guards the scenario itself: if the seeded version ever reaches the pin,
    # converge's version gate closes and the upgrade assertion below would pass
    # without any upgrade having happened.
    assert AWS_CLI_OLD_VERSION != AWS_CLI_VERSION, (
        f"prepare.yml seeds {AWS_CLI_OLD_VERSION}, which is the pinned version — "
        "this scenario would no longer exercise an upgrade"
    )


def test_aws_upgraded_to_pinned_version(host):
    # prepare.yml seeded AWS_CLI_OLD_VERSION; converge should have upgraded it.
    cmd = host.run("aws --version")
    assert cmd.rc == 0, f"aws --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    combined = cmd.stdout + cmd.stderr
    assert AWS_CLI_VERSION in combined, f"expected pinned version, got: {combined!r}"
    assert AWS_CLI_OLD_VERSION not in combined, f"old version still present: {combined!r}"
