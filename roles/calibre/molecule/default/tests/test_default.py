def test_calibre_installed(host):
    assert host.package("calibre").is_installed
