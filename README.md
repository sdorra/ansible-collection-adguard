# Ansible Collection - sdorra.adguard

This Ansible Collection provides a module for managing rewrites of [AdGuard Home](https://adguard.com/de/adguard-home/overview.html).

## Included content

This collection includes the following module:

- `adguard_rewrite`: This module allows you to create and delete rewrites on [AdGuard Home](https://adguard.com/de/adguard-home/overview.html).

## Installation

The collection can be installed with the `ansible-galaxy` tool.

```bash
ansible-galaxy collection install sdorra.adguar
```

For more information have a look at the [ansible documentation](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html#installing-collections)

## Using this collection

You can use the modules in this collection in your playbooks as follows:

```yaml
- name: Create rewrite
- sdorra.adguard.adguard_rewrite:
    state: present
    servers:
      - url: http://localhost:3000
        username: admin
        password: password
    rewrites:
      - domain: example.com
        answer: 192.168.1.42

```

## License
This collection is licensed under the MIT License.

## Author

[Sebastian Sdorra](https://sdorra.dev)
