<!-- STATIC CONTENT START
Use this section for adding additional content to the README
This will not be overwritten by Docsible -->
# 📃 Role overview

<!-- STATIC CONTENT END -->
<!-- Everything below will be overwritten by Docsible -->
<!-- DOCSIBLE START -->
## vm_networking

```
Role belongs to infra/openshift_virtualization_ops
Namespace - infra
Collection - openshift_virtualization_ops
Version - 1.0.3
Repository - https://github.com/redhat-cop/openshift_virtualization_ops
```

Description: Manage network attachments on OpenShift Virtualization VMs

### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Choices    |Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|-------------|
| [`vm_networking_api_key`](defaults/main.yml#L23)   | str   | `{{ openshift_api_key }}` |  None  |   True  |  OpenShift API Key |
| [`vm_networking_openshift_host`](defaults/main.yml#L19)   | str   | `{{ openshift_host }}` |  None  |   True  |  OpenShift Host |
| [`vm_networking_openshift_verify_ssl`](defaults/main.yml#L27)   | str   | `{{ openshift_verify_ssl }}` |  None  |   True  |  Verify SSL Certificate |
| [`vm_networking_request`](defaults/main.yml#L7)   | list   | `[]` |  None  |   True  |  Network Attachment Requests |
| [`vm_networking_vms`](defaults/main.yml#L34)   | list   | `[]` |  None  |   False  |  Pre-collected VMs |

<summary><b>🖇️ Full descriptions for vars in defaults/main.yml</b></summary>
<br>
<b>`vm_networking_api_key`:</b> OpenShift API Key
<br>
<b>`vm_networking_openshift_host`:</b> OpenShift Host
<br>
<b>`vm_networking_openshift_verify_ssl`:</b> Verify SSL Certificate
<br>
<b>`vm_networking_request`:</b> List of network attachment requests
<br>
<b>`vm_networking_vms`:</b> >
<br>
<br>

### Vars

**These are variables with higher priority**

#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [vm_networking_valid_states](vars/main.yml#L3)   | list   | `[]` |
| [vm_networking_valid_states.0](vars/main.yml#L4)   | str   | `present` |
| [vm_networking_valid_states.1](vars/main.yml#L5)   | str   | `absent` |

### Tasks

#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Verify vm_networking_request Provided | `ansible.builtin.assert` | False |
| Validate Request States | `ansible.builtin.assert` | False |
| Initialize Variables | `ansible.builtin.set_fact` | True |
| Collect VMs | `ansible.builtin.include_role` | True |
| Process Network Attachments | `ansible.builtin.include_tasks` | False |

#### File: tasks/_attach_network.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| _attach_network ¦ Verify NAD Name Provided | `ansible.builtin.assert` | False |
| _attach_network ¦ Build Interface Name | `ansible.builtin.set_fact` | False |
| _attach_network ¦ Check Interface Not Already Attached | `ansible.builtin.set_fact` | False |
| _attach_network ¦ Build Network Entry | `ansible.builtin.set_fact` | True |
| _attach_network ¦ Build Interface Entry | `ansible.builtin.set_fact` | True |
| _attach_network ¦ Attach Network Interface | `kubernetes.core.k8s` | True |

#### File: tasks/_detach_network.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| _detach_network ¦ Verify NAD Name Provided | `ansible.builtin.assert` | False |
| _detach_network ¦ Build Interface Name | `ansible.builtin.set_fact` | False |
| _detach_network ¦ Check Interface Exists | `ansible.builtin.set_fact` | False |
| _detach_network ¦ Build Filtered Lists | `ansible.builtin.set_fact` | True |
| _detach_network ¦ Detach Network Interface | `kubernetes.core.k8s` | True |

## Task Flow Graphs

### Graph for _attach_network.yml

```mermaid
flowchart TD
Start
classDef block stroke:#3498db,stroke-width:2px;
classDef task stroke:#4b76bb,stroke-width:2px;
classDef includeTasks stroke:#16a085,stroke-width:2px;
classDef importTasks stroke:#34495e,stroke-width:2px;
classDef includeRole stroke:#2980b9,stroke-width:2px;
classDef importRole stroke:#699ba7,stroke-width:2px;
classDef includeVars stroke:#8e44ad,stroke-width:2px;
classDef rescue stroke:#665352,stroke-width:2px;

  Start-->|Task| _attach_network___Verify_NAD_Name_Provided0[ attach network   verify nad name provided]:::task
  _attach_network___Verify_NAD_Name_Provided0-->|Task| _attach_network___Build_Interface_Name1[ attach network   build interface name]:::task
  _attach_network___Build_Interface_Name1-->|Task| _attach_network___Check_Interface_Not_Already_Attached2[ attach network   check interface not already<br>attached]:::task
  _attach_network___Check_Interface_Not_Already_Attached2-->|Task| _attach_network___Build_Network_Entry3[ attach network   build network entry<br>When: **not  vm networking already attached   bool**]:::task
  _attach_network___Build_Network_Entry3-->|Task| _attach_network___Build_Interface_Entry4[ attach network   build interface entry<br>When: **not  vm networking already attached   bool**]:::task
  _attach_network___Build_Interface_Entry4-->|Task| _attach_network___Attach_Network_Interface5[ attach network   attach network interface<br>When: **not  vm networking already attached   bool**]:::task
  _attach_network___Attach_Network_Interface5-->End
```

### Graph for _detach_network.yml

```mermaid
flowchart TD
Start
classDef block stroke:#3498db,stroke-width:2px;
classDef task stroke:#4b76bb,stroke-width:2px;
classDef includeTasks stroke:#16a085,stroke-width:2px;
classDef importTasks stroke:#34495e,stroke-width:2px;
classDef includeRole stroke:#2980b9,stroke-width:2px;
classDef importRole stroke:#699ba7,stroke-width:2px;
classDef includeVars stroke:#8e44ad,stroke-width:2px;
classDef rescue stroke:#665352,stroke-width:2px;

  Start-->|Task| _detach_network___Verify_NAD_Name_Provided0[ detach network   verify nad name provided]:::task
  _detach_network___Verify_NAD_Name_Provided0-->|Task| _detach_network___Build_Interface_Name1[ detach network   build interface name]:::task
  _detach_network___Build_Interface_Name1-->|Task| _detach_network___Check_Interface_Exists2[ detach network   check interface exists]:::task
  _detach_network___Check_Interface_Exists2-->|Task| _detach_network___Build_Filtered_Lists3[ detach network   build filtered lists<br>When: **vm networking is attached   bool**]:::task
  _detach_network___Build_Filtered_Lists3-->|Task| _detach_network___Detach_Network_Interface4[ detach network   detach network interface<br>When: **vm networking is attached   bool**]:::task
  _detach_network___Detach_Network_Interface4-->End
```

### Graph for main.yml

```mermaid
flowchart TD
Start
classDef block stroke:#3498db,stroke-width:2px;
classDef task stroke:#4b76bb,stroke-width:2px;
classDef includeTasks stroke:#16a085,stroke-width:2px;
classDef importTasks stroke:#34495e,stroke-width:2px;
classDef includeRole stroke:#2980b9,stroke-width:2px;
classDef importRole stroke:#699ba7,stroke-width:2px;
classDef includeVars stroke:#8e44ad,stroke-width:2px;
classDef rescue stroke:#665352,stroke-width:2px;

  Start-->|Task| Verify_vm_networking_request_Provided0[verify vm networking request provided]:::task
  Verify_vm_networking_request_Provided0-->|Task| Validate_Request_States1[validate request states]:::task
  Validate_Request_States1-->|Task| Initialize_Variables2[initialize variables<br>When: **vm networking vms   length    0**]:::task
  Initialize_Variables2-->|Include role| Collect_VMs_infra_openshift_virtualization_ops_vm_collect_3(collect vms<br>When: **vm networking vms   length    0**<br>include_role: infra openshift virtualization ops vm collect):::includeRole
  Collect_VMs_infra_openshift_virtualization_ops_vm_collect_3-->|Include task| Process_Network_Attachments______attach_network_yml_____if__vm_networking_vm_state___default__present________present_____else___detach_network_yml_____4[process network attachments<br>include_task:      attach network yml     if  vm networking vm<br>state   default  present        present     else  <br>detach network yml    ]:::includeTasks
  Process_Network_Attachments______attach_network_yml_____if__vm_networking_vm_state___default__present________present_____else___detach_network_yml_____4-->End
```

## Playbook

```yml
---
- name: Test
  hosts: localhost
  remote_user: root
  roles:
    - vm_networking
...

```

## Playbook graph

```mermaid
flowchart TD
  hosts[localhost]-->|Role| vm_networking[vm networking]
```

## Author Information

OpenShift Virtualization Migration Contributors

## License

GPL-3.0-or-later

## Minimum Ansible Version

2.16

## Platforms

* **EL**: ['9']

<!-- DOCSIBLE END -->