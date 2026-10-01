def test_claude_binary_exists(host):
    b = host.file(f"{host.user().home}/.local/bin/claude")
    assert b.exists
    assert b.mode & 0o111


def test_claude_version(host):
    cmd = host.run(f"{host.user().home}/.local/bin/claude --version")
    assert cmd.rc == 0
    assert "Claude Code" in cmd.stdout
