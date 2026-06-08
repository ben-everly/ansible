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
    # resolve pip from PATH, same as the role does (see prepare.yml)
    cmd = host.run("pip show pynvim")
    assert cmd.rc == 0, f"pynvim not installed for `pip`: {cmd.stderr!r}"


def test_node_provider_installed(host):
    cmd = host.run("npm ls -g neovim")
    assert cmd.rc == 0, f"global npm neovim package missing: {cmd.stdout!r}"


def test_ruby_provider_installed(host):
    cmd = host.run("gem list -i neovim")
    assert cmd.rc == 0, f"neovim ruby gem missing: {cmd.stdout!r}"


def test_perl_provider_installed(host):
    cmd = host.run("perl -MNeovim::Ext -e 1")
    assert cmd.rc == 0, f"Neovim::Ext perl module missing: {cmd.stderr!r}"
