import pytest

# from https://cli.github.com/packages/githubcli-archive-keyring.gpg, captured 2026-06-07
GH_KEY_FPR = "2C6106201985B60E6C7AC87323F3D4EA75716059"


def test_gh_keyring_present(host):
    keyring = "/etc/apt/keyrings/github-cli.asc"
    f = host.file(keyring)
    assert f.exists
    assert f.size > 0
    cmd = host.run(f"gpg --show-keys --with-colons {keyring}")
    assert cmd.rc == 0, f"gpg --show-keys failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert GH_KEY_FPR in cmd.stdout, f"unexpected key fingerprint: {cmd.stdout!r}"


def test_gh_no_stale_module_keyring(host):
    # the binary key the module fetched while signed_by was a URL
    assert not host.file("/etc/apt/keyrings/github-cli.gpg").exists


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
