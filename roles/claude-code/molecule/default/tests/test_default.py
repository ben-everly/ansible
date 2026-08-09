# key from https://downloads.claude.ai/keys/claude-code.asc, captured 2026-08-07
# CORROBORATED: Anthropic publishes this fingerprint in the Claude Code setup
# docs (code.claude.com/docs/en/setup, "Install with Linux package managers"
# and "Binary integrity and code signing"), so trust is not the HTTPS fetch
# alone. uid "Anthropic Claude Code Release Signing <security@anthropic.com>".
# 4096-bit RSA primary, created 2026-03-30, no expiry, signs the repo directly
# (no subkeys). If Anthropic rotates it, `apt update` fails closed and the
# assert below goes red -- re-capture the .asc and update CLAUDE_KEY_FPR.
CLAUDE_KEY_FPR = "31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE"


def test_claude_code_keyring_present(host):
    keyring = "/etc/apt/keyrings/claude-code.asc"
    f = host.file(keyring)
    assert f.exists
    assert f.size > 0
    cmd = host.run(f"gpg --show-keys --with-colons {keyring}")
    assert cmd.rc == 0, f"gpg --show-keys failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert CLAUDE_KEY_FPR in cmd.stdout, f"missing expected key: {cmd.stdout!r}"


def test_claude_code_repo_configured(host):
    f = host.file("/etc/apt/sources.list.d/claude-code.sources")
    assert f.exists
    content = f.content_string
    assert "URIs: https://downloads.claude.ai/claude-code/apt/stable" in content
    # repo must be scoped to its own key, not globally-trusted
    assert "Signed-By: /etc/apt/keyrings/claude-code.asc" in content


def test_claude_code_package_installed(host):
    assert host.package("claude-code").is_installed


def test_claude_binary_exists(host):
    b = host.file("/usr/bin/claude")
    assert b.exists
    assert b.mode & 0o111


def test_claude_version(host):
    cmd = host.run("claude --version")
    assert cmd.rc == 0
    assert "Claude Code" in cmd.stdout
