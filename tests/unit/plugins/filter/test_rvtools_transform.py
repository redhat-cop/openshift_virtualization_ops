# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for rvtools_transform filter plugin."""

import pytest


SAMPLE_PARSED = {
    "vinfo": [
        {
            "vm_name": "web-01",
            "power_state": "poweredOn",
            "guest_os": "Red Hat Enterprise Linux 9 (64-bit)",
            "cpus": 4,
            "memory_mb": 8192,
            "nics": 2,
            "disks": 2,
            "folder": "Production/Web",
            "resource_pool": "RP-Prod",
            "cluster": "Cluster-01",
            "host": "esxi-03.example.com",
            "datacenter": "DC-East",
            "dns_name": "web-01.example.com",
            "primary_ip": "10.0.1.50",
            "annotation": "Production web server",
        },
        {
            "vm_name": "db-01",
            "power_state": "poweredOff",
            "guest_os": "Red Hat Enterprise Linux 8 (64-bit)",
            "cpus": 8,
            "memory_mb": 32768,
            "nics": 1,
            "disks": 3,
            "folder": "Production/DB",
            "resource_pool": "RP-Prod",
            "cluster": "Cluster-01",
            "host": "esxi-01.example.com",
            "datacenter": "DC-East",
            "dns_name": "db-01.example.com",
            "primary_ip": "10.0.2.10",
            "annotation": "Database server",
        },
    ],
    "vcpu": [
        {"vm_name": "web-01", "cpus": 4, "sockets": 2, "cores_per_socket": 2,
         "cpu_reservation_mhz": 0, "cpu_limit_mhz": -1},
        {"vm_name": "db-01", "cpus": 8, "sockets": 4, "cores_per_socket": 2,
         "cpu_reservation_mhz": 0, "cpu_limit_mhz": -1},
    ],
    "vmemory": [
        {"vm_name": "web-01", "size_mb": 8192, "reservation_mb": 0,
         "limit_mb": -1, "shares": 81920},
        {"vm_name": "db-01", "size_mb": 32768, "reservation_mb": 0,
         "limit_mb": -1, "shares": 327680},
    ],
    "vdisk": [
        {"vm_name": "web-01", "disk_name": "Hard disk 1",
         "capacity_mb": 102400, "thin": True,
         "datastore": "DS-SSD-01",
         "path": "[DS-SSD-01] web-01/web-01.vmdk"},
        {"vm_name": "db-01", "disk_name": "Hard disk 1",
         "capacity_mb": 204800, "thin": False,
         "datastore": "DS-SAN-01",
         "path": "[DS-SAN-01] db-01/db-01.vmdk"},
    ],
    "vnetwork": [
        {"vm_name": "web-01", "nic_name": "Network adapter 1",
         "network_name": "VLAN-100-Prod", "adapter_type": "vmxnet3",
         "mac_address": "00:50:56:a1:b2:c3", "ip_address": "10.0.1.50",
         "connected": True},
        {"vm_name": "db-01", "nic_name": "Network adapter 1",
         "network_name": "VLAN-200-DB", "adapter_type": "vmxnet3",
         "mac_address": "00:50:56:d4:e5:f6", "ip_address": "10.0.2.10",
         "connected": True},
    ],
}


class TestRvtoolsToHotPlug:
    def test_generates_hot_plug_request(self):
        from plugins.filter.rvtools_transform import rvtools_to_hot_plug

        result = rvtools_to_hot_plug(SAMPLE_PARSED, namespace="vm-prod")
        assert len(result) == 2
        assert result[0]["namespace"] == "vm-prod"
        assert result[0]["names"] == ["web-01"]
        assert result[0]["compute"]["cpu"]["cores"] == 4
        assert result[0]["compute"]["memory"] == "8192Mi"


class TestRvtoolsToLifecycle:
    def test_start_powered_off_vms(self):
        from plugins.filter.rvtools_transform import rvtools_to_lifecycle

        result = rvtools_to_lifecycle(
            SAMPLE_PARSED, namespace="vm-prod", target_state="running"
        )
        # Only db-01 is poweredOff, so only it needs a start
        assert len(result) == 1
        assert result[0]["operation"] == "start"
        assert result[0]["names"] == ["db-01"]

    def test_stop_powered_on_vms(self):
        from plugins.filter.rvtools_transform import rvtools_to_lifecycle

        result = rvtools_to_lifecycle(
            SAMPLE_PARSED, namespace="vm-prod", target_state="stopped"
        )
        assert len(result) == 1
        assert result[0]["operation"] == "stop"
        assert result[0]["names"] == ["web-01"]


class TestRvtoolsToStorageLabels:
    def test_generates_storage_labels(self):
        from plugins.filter.rvtools_transform import rvtools_to_storage_labels

        result = rvtools_to_storage_labels(SAMPLE_PARSED, namespace="vm-prod")
        assert len(result) >= 1
        first = result[0]
        assert "labels" in first
        assert first["labels"]["rvtools.vmware/source-datastore"] == "ds-ssd-01"


class TestRvtoolsToNetworking:
    def test_generates_networking_request(self):
        from plugins.filter.rvtools_transform import rvtools_to_networking

        nad_map = {
            "VLAN-100-Prod": "prod-net-attach",
            "VLAN-200-DB": "db-net-attach",
        }
        result = rvtools_to_networking(
            SAMPLE_PARSED, namespace="vm-prod", nad_map=nad_map
        )
        assert len(result) == 2
        assert result[0]["namespace"] == "vm-prod"
        assert result[0]["nad_name"] == "prod-net-attach"


class TestRvtoolsToVmSpecs:
    def test_generates_vm_specs(self):
        from plugins.filter.rvtools_transform import rvtools_to_vm_specs

        nad_map = {"VLAN-100-Prod": "prod-net-attach", "VLAN-200-DB": "db-net-attach"}
        result = rvtools_to_vm_specs(
            SAMPLE_PARSED,
            namespace="vm-prod",
            storage_class="ocs-storagecluster-ceph-rbd",
            nad_map=nad_map,
        )
        assert len(result) == 2
        spec = result[0]
        assert spec["metadata"]["name"] == "web-01"
        assert spec["metadata"]["namespace"] == "vm-prod"
        domain = spec["spec"]["template"]["spec"]["domain"]
        assert domain["cpu"]["cores"] == 4
        assert domain["resources"]["requests"]["memory"] == "8192Mi"
