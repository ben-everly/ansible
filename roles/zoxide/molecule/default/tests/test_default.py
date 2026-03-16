def test_zoxide_installed(host):
    assert host.package("zoxide").is_installed


def test_zoxide_version(host):
    cmd = host.run("zoxide --version")
    assert cmd.rc == 0
