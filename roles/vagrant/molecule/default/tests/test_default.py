def test_vagrant_package_installed(host):
    assert host.package("vagrant").is_installed


def test_vagrant_version(host):
    cmd = host.run("vagrant --version")
    assert cmd.rc == 0, f"vagrant --version failed: {cmd.stderr!r}"


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
