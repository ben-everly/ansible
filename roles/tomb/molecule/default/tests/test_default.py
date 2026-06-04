import pytest


@pytest.mark.parametrize("pkg", [
    "cryptsetup",
    "gnupg",
    "pinentry-curses",
    "sudo",
    "zsh",
])
def test_apt_dependencies_installed(host, pkg):
    assert host.package(pkg).is_installed


def test_tomb_binary(host):
    f = host.file("/usr/local/bin/tomb")
    assert f.exists
    assert f.is_file
    assert f.mode & 0o111


def test_tomb_version(host):
    cmd = host.run("tomb -h")
    assert cmd.rc == 0, f"tomb -h failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    combined = cmd.stdout + cmd.stderr
    assert "2.9" in combined, f"unexpected tomb output: {combined!r}"
