<!-- STATIC CONTENT START
Use this section for adding additional content to the README
This will not be overwritten by Docsible -->
# Role overview

This role performs health validation checks on Virtual Machines running in OpenShift Virtualization.
It verifies VM status, networking, storage, and resource configuration, and generates an HTML report
summarizing the results.

## Checks performed

- **Status**: VM phase (Running), Ready condition, guest agent presence, node assignment
- **Networking**: Interface IP assignment, interface name consistency, masquerade pod network, bridge/multus attachment
- **Storage**: PVC bound status, DataVolume succeeded status, volume attachment verification
- **Resources**: CPU/memory requests vs limits, node capacity, overcommit detection

## Usage

```yaml
---
- name: Run VM healthchecks
  hosts: localhost
  connection: local
  gather_facts: false
  roles:
    - role: infra.openshift_virtualization_ops.vm_healthcheck
      vars:
        vm_healthcheck_namespace: my-vms
        vm_healthcheck_vm_names:
          - my-vm-01
          - my-vm-02
        vm_healthcheck_report_path: /tmp/vm_healthcheck_report.html
```

Individual check categories can be disabled:

```yaml
vm_healthcheck_check_networking: false
vm_healthcheck_check_storage: false
vm_healthcheck_check_resources: false
vm_healthcheck_generate_report: false
```

<!-- STATIC CONTENT END -->
<!-- Everything below will be overwritten by Docsible -->
<!-- DOCSIBLE START -->
## vm_healthcheck

```
Role belongs to infra/openshift_virtualization_ops
Namespace - infra
Collection - openshift_virtualization_ops
Version - 1.0.2
Repository - https://github.com/redhat-cop/openshift_virtualization_ops
```

Description: Health validation and status reporting for Virtual Machines.

### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|
| [`vm_healthcheck_namespace`](defaults/main.yml#L4)   | str   | `""` |   True  |  Target namespace |
| [`vm_healthcheck_vm_names`](defaults/main.yml#L9)   | list   | `[]` |   False  |  List of VM names |
| [`vm_healthcheck_check_networking`](defaults/main.yml#L14)   | bool   | `true` |   False  |  Check networking |
| [`vm_healthcheck_check_storage`](defaults/main.yml#L19)   | bool   | `true` |   False  |  Check storage |
| [`vm_healthcheck_check_resources`](defaults/main.yml#L24)   | bool   | `true` |   False  |  Check resources |
| [`vm_healthcheck_generate_report`](defaults/main.yml#L29)   | bool   | `true` |   False  |  Generate report |
| [`vm_healthcheck_report_path`](defaults/main.yml#L34)   | str   | `/tmp/vm_healthcheck_report.html` |   False  |  Report output path |
| [`vm_healthcheck_kubevirt_api_version`](defaults/main.yml#L39)   | str   | `kubevirt.io/v1` |   True  |  KubeVirt API Version |
| [`vm_healthcheck_cdi_api_version`](defaults/main.yml#L44)   | str   | `cdi.kubevirt.io/v1beta1` |   True  |  CDI API Version |
| [`vm_healthcheck_openshift_host`](defaults/main.yml#L49)   | str   | `{{ openshift_host }}` |   True  |  OpenShift host |
| [`vm_healthcheck_openshift_api_key`](defaults/main.yml#L53)   | str   | `{{ openshift_api_key }}` |   True  |  OpenShift API Key |
| [`vm_healthcheck_openshift_verify_ssl`](defaults/main.yml#L57)   | str   | `{{ openshift_verify_ssl }}` |   True  |  Enable SSL Verification |

## Author Information

OpenShift Virtualization Migration Contributors

## License

GPL-3.0-only

## Minimum Ansible Version

2.15.0

<!-- DOCSIBLE END -->
