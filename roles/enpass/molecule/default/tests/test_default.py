def test_enpass_package_installed(host):
    assert host.package("enpass").is_installed


def test_enpass_binary(host):
    # enpass installs to /opt/enpass/, no /usr/bin symlink
    f = host.file("/opt/enpass/Enpass")
    assert f.exists
    assert f.is_file
    assert f.mode & 0o111


def test_enpass_keyring_present(host):
    keyring = "/etc/apt/keyrings/enpass.asc"
    f = host.file(keyring)
    assert f.exists
    assert f.size > 0
    cmd = host.run(f"gpg --show-keys {keyring}")
    assert cmd.rc == 0, f"gpg --show-keys failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"


def test_enpass_repo_configured(host):
    f = host.file("/etc/apt/sources.list.d/enpass.sources")
    assert f.exists
    content = f.content_string
    assert "URIs: https://apt.enpass.io/" in content
    # repo must be scoped to its own key, not globally-trusted
    assert "Signed-By: /etc/apt/keyrings/enpass.asc" in content
