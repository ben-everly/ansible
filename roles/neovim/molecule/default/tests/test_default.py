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


def test_python_provider_installed(host):
    # pynvim must land in the venv that bare 'pip' resolves to
    cmd = host.run("/opt/nvenv/bin/python -c 'import pynvim'")
    assert cmd.rc == 0, f"pynvim not importable: {cmd.stderr!r}"


def test_node_provider_installed(host):
    cmd = host.run("npm ls -g neovim")
    assert cmd.rc == 0, f"global npm neovim package missing: {cmd.stdout!r}"
