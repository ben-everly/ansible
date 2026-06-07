def test_enpass_package_installed(host):
    assert host.package("enpass").is_installed


def test_enpass_binary(host):
    # enpass installs to /opt/enpass/, no /usr/bin symlink
    f = host.file("/opt/enpass/Enpass")
    assert f.exists
    assert f.is_file
    assert f.mode & 0o111


# from https://apt.enpass.io/keys/enpass-linux.key, captured 2026-06-07
ENPASS_KEY_FPR = "F433834B65BE665BCE974660877653760D0214BC"


def test_enpass_keyring_present(host):
    keyring = "/etc/apt/keyrings/enpass.asc"
    f = host.file(keyring)
    assert f.exists
    assert f.size > 0
    cmd = host.run(f"gpg --show-keys --with-colons {keyring}")
    assert cmd.rc == 0, f"gpg --show-keys failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert ENPASS_KEY_FPR in cmd.stdout, f"unexpected key fingerprint: {cmd.stdout!r}"


def test_enpass_repo_configured(host):
    f = host.file("/etc/apt/sources.list.d/enpass.sources")
    assert f.exists
    content = f.content_string
    assert "URIs: https://apt.enpass.io/" in content
    # repo must be scoped to its own key, not globally-trusted
    assert "Signed-By: /etc/apt/keyrings/enpass.asc" in content


def test_enpass_no_global_key(host):
    # the .deb postinst installs a redundant global key; the role strips it,
    # and the old apt_repository-era .list source must be gone too
    assert not host.file("/etc/apt/trusted.gpg.d/enpass.asc").exists
    assert not host.file("/etc/apt/sources.list.d/enpass.list").exists
