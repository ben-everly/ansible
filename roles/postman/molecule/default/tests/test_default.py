def test_flatpak_installed(host):
    assert host.package("flatpak").is_installed
