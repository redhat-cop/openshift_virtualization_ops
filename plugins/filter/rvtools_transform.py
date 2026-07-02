# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Filter plugin to transform parsed RVTools data into role request formats."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
name: rvtools_transform
short_description: Transform parsed RVTools data into role request formats
version_added: "1.1.0"
description:
  - Collection of filters that convert parsed RVTools inventory data
    into request formats consumed by openshift_virtualization_ops roles.
author:
  - OpenShift Virtualization Migration Contributors
"""

import re


def _sanitize_k8s_name(name):
    """Convert a VM name to a valid Kubernetes resource name."""
    sanitized = re.sub(r"[^a-z0-9-]", "-", name.lower())
    sanitized = re.sub(r"-+", "-", sanitized).strip("-")
    return sanitized[:253]


def _group_by_vm(records):
    """Group a list of records by vm_name."""
    grouped = {}
    for rec in records:
        vm_name = rec.get("vm_name", "")
        if vm_name:
            grouped.setdefault(vm_name, []).append(rec)
    return grouped


def rvtools_to_hot_plug(parsed, namespace):
    """Transform parsed RVTools data into vm_hot_plug_request format.

    Args:
        parsed: Dict from rvtools_parse module return.
        namespace: Target OCP namespace for the VMs.

    Returns:
        List of vm_hot_plug_request entries.
    """
    vinfo = parsed.get("vinfo", [])
    vcpu_map = {r["vm_name"]: r for r in parsed.get("vcpu", [])}
    vmem_map = {r["vm_name"]: r for r in parsed.get("vmemory", [])}

    requests = []
    for vm in vinfo:
        vm_name = vm.get("vm_name", "")
        if not vm_name:
            continue

        cpu_info = vcpu_map.get(vm_name, {})
        cores = cpu_info.get("cpus", vm.get("cpus", 0))

        mem_info = vmem_map.get(vm_name, {})
        memory_mb = mem_info.get("size_mb", vm.get("memory_mb", 0))

        request = {
            "namespace": namespace,
            "names": [_sanitize_k8s_name(vm_name)],
            "compute": {
                "cpu": {"cores": cores},
                "memory": f"{memory_mb}Mi",
            },
        }
        requests.append(request)

    return requests


def rvtools_to_lifecycle(parsed, namespace, target_state="running"):
    """Transform parsed RVTools data into vm_lifecycle_vm_operations_request format.

    Args:
        parsed: Dict from rvtools_parse module return.
        namespace: Target OCP namespace.
        target_state: Desired state — 'running' or 'stopped'.

    Returns:
        List of vm_lifecycle_vm_operations_request entries.
    """
    vinfo = parsed.get("vinfo", [])

    state_op_map = {
        "running": {"needs_action": "poweredOff", "operation": "start"},
        "stopped": {"needs_action": "poweredOn", "operation": "stop"},
    }

    mapping = state_op_map.get(target_state)
    if not mapping:
        return []

    names = [
        _sanitize_k8s_name(vm["vm_name"])
        for vm in vinfo
        if vm.get("power_state") == mapping["needs_action"] and vm.get("vm_name")
    ]

    if not names:
        return []

    return [{
        "operation": mapping["operation"],
        "namespace": namespace,
        "names": names,
    }]


def rvtools_to_storage_labels(parsed, namespace):
    """Transform parsed RVTools vDisk data into vm_storage_labeling_request format.

    Args:
        parsed: Dict from rvtools_parse module return.
        namespace: Target OCP namespace.

    Returns:
        List of vm_storage_labeling_request entries.
    """
    vdisk = parsed.get("vdisk", [])
    by_datastore = {}
    for disk in vdisk:
        ds = disk.get("datastore", "unknown")
        vm_name = disk.get("vm_name", "")
        if vm_name:
            by_datastore.setdefault(ds, set()).add(_sanitize_k8s_name(vm_name))

    requests = []
    for datastore, vm_names in by_datastore.items():
        requests.append({
            "namespace": namespace,
            "label_selectors": [
                f"vm.kubevirt.io/name in ({','.join(sorted(vm_names))})"
            ],
            "labels": {
                "rvtools.vmware/source-datastore": _sanitize_k8s_name(datastore),
            },
            "annotations": {
                "rvtools.vmware/source-datastore": datastore,
            },
        })

    return requests


def rvtools_to_networking(parsed, namespace, nad_map=None):
    """Transform parsed RVTools vNetwork data into vm_networking_request format.

    Args:
        parsed: Dict from rvtools_parse module return.
        namespace: Target OCP namespace.
        nad_map: Dict mapping VMware network names to OCP NAD names.

    Returns:
        List of vm_networking_request entries.
    """
    if nad_map is None:
        nad_map = {}

    vnetwork = parsed.get("vnetwork", [])
    requests = []

    for nic in vnetwork:
        vm_name = nic.get("vm_name", "")
        network_name = nic.get("network_name", "")
        if not vm_name or not network_name:
            continue

        nad_name = nad_map.get(network_name, _sanitize_k8s_name(network_name))

        requests.append({
            "namespace": namespace,
            "names": [_sanitize_k8s_name(vm_name)],
            "nad_name": nad_name,
            "source_network": network_name,
            "mac_address": nic.get("mac_address"),
            "adapter_type": nic.get("adapter_type"),
        })

    return requests


def rvtools_to_vm_specs(parsed, namespace, storage_class, nad_map=None):
    """Transform parsed RVTools data into KubeVirt VirtualMachine spec dicts.

    Args:
        parsed: Dict from rvtools_parse module return.
        namespace: Target OCP namespace.
        storage_class: StorageClass name for PVCs.
        nad_map: Dict mapping VMware network names to OCP NAD names.

    Returns:
        List of KubeVirt VirtualMachine resource dicts.
    """
    if nad_map is None:
        nad_map = {}

    vinfo = parsed.get("vinfo", [])
    vcpu_map = {r["vm_name"]: r for r in parsed.get("vcpu", [])}
    vmem_map = {r["vm_name"]: r for r in parsed.get("vmemory", [])}
    vdisk_grouped = _group_by_vm(parsed.get("vdisk", []))
    vnet_grouped = _group_by_vm(parsed.get("vnetwork", []))

    specs = []
    for vm in vinfo:
        vm_name = vm.get("vm_name", "")
        if not vm_name:
            continue

        k8s_name = _sanitize_k8s_name(vm_name)
        cpu_info = vcpu_map.get(vm_name, {})
        cores = cpu_info.get("cpus", vm.get("cpus", 1))
        sockets = cpu_info.get("sockets", 1)

        mem_info = vmem_map.get(vm_name, {})
        memory_mb = mem_info.get("size_mb", vm.get("memory_mb", 1024))

        disks = vdisk_grouped.get(vm_name, [])
        if not disks:
            continue
        networks = vnet_grouped.get(vm_name, [])

        volumes = []
        disk_devices = []
        for idx, disk in enumerate(disks):
            disk_name = f"disk-{idx}"
            disk_devices.append({
                "name": disk_name,
                "disk": {"bus": "virtio"},
            })
            volumes.append({
                "name": disk_name,
                "dataVolume": {"name": f"{k8s_name}-{disk_name}"},
            })

        interfaces = []
        net_entries = []
        for idx, net in enumerate(networks):
            net_name = f"nic-{idx}"
            network_name = net.get("network_name", "")
            nad = nad_map.get(network_name, _sanitize_k8s_name(network_name))

            interfaces.append({
                "name": net_name,
                "bridge": {},
            })
            net_entries.append({
                "name": net_name,
                "multus": {"networkName": nad},
            })

        if not interfaces:
            interfaces.append({"name": "default", "masquerade": {}})
            net_entries.append({"name": "default", "pod": {}})

        running = vm.get("power_state") == "poweredOn"

        spec = {
            "apiVersion": "kubevirt.io/v1",
            "kind": "VirtualMachine",
            "metadata": {
                "name": k8s_name,
                "namespace": namespace,
                "labels": {
                    "rvtools.vmware/source-vm": k8s_name,
                    "rvtools.vmware/source-folder": _sanitize_k8s_name(
                        vm.get("folder", "")
                    ),
                    "rvtools.vmware/source-cluster": _sanitize_k8s_name(
                        vm.get("cluster", "")
                    ),
                },
                "annotations": {
                    "rvtools.vmware/source-host": vm.get("host", ""),
                    "rvtools.vmware/guest-os": vm.get("guest_os", ""),
                    "rvtools.vmware/source-datacenter": vm.get("datacenter", ""),
                },
            },
            "spec": {
                "running": running,
                "template": {
                    "metadata": {
                        "labels": {
                            "vm.kubevirt.io/name": k8s_name,
                        },
                    },
                    "spec": {
                        "domain": {
                            "cpu": {
                                "cores": cores,
                                "sockets": sockets,
                            },
                            "resources": {
                                "requests": {
                                    "memory": f"{memory_mb}Mi",
                                },
                            },
                            "devices": {
                                "disks": disk_devices,
                                "interfaces": interfaces,
                            },
                        },
                        "networks": net_entries,
                        "volumes": volumes,
                    },
                },
                "dataVolumeTemplates": [
                    {
                        "metadata": {
                            "name": f"{k8s_name}-disk-{idx}",
                        },
                        "spec": {
                            "storage": {
                                "accessModes": ["ReadWriteOnce"],
                                "resources": {
                                    "requests": {
                                        "storage": "{}Gi".format(
                                            max(1, disk.get("capacity_mb", 10240) // 1024)
                                        ),
                                    },
                                },
                                "storageClassName": storage_class,
                            },
                        },
                    }
                    for idx, disk in enumerate(disks)
                ],
            },
        }

        specs.append(spec)

    return specs


class FilterModule:
    """Ansible filter plugin for RVTools data transformation."""

    def filters(self):
        return {
            "rvtools_to_hot_plug": rvtools_to_hot_plug,
            "rvtools_to_lifecycle": rvtools_to_lifecycle,
            "rvtools_to_storage_labels": rvtools_to_storage_labels,
            "rvtools_to_networking": rvtools_to_networking,
            "rvtools_to_vm_specs": rvtools_to_vm_specs,
        }
