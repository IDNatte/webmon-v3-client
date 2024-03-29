from wireguard_tools import WireguardDevice
from wireguard_tools import WireguardPeer

import subprocess
import threading
import platform
import datetime
import msgpack
import psutil
import socket
import json
import os


class SystemProberThread(threading.Thread):
    def __init__(self, output_dir, output_file):
        super().__init__()
        self.output_dir = output_dir
        self.output_file = output_file
        self.stop_event = threading.Event()

        if not os.path.isdir(self.output_dir):
            os.mkdir(os.path.join(os.path.abspath(output_dir)))

    def run(self):
        network = psutil.net_io_counters(pernic=True)
        wireguard = [device.interface for device in WireguardDevice.list()]
        with open(os.path.join(self.output_dir, self.output_file), "wb") as sys_probed:
            # running only if linux
            if platform.system() == "Linux":
                journal_prober = subprocess.run(
                    ["journalctl", "-n", "20", "-o", "json"],
                    capture_output=True,
                    text=True,
                )

                probe_result = journal_prober.stdout.strip().split("\n")
                journal = [json.loads(jour_prober) for jour_prober in probe_result]

            else:
                journal = []

            packed = msgpack.packb(
                {
                    "probe_time": f"{datetime.datetime.now()}",
                    "system_info": {
                        "net_info": [
                            {
                                "interface": net,
                                "receive": network.get(net).bytes_recv,
                                "transfer": network.get(net).bytes_sent,
                                "ip_addr": [
                                    net.address
                                    for net in psutil.net_if_addrs().get(net)
                                    if net.family == socket.AF_INET
                                ],
                            }
                            for net in network
                        ],
                        "hostname": socket.gethostname(),
                        "cpu": "",
                        "memory": "",
                        "wireguard": [
                            {
                                "peers": peer_key,
                                "last_handshake": WireguardPeer.asdict(peer).get(
                                    "last_handshake"
                                ),
                                "rx_bytes": WireguardPeer.asdict(peer).get("rx_bytes"),
                                "tx_bytes": WireguardPeer.asdict(peer).get("tx_bytes"),
                                "endpoint": WireguardPeer.asdict(peer).get(
                                    "endpoint_host"
                                ),
                                "port": WireguardPeer.asdict(peer).get("port"),
                            }
                            for wg_info in wireguard
                            for peer_key, peer in WireguardDevice.get(wg_info)
                            .get_config()
                            .peers.items()
                        ],
                    },
                    "application": {
                        "app_net_usage": [
                            {
                                "proc_name": psutil.Process(conn.pid).name(),
                                "pid": conn.pid,
                                "status": conn.status,
                                "address": {
                                    "local_address": conn.laddr[0],
                                    "local_port": conn.laddr[1],
                                    "remote_address": conn.raddr[0],
                                    "remote_port": conn.raddr[1],
                                },
                            }
                            for conn in psutil.net_connections()
                            if conn.status == psutil.CONN_ESTABLISHED
                        ],
                        "running_app": [
                            {
                                "proc_name": proc.info.get("name"),
                                "proc_info": proc.info,
                                "used_resource": {
                                    "cpu": psutil.Process(
                                        proc.info.get("pid")
                                    ).cpu_percent(),
                                    "mem": psutil.Process(
                                        proc.info.get("pid")
                                    ).memory_percent(memtype="rss"),
                                },
                            }
                            for proc in psutil.process_iter(["pid", "name", "username"])
                        ],
                    },
                    "journal_info": journal,
                }
            )

            sys_probed.write(packed)

    def stop(self):
        self.stop_event.set()
