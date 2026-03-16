def test_btm_binary_exists(host):
    btm = host.file("/usr/bin/btm")
    assert btm.exists
    assert btm.is_file
    assert btm.mode & 0o111


def test_btm_version(host):
    cmd = host.run("btm --version")
    assert cmd.rc == 0
    assert "btm" in cmd.stdout.lower() or "bottom" in cmd.stdout.lower()
