def test_handy_package_installed(host):
    assert host.package("handy").is_installed


def test_handy_binary(host):
    cmd = host.run("command -v handy")
    assert cmd.rc == 0, "handy binary not found on PATH"
