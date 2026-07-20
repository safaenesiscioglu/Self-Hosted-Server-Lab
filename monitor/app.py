"""
Self-Hosted Server Lab — lightweight system monitor.

A small Flask + psutil dashboard that reports live CPU / RAM / disk usage,
disk temperatures, the top running processes and (if the Docker socket is
available) running containers.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://<host>:5050
"""

import time

import psutil
from flask import Flask, jsonify, render_template

# Docker is optional — the monitor still works without it.
try:
    import docker

    _docker_client = docker.from_env()
except Exception:
    _docker_client = None

app = Flask(__name__)
PORT = 5050


def get_cpu():
    return {
        "percent": psutil.cpu_percent(interval=None),
        "per_core": psutil.cpu_percent(interval=None, percpu=True),
        "cores": psutil.cpu_count(logical=True),
    }


def get_memory():
    m = psutil.virtual_memory()
    return {
        "percent": m.percent,
        "used_gb": round(m.used / 1e9, 1),
        "total_gb": round(m.total / 1e9, 1),
    }


def get_disks():
    disks = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except (PermissionError, OSError):
            continue
        disks.append(
            {
                "mount": part.mountpoint,
                "fstype": part.fstype,
                "percent": usage.percent,
                "used_gb": round(usage.used / 1e9, 1),
                "total_gb": round(usage.total / 1e9, 1),
            }
        )
    return disks


def get_temps():
    """Disk / system temperatures where the platform exposes them."""
    temps = []
    fn = getattr(psutil, "sensors_temperatures", None)
    if not fn:
        return temps
    try:
        for name, entries in fn().items():
            for e in entries:
                if e.current:
                    temps.append(
                        {
                            "label": e.label or name,
                            "current": round(e.current, 1),
                        }
                    )
    except Exception:
        pass
    return temps


def get_top_processes(limit=10):
    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        info = p.info
        procs.append(
            {
                "pid": info["pid"],
                "name": info["name"],
                "cpu": round(info["cpu_percent"] or 0, 1),
                "mem": round(info["memory_percent"] or 0, 1),
            }
        )
    procs.sort(key=lambda x: x["cpu"], reverse=True)
    return procs[:limit]


def get_containers():
    if _docker_client is None:
        return []
    out = []
    try:
        for c in _docker_client.containers.list():
            out.append({"name": c.name, "status": c.status, "image": c.image.tags[:1]})
    except Exception:
        pass
    return out


@app.route("/api/stats")
def stats():
    return jsonify(
        {
            "timestamp": time.time(),
            "cpu": get_cpu(),
            "memory": get_memory(),
            "disks": get_disks(),
            "temps": get_temps(),
            "processes": get_top_processes(),
            "containers": get_containers(),
        }
    )


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # prime cpu_percent so the first reading isn't 0.0
    psutil.cpu_percent(interval=None, percpu=True)
    app.run(host="0.0.0.0", port=PORT)
