import pytest

# key from https://cli.github.com/packages/githubcli-archive-keyring.gpg, captured 2026-06-13
# fingerprints corroborated in https://github.com/cli/cli/blob/trunk/docs/install_linux.md
# 2C61... signs today but expires 2026-09-05; 7F38... is the successor key
GH_KEY_FPRS = [
    "2C6106201985B60E6C7AC87323F3D4EA75716059",
    "7F38BBB59D064DBCB3D84D725612B36462313325",
]


def test_gh_keyring_present(host):
    keyring = "/etc/apt/keyrings/github-cli.asc"
    f = host.file(keyring)
    assert f.exists
    assert f.size > 0
    cmd = host.run(f"gpg --show-keys --with-colons {keyring}")
    assert cmd.rc == 0, f"gpg --show-keys failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    for fpr in GH_KEY_FPRS:
        assert fpr in cmd.stdout, f"missing expected key {fpr}: {cmd.stdout!r}"


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
    if host.run("gh auth status").rc != 0:
        pytest.skip("gh not authenticated, extensions not managed")
    cmd = host.run("gh extension list")
    assert "nektos/gh-act" in cmd.stdout
