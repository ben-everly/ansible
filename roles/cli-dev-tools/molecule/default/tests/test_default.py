import pytest


@pytest.mark.parametrize("pkg", [
    "jq",
    "ripgrep",
    "zsh",
    "fzf",
    "git",
    "curl",
    "vim",
])
def test_apt_packages_installed(host, pkg):
    assert host.package(pkg).is_installed


def test_default_shell_is_zsh(host):
    user = host.user()
    assert user.shell == "/usr/bin/zsh"
