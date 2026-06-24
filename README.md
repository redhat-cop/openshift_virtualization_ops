# OpenShift Virtualization Operations Collection

![GitHub Release](https://img.shields.io/github/v/release/redhat-cop/openshift_virtualization_ops?include_prereleases&style=flat-square)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/redhat-cop/openshift_virtualization_ops/ci.yml?style=flat-square&label=release)](https://github.com/redhat-cop/openshift_virtualization_ops/actions)
[![Semantic Versioning](https://img.shields.io/badge/semver-2.0.0-blue?style=flat-square)](https://semver.org/)
[![License](https://img.shields.io/github/license/redhat-cop/openshift_virtualization_ops?style=flat-square)](LICENSE)

<!--TOC-->

- [OpenShift Virtualization Operations Collection](#openshift-virtualization-operations-collection)
  - [Description](#description)
  - [Documentation](#documentation)
  - [Release Notes](#release-notes)
  - [Roles](#roles)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Use Cases](#use-cases)
  - [Testing](#testing)
  - [Support](#support)
  - [License](#license)

<!--TOC-->

## Description

This repository contains tooling to support the operational aspects of OpenShift Virtualization.

## Documentation

* [Contributing Guide](CONTRIBUTING.md)

## Release Notes

See [CHANGELOG.md](CHANGELOG.md) for release history and changes.

## Roles

This collection includes the following roles for operating OpenShift Virtualization:

<!--ROLES_LIST_START-->
* [vm_backup_restore](roles/vm_backup_restore/README.md) - Virtual Machine backup and restore capabilities.
* [vm_collect](roles/vm_collect/README.md) - Collection of Migration Toolkit for Virtualization inventory information.
* [vm_hot_plug](roles/vm_hot_plug/README.md) - Hot Plug Virtual Machine resources.
* [vm_lifecycle](roles/vm_lifecycle/README.md) - Management of the lifecycle activities of Virtual Machines.
* [vm_networking](roles/vm_networking/README.md) - Management of Virtual Machine networking.
* [vm_patching](roles/vm_patching/README.md) - Patching related activities for Virtual Machines.
<!--ROLES_LIST_END-->

## Requirements

The following Ansible Collections are required:

```yaml
---
collections:
  - name: redhat.openshift_virtualization
    version: ">=2.1.0"
  - name: redhat.openshift
    version: ">=4.0.0"
  - name: kubernetes.core
    version: ">=5.2.0"
...
```

## Installation

You can install the `infra.openshift_virtualization_ops` collection with the Ansible Galaxy CLI:

```shell
ansible-galaxy collection install infra.openshift_virtualization_ops
```

Note that if you install any collections from Ansible Galaxy, they will not be upgraded automatically when you upgrade the Ansible package.

To upgrade the collection to the latest available version, run the following command:

```shell
ansible-galaxy collection install infra.openshift_virtualization_ops --upgrade
```

You can also include it in a `requirements.yml` file and install it with
`ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: infra.openshift_virtualization_ops
...
```

See
[Using Ansible Collections](https://docs.ansible.com/projects/ansible/latest/collections_guide/index.html)
for more details.

## Use Cases

This collection is ideal for accomplishing the following using Ansible automation:

* Day 2 operations of Virtual Machines running in OpenShift.

## Testing

[tox](https://tox.wiki) is used to perform tests and verification of this collection.

The following commands can be used to execute the various types of tests implemented:

```shell
tox -av # lists all tests

tox # run them all

tox -e <test name> # run specific one

tox -f sanity --ansible -c tox-ansible.ini     # run tox-ansible that does our ansible-test sanity suite
```

## Support

The [Ansible Forum](https://forum.ansible.com/tag/openshift_migrate) can be used for additional questions and issues related to this collection.

## License

GNU General Public License v3.0 or later.

See the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) to see the full text.
