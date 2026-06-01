def test_acli_package_installed(host):
    assert host.package("acli").is_installed


def test_acli_binary(host):
    f = host.file("/usr/bin/acli")
    assert f.exists
    assert f.is_file
    assert f.mode & 0o111


def test_acli_version(host):
    cmd = host.run("acli --version")
    assert cmd.rc == 0, f"acli --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert "version" in cmd.stdout.lower(), f"unexpected output: {cmd.stdout!r}"


def test_acli_keyring_dearmored(host):
    keyring = "/etc/apt/keyrings/acli-archive-keyring.gpg"
    f = host.file(keyring)
    assert f.exists
    assert f.size > 0
    cmd = host.run(f"gpg --show-keys {keyring}")
    assert cmd.rc == 0, f"gpg --show-keys failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    # ensure the dearmor step ran — ASCII-armored keys start with "-----BEGIN PGP"
    assert not f.content.startswith(b"-----BEGIN PGP")


def test_acli_repo_configured(host):
    f = host.file("/etc/apt/sources.list.d/acli.list")
    assert f.exists
    content = f.content_string
    assert "acli.atlassian.com/linux/deb" in content
    # guards the ansible_architecture -> amd64 templating
    assert "arch=amd64" in content
