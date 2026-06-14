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


# key from https://acli.atlassian.com/gpg/public-key.asc, captured 2026-06-07
# no independent fingerprint published upstream (trust-on-first-use)
ACLI_KEY_FPR = "A99C71D268433EDC13CC885FFA73568DB7ADDBBB"


def test_acli_keyring_present(host):
    keyring = "/etc/apt/keyrings/acli.asc"
    f = host.file(keyring)
    assert f.exists
    assert f.size > 0
    cmd = host.run(f"gpg --show-keys --with-colons {keyring}")
    assert cmd.rc == 0, f"gpg --show-keys failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert ACLI_KEY_FPR in cmd.stdout, f"unexpected key fingerprint: {cmd.stdout!r}"


def test_acli_repo_configured(host):
    f = host.file("/etc/apt/sources.list.d/acli.sources")
    assert f.exists
    content = f.content_string
    assert "URIs: https://acli.atlassian.com/linux/deb" in content
    # repo must be scoped to its own key, not globally-trusted
    assert "Signed-By: /etc/apt/keyrings/acli.asc" in content


def test_acli_no_legacy_artifacts(host):
    # migration must remove the old keyring and .list source
    assert not host.file("/etc/apt/keyrings/acli-archive-keyring.gpg").exists
    assert not host.file("/etc/apt/keyrings/acli-archive-keyring.asc").exists
    assert not host.file("/etc/apt/sources.list.d/acli.list").exists
