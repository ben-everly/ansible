import pytest

PROVIDERS = {
    "pip": "pip show pynvim",
    "gem": "gem list -i neovim",
    "npm": "npm ls -g neovim",
    "cpanm": "perl -MNeovim::Ext -e 1",
}


def test_universal_ctags_installed(host):
    assert host.package("universal-ctags").is_installed


def test_nvim_binary(host):
    home = host.user().home
    f = host.file(f"{home}/.local/bin/nvim")
    assert f.exists
    assert f.is_file
    assert f.mode & 0o111


def test_nvim_runs(host):
    home = host.user().home
    # FUSE is unavailable in docker, so extract-and-run the AppImage
    cmd = host.run(f"APPIMAGE_EXTRACT_AND_RUN=1 {home}/.local/bin/nvim --version")
    assert cmd.rc == 0, f"nvim --version failed: {cmd.stderr!r}"
    assert "NVIM" in cmd.stdout


@pytest.mark.parametrize(
    "provider,cmd", PROVIDERS.items(), ids=list(PROVIDERS)
)
def test_provider_package_installed(host, provider, cmd):
    result = host.run(cmd)
    assert result.rc == 0, f"{provider} provider not installed ({cmd!r}): {result.stderr!r}"
