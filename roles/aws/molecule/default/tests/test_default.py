from pathlib import Path

import yaml

# expected version comes from the role's pin, so a bump edits one place
AWS_CLI_VERSION = yaml.safe_load(
    (Path(__file__).parents[3] / "defaults" / "main.yml").read_text()
)["aws_cli_version"]


def test_unzip_installed(host):
    assert host.package("unzip").is_installed


def test_aws_binary(host):
    f = host.file("/usr/local/bin/aws")
    assert f.exists
    assert f.is_file
    assert f.mode & 0o111


def test_aws_version(host):
    cmd = host.run("/usr/local/bin/aws --version")
    assert cmd.rc == 0, f"aws --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    combined = cmd.stdout + cmd.stderr
    assert f"aws-cli/{AWS_CLI_VERSION}" in combined, f"unexpected aws version output: {combined!r}"
