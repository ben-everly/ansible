# Ansible Pull - Workstation

Ansible playbook for provisioning and maintaining my personal workstation and server environments.

## Usage

Install Galaxy dependencies:

```sh
ansible-galaxy install -r roles/requirements.yml
```

Run the playbook:

```sh
ansible-playbook playbook.yml -K
```

## Roles

Roles live in `roles/` and are applied via `playbook.yml`. Each role installs and configures a specific tool or application.

## Testing

Roles are tested with [Molecule](https://github.com/ansible/molecule) using Docker containers and [Testinfra](https://testinfra.readthedocs.io/) for verification.

### Prerequisites

- Docker
- Python 3

### Setup

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-test.txt
```

### Running Tests

Run all roles with molecule tests:

```sh
make test
```

Run tests for a specific role:

```sh
make test ROLE=gh-cli
```

Run individual stages (useful during development):

```sh
make converge ROLE=bottom   # run the role
make verify ROLE=bottom     # run testinfra tests
make destroy ROLE=bottom    # tear down the container
```

Alternatively, run molecule directly from the role directory:

```sh
cd roles/<role-name>
molecule test
```

### Roles with Molecule Scenarios

Not all roles have molecule tests yet. Roles with tests have a `molecule/default/` directory containing:

- `molecule.yml` — platform config (driver, provisioner, verifier, and test sequence are inherited from `.config/molecule/config.yml`)
- `converge.yml` — playbook that applies the role
- `tests/test_default.py` — testinfra assertions
- `prepare.yml` (optional) — pre-test setup (e.g. installing dependencies)

### Environment Variables

Some roles adapt their behavior based on environment variables:

| Variable   | Role     | Effect                                                                                                          |
| ---------- | -------- | --------------------------------------------------------------------------------------------------------------- |
| `GH_TOKEN` | `gh-cli` | When set, gh extensions are installed and tested. When unset, extension tasks and tests are skipped gracefully. |

To run gh-cli tests with extension coverage:

```sh
GH_TOKEN=ghp_xxx molecule test
```

### Writing Tests for a New Role

1. Create the molecule scenario directory:

    ```
    roles/<role-name>/molecule/default/
    ```

2. Add `molecule.yml` (only platforms — shared config is auto-discovered from `.config/molecule/config.yml`):

    ```yaml
    ---
    platforms:
        - name: <role-name>
          image: geerlingguy/docker-ubuntu2204-ansible:latest
          privileged: true
          pre_build_image: true
    ```

3. Add `converge.yml`:

    ```yaml
    ---
    - name: Converge
      hosts: all
      become: true
      roles:
          - role: "{{ playbook_dir }}/../.."
    ```

4. Add `tests/test_default.py` with testinfra assertions:

    ```python
    def test_binary_exists(host):
        binary = host.file("/usr/bin/<tool>")
        assert binary.exists
        assert binary.is_file
    ```

5. Run `make test ROLE=<role-name>` from the repo root.
