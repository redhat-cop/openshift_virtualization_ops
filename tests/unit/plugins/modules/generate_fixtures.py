#!/usr/bin/env python
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Generate RVTools test fixture files."""

import csv
import os

try:
    from openpyxl import Workbook
except ImportError:
    Workbook = None

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

VINFO_HEADERS = [
    "VM", "Powerstate", "Guest OS", "CPUs", "Memory", "NICs", "Disks",
    "Folder", "Resource pool", "Cluster", "Host", "Datacenter",
    "DNS Name", "Primary IP Address", "Annotation",
]
VINFO_ROW = [
    "web-server-01", "poweredOn", "Red Hat Enterprise Linux 9 (64-bit)",
    4, 8192, 2, 2, "Production/Web", "RP-Prod", "Cluster-01",
    "esxi-host-03.example.com", "DC-East",
    "web-server-01.example.com", "10.0.1.50", "Production web server",
]

VCPU_HEADERS = [
    "VM", "CPUs", "Sockets", "Cores per Socket",
    "CPU reservation [MHz]", "CPU limit [MHz]",
]
VCPU_ROW = ["web-server-01", 4, 2, 2, 0, -1]

VMEMORY_HEADERS = [
    "VM", "Size [MB]", "Reservation [MB]", "Limit [MB]", "Shares",
]
VMEMORY_ROW = ["web-server-01", 8192, 0, -1, 81920]

VDISK_HEADERS = [
    "VM", "Disk", "Capacity MB", "Thin", "Datastore", "Path",
]
VDISK_ROW = [
    "web-server-01", "Hard disk 1", 102400, True,
    "DS-SSD-01", "[DS-SSD-01] web-server-01/web-server-01.vmdk",
]

VNETWORK_HEADERS = [
    "VM", "Network Adapter", "Network", "Adapter Type",
    "MAC Address", "IP Address", "Connected",
]
VNETWORK_ROW = [
    "web-server-01", "Network adapter 1", "VLAN-100-Prod",
    "vmxnet3", "00:50:56:a1:b2:c3", "10.0.1.50", True,
]

TABS = {
    "vInfo": (VINFO_HEADERS, [VINFO_ROW]),
    "vCPU": (VCPU_HEADERS, [VCPU_ROW]),
    "vMemory": (VMEMORY_HEADERS, [VMEMORY_ROW]),
    "vDisk": (VDISK_HEADERS, [VDISK_ROW]),
    "vNetwork": (VNETWORK_HEADERS, [VNETWORK_ROW]),
}


def generate_xlsx():
    if Workbook is None:
        return
    wb = Workbook()
    first = True
    for tab_name, (headers, rows) in TABS.items():
        ws = wb.active if first else wb.create_sheet(tab_name)
        if first:
            ws.title = tab_name
            first = False
        ws.append(headers)
        for row in rows:
            ws.append(row)
    wb.save(os.path.join(FIXTURES_DIR, "rvtools_sample.xlsx"))


def generate_csv():
    for tab_name, (headers, rows) in TABS.items():
        filename = f"rvtools_{tab_name.lower()}.csv"
        with open(os.path.join(FIXTURES_DIR, filename), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)


if __name__ == "__main__":
    os.makedirs(FIXTURES_DIR, exist_ok=True)
    generate_xlsx()
    generate_csv()
