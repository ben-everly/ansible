# key from https://pkg.cloudflare.com/cloudflare-main.gpg, captured 2026-07-08
# Cloudflare publishes no fingerprint on pkg.cloudflare.com or its cloudflared
# docs, so these are NOT independently corroborated — trust is the HTTPS fetch.
# primary signs the repo; no expiry set. uid "CloudFlare Software Packaging 2025".
# Cloudflare rotates this year-branded key (this one rolled 2025-10-23; the
# prior keys were removed 2026-04-30). When they re-sign the repo with a
# successor, `apt update` fails closed and the fingerprint assert below goes
# red — re-capture the .asc and update CF_KEY_FPRS. No successor published yet.
CF_KEY_FPRS = [
    "CC94B39C77AE7342A68B89628A682D308D4E5E73",
    "06C89DB3B80A8F4349697C76029E1444B7D9F50F",
]


def test_cloudflared_keyring_present(host):
    keyring = "/etc/apt/keyrings/cloudflare-main.asc"
    f = host.file(keyring)
    assert f.exists
    assert f.size > 0
    cmd = host.run(f"gpg --show-keys --with-colons {keyring}")
    assert cmd.rc == 0, f"gpg --show-keys failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    for fpr in CF_KEY_FPRS:
        assert fpr in cmd.stdout, f"missing expected key {fpr}: {cmd.stdout!r}"


def test_cloudflared_repo_configured(host):
    f = host.file("/etc/apt/sources.list.d/cloudflared.sources")
    assert f.exists
    content = f.content_string
    assert "URIs: https://pkg.cloudflare.com/cloudflared" in content
    # repo must be scoped to its own key, not globally-trusted
    assert "Signed-By: /etc/apt/keyrings/cloudflare-main.asc" in content


def test_cloudflared_binary_exists(host):
    b = host.file("/usr/bin/cloudflared")
    assert b.exists
    assert b.is_file
    assert b.mode & 0o111


def test_cloudflared_version(host):
    cmd = host.run("cloudflared --version")
    assert cmd.rc == 0
    assert "cloudflared version" in cmd.stdout
