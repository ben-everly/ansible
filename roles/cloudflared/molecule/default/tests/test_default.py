# key from https://pkg.cloudflare.com/cloudflare-main.gpg, captured 2026-07-08
# Cloudflare publishes no fingerprint on pkg.cloudflare.com or its cloudflared
# docs, so these are NOT independently corroborated — trust is the HTTPS fetch.
# primary signs the repo; no expiry set. uid "CloudFlare Software Packaging 2025".
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


def test_cloudflared_binary_exists(host):
    b = host.file("/usr/bin/cloudflared")
    assert b.exists
    assert b.is_file
    assert b.mode & 0o111


def test_cloudflared_version(host):
    cmd = host.run("cloudflared --version")
    assert cmd.rc == 0
    assert "cloudflared version" in cmd.stdout
