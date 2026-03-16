def test_newsboat_snap_dependency(host):
    assert host.package("snapd").is_installed
