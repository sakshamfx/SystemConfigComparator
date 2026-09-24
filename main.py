import platform
import psutil
import subprocess
import json
import os
from datetime import datetime


# ==========================================
# SYSTEM CONFIGURATION COMPARATOR
# System Information Scanner
# ==========================================

system_info = {}


# ==========================================
# BASIC SYSTEM INFORMATION
# ==========================================

system_info["computer_name"] = platform.node()
system_info["operating_system"] = platform.system()
system_info["os_version"] = platform.version()
system_info["architecture"] = platform.machine()
system_info["processor"] = platform.processor()


# ==========================================
# CPU INFORMATION
# ==========================================

system_info["cpu_cores"] = psutil.cpu_count(logical=False)
system_info["cpu_threads"] = psutil.cpu_count(logical=True)

cpu_frequency = psutil.cpu_freq()

if cpu_frequency:
    system_info["cpu_frequency_mhz"] = round(cpu_frequency.current, 2)
else:
    system_info["cpu_frequency_mhz"] = None

system_info["cpu_usage_percent"] = psutil.cpu_percent(interval=1)


# ==========================================
# RAM INFORMATION
# ==========================================

ram = psutil.virtual_memory()

system_info["total_ram_gb"] = round(ram.total / (1024 ** 3), 2)
system_info["used_ram_gb"] = round(ram.used / (1024 ** 3), 2)
system_info["available_ram_gb"] = round(ram.available / (1024 ** 3), 2)
system_info["ram_usage_percent"] = ram.percent


# ==========================================
# STORAGE INFORMATION
# ==========================================

system_info["storage"] = []

partitions = psutil.disk_partitions()

for partition in partitions:
    try:
        usage = psutil.disk_usage(partition.mountpoint)

        drive_info = {
            "drive": partition.device,
            "mountpoint": partition.mountpoint,
            "filesystem": partition.fstype,
            "total_gb": round(usage.total / (1024 ** 3), 2),
            "used_gb": round(usage.used / (1024 ** 3), 2),
            "free_gb": round(usage.free / (1024 ** 3), 2),
            "usage_percent": usage.percent
        }

        system_info["storage"].append(drive_info)

    except (PermissionError, OSError):
        pass


# ==========================================
# GPU INFORMATION
# ==========================================

system_info["gpu"] = []

try:
    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-CimInstance Win32_VideoController | "
            "Select-Object -ExpandProperty Name"
        ],
        capture_output=True,
        text=True,
        timeout=10
    )

    gpu_output = result.stdout.strip()

    if gpu_output:
        gpu_names = gpu_output.splitlines()

        for gpu in gpu_names:
            gpu = gpu.strip()

            if gpu and gpu not in system_info["gpu"]:
                system_info["gpu"].append(gpu)

except Exception as e:
    system_info["gpu_error"] = str(e)


# ==========================================
# ADD SCAN TIME
# ==========================================

system_info["scan_time"] = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)


# ==========================================
# SAVE SYSTEM PROFILE
# ==========================================

profiles_folder = "profiles"

os.makedirs(profiles_folder, exist_ok=True)

filename = system_info["computer_name"] + "_profile.json"
filepath = os.path.join(profiles_folder, filename)

with open(filepath, "w") as file:
    json.dump(system_info, file, indent=4)


# ==========================================
# DISPLAY SYSTEM INFORMATION
# ==========================================

print()
print("=" * 50)
print("       SYSTEM CONFIGURATION REPORT")
print("=" * 50)

print()
print("BASIC SYSTEM INFORMATION")
print("-" * 30)

print("Computer Name :", system_info["computer_name"])
print("Operating System :", system_info["operating_system"])
print("OS Version :", system_info["os_version"])
print("Architecture :", system_info["architecture"])
print("Processor :", system_info["processor"])


print()
print("CPU INFORMATION")
print("-" * 30)

print("CPU Cores :", system_info["cpu_cores"])
print("CPU Threads :", system_info["cpu_threads"])
print("CPU Frequency :", system_info["cpu_frequency_mhz"], "MHz")
print("CPU Usage :", system_info["cpu_usage_percent"], "%")


print()
print("RAM INFORMATION")
print("-" * 30)

print("Total RAM :", system_info["total_ram_gb"], "GB")
print("Used RAM :", system_info["used_ram_gb"], "GB")
print("Available RAM :", system_info["available_ram_gb"], "GB")
print("RAM Usage :", system_info["ram_usage_percent"], "%")


print()
print("STORAGE INFORMATION")
print("-" * 30)

for drive in system_info["storage"]:
    print()
    print("Drive :", drive["drive"])
    print("File System :", drive["filesystem"])
    print("Total :", drive["total_gb"], "GB")
    print("Used :", drive["used_gb"], "GB")
    print("Free :", drive["free_gb"], "GB")
    print("Usage :", drive["usage_percent"], "%")


print()
print("GPU INFORMATION")
print("-" * 30)

for gpu in system_info["gpu"]:
    print("-", gpu)


print()
print("=" * 50)
print("SYSTEM PROFILE SAVED")
print("=" * 50)

print()
print("File:", filepath)
print("Scan Time:", system_info["scan_time"])
print()
print("Scanner completed successfully.")