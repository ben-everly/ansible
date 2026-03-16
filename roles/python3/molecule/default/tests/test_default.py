import pytest


@pytest.mark.parametrize("pkg", [
    "python3",
    "python3-gpg",
    "python3-pip",
])
def test_apt_packages_installed(host, pkg):
    assert host.package(pkg).is_installed


def test_python3_version(host):
    cmd = host.run("python3 --version")
    assert cmd.rc == 0
