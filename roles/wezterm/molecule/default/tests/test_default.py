def test_wezterm_package_installed(host):
    assert host.package("wezterm").is_installed


def test_wezterm_binary(host):
    f = host.file("/usr/bin/wezterm")
    assert f.exists
    assert f.is_file
    assert f.mode & 0o111


def test_wezterm_keyring_present(host):
    keyring = "/etc/apt/keyrings/wezterm.asc"
    f = host.file(keyring)
    assert f.exists
    assert f.size > 0
    cmd = host.run(f"gpg --show-keys {keyring}")
    assert cmd.rc == 0, f"gpg --show-keys failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"


def test_wezterm_repo_configured(host):
    f = host.file("/etc/apt/sources.list.d/wezterm.sources")
    assert f.exists
    content = f.content_string
    # pin the fury.io wildcard idiom + scoped trust via Signed-By
    assert "URIs: https://apt.fury.io/wez/" in content
    assert "Suites: *" in content
    assert "Components: *" in content
    assert "Signed-By: /etc/apt/keyrings/wezterm.asc" in content


def test_wezterm_version(host):
    cmd = host.run("wezterm --version")
    assert cmd.rc == 0, f"wezterm --version failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert "wezterm" in cmd.stdout.lower(), f"unexpected output: {cmd.stdout!r}"
