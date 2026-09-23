SENTINEL = "hand-installed fd"


def test_role_converged(host):
    assert host.package("yazi").is_installed
    assert host.package("fd-find").is_installed


def test_hand_installed_fd_not_converted_to_a_symlink(host):
    f = host.file("/usr/local/bin/fd")
    assert f.exists
    assert f.is_file
    assert not f.is_symlink


def test_hand_installed_fd_not_clobbered(host):
    cmd = host.run("/usr/local/bin/fd")
    assert cmd.rc == 0, f"planted fd failed to run: stderr={cmd.stderr!r}"
    assert cmd.stdout.strip() == SENTINEL, f"planted fd was overwritten: {cmd.stdout!r}"
