import re


def test_pulumi_binary(host):
    f = host.file(f"{host.user().home}/.local/bin/pulumi")
    assert f.exists
    assert f.is_file
    assert f.mode & 0o111


def test_pulumi_cosign_installed(host):
    f = host.file(f"{host.user().home}/.local/bin/cosign")
    assert f.exists
    assert f.is_file
    assert f.mode & 0o111


def test_pulumi_version_runs(host):
    cmd = host.run(f"{host.user().home}/.local/bin/pulumi version")
    assert cmd.rc == 0, f"pulumi version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert re.match(r"^v\d+\.\d+\.\d+", cmd.stdout.strip()), f"unexpected version output: {cmd.stdout!r}"
