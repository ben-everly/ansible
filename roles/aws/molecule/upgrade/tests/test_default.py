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


def test_upgrade_replaced_the_seeded_install(host):
    # The installer never removes the version it upgraded from, so both trees
    # surviving with current repointed is the signature of a real upgrade —
    # something a converge that merely reinstalled the pin cannot produce.
    assert host.file(f"/usr/local/aws-cli/v2/{AWS_CLI_OLD_VERSION}").is_directory
    current = host.file("/usr/local/aws-cli/v2/current")
    assert current.is_symlink
    assert current.linked_to == f"/usr/local/aws-cli/v2/{AWS_CLI_VERSION}"


def test_aws_upgraded_to_pinned_version(host):
    # prepare.yml seeded AWS_CLI_OLD_VERSION; converge should have upgraded it.
    cmd = host.run("aws --version")
    assert cmd.rc == 0, f"aws --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    combined = cmd.stdout + cmd.stderr
    assert f"aws-cli/{AWS_CLI_VERSION}" in combined, f"expected pinned version, got: {combined!r}"
    assert f"aws-cli/{AWS_CLI_OLD_VERSION}" not in combined, f"old version still present: {combined!r}"
