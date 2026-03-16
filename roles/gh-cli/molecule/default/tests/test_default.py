import pytest


def test_gh_binary_exists(host):
    gh = host.file("/usr/bin/gh")
    assert gh.exists
    assert gh.is_file
    assert gh.mode & 0o111


def test_gh_version(host):
    cmd = host.run("gh --version")
    assert cmd.rc == 0
    assert "gh version" in cmd.stdout


def test_gh_act_extension(host):
    token_check = host.run('test -n "$GH_TOKEN"')
    if token_check.rc != 0:
        pytest.skip("GH_TOKEN not set, skipping extension test")
    cmd = host.run("gh extension list")
    assert "nektos/gh-act" in cmd.stdout
