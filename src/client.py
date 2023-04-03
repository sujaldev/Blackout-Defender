#!/usr/bin/python3

from __future__ import annotations

import json
import subprocess
from time import time
from datetime import timedelta

import psutil as ps


def parse_uptime_seconds(seconds: int | float) -> str:
    return str(timedelta(seconds=int(seconds)))


def item_uptime() -> str:
    return parse_uptime_seconds(time() - ps.boot_time())


def item_cpu() -> dict:
    return {
        "cores": ps.cpu_count(),
        "util": ps.cpu_percent(interval=0.4),
    }


def item_memory() -> dict:
    memory = ps.virtual_memory()
    total = memory.total
    return {
        "total": total,
        "util": total - memory.available
    }


def item_disks() -> list:
    return [{
        "device": partition.device,
        "mountpoint": partition.mountpoint,
        "total": (usage := ps.disk_usage(partition.mountpoint)).total,
        "util": usage.used,
    } for partition in ps.disk_partitions()]


def item_network() -> dict:
    net_stats = ps.net_io_counters()
    return {
        "bytes_in": net_stats.bytes_recv,
        "bytes_out": net_stats.bytes_sent,
    }


def item_thermals() -> dict:
    # TODO: This one is going to be a bit tricky.
    return {}


def item_vm() -> dict:
    is_proxmox_host = "pve" in subprocess.check_output(["uname", "-r"]).decode()
    if not is_proxmox_host:
        return {}

    node = "proxmox"  # TODO: auto-detect actual name, "proxmox" is just a guess.

    vms = {}
    for vm in json.loads(subprocess.check_output(
            ["pvesh", "get", f"/nodes/{node}/qemu", "--output-format", "json"]
    ).decode()):
        vms[f'{vm["name"]} ({vm["vmid"]})'] = {
            "status": vm["status"] == "running",
            "uptime": parse_uptime_seconds(vm["uptime"]),
            "cpu": {
                "cores": vm["cpus"],
            },
            "memory": {
                "total": vm["maxmem"],
                "util": vm["mem"],
            },
            "net": {
                "in": vm["netin"],
                "out": vm["netout"],
            }
        }
    return vms


def parse_items() -> dict:
    return {
        key.removeprefix("item_"): globals()[key]()
        for key in
        [f for f in globals().keys() if f.startswith("item_")]
    }


if __name__ == "__main__":
    print(parse_items())
