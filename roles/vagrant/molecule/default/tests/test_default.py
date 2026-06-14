# key from https://apt.releases.hashicorp.com/gpg, captured 2026-06-07
# verify at https://www.hashicorp.com/security (Linux Package Verification)
VAGRANT_KEY_FPR = "798AEC654E5C15428C8E42EEAA16FCBCA621E701"


def test_vagrant_package_installed(host):
    assert host.package("vagrant").is_installed


def test_vagrant_keyring_present(host):
    keyring = "/etc/apt/keyrings/vagrant.asc"
    f = host.file(keyring)
    assert f.exists
    assert f.size > 0
    cmd = host.run(f"gpg --show-keys --with-colons {keyring}")
    assert cmd.rc == 0, f"gpg --show-keys failed: stdout={cmd.stdout!r} stderr={cmd.stderr!r}"
    assert VAGRANT_KEY_FPR in cmd.stdout, f"unexpected key fingerprint: {cmd.stdout!r}"


def test_vagrant_version(host):
    cmd = host.run("vagrant --version")
    assert cmd.rc == 0, f"vagrant --version failed: {cmd.stderr!r}"
    assert "Vagrant" in cmd.stdout, f"unexpected version output: {cmd.stdout!r}"


def test_vagrant_repo_scoped_to_its_own_key(host):
    f = host.file("/etc/apt/sources.list.d/vagrant.sources")
    assert f.exists
    content = f.content_string
    assert "URIs: https://apt.releases.hashicorp.com" in content
    # key must be scoped to this repo, not the global trust store
    assert "Signed-By: /etc/apt/keyrings/vagrant.asc" in content


def test_vagrant_no_global_trust_key(host):
    # the legacy global-trust key must be gone
    assert not host.file("/etc/apt/trusted.gpg.d/vagrant.asc").exists
