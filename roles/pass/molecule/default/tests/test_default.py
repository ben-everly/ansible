import pytest


@pytest.mark.parametrize("pkg", [
    "pass",
    "pass-extension-tomb",
])
def test_apt_packages_installed(host, pkg):
    assert host.package(pkg).is_installed
