# OpenShift Virtualization Operations Collection

This repository contains tooling to support the operational aspects of OpenShift Virtualization.

<!-- add collection requirements -->

## Installation

You can install the `infra.openshift_virtualization_ops` collection with the Ansible Galaxy CLI:

```bash
    ansible-galaxy collection install infra.openshift_virtualization_ops
```

You can also include it in a `requirements.yml` file and install it via
`ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
  - name: infra.openshift_virtualization_ops
```

Note that if you install any collection from Ansible Galaxy, they will not be upgraded automatically when you upgrade the Ansible package.

To upgrade the collection to the latest available version, run the following
command:

```bash
ansible-galaxy collection install infra.openshift_virtualization_ops --upgrade
```

You can also install a specific version of the collection, for example, if you
need to downgrade when something is broken in the latest version (please report
an issue in this repository). Use the following syntax where `X.Y.Z` can be any
[available version](https://galaxy.ansible.com/infra/openshift_virtualization_ops):

```bash
ansible-galaxy collection install infra.openshift_virtualization_ops:==X.Y.Z
```

See
[Ansible Using Collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)
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

## Release Notes

Information related to the releases for this collection can be found in the Release Notes found within this collection.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
