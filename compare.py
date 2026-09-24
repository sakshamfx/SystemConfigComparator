import json
import os


# ==========================================
# LOAD PROFILE
# ==========================================

def load_profile(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


# ==========================================
# DISPLAY COMPARISON
# ==========================================

def compare_systems(system_a, system_b):
    print()
    print("=" * 65)
    print("             SYSTEM CONFIGURATION COMPARISON")
    print("=" * 65)

    print()
    print(f"{'CATEGORY':<25}{system_a['computer_name']:<20}{system_b['computer_name']}")
    print("-" * 65)

    print(
        f"{'Operating System':<25}"
        f"{system_a['operating_system']:<20}"
        f"{system_b['operating_system']}"
    )

    print(
        f"{'CPU Cores':<25}"
        f"{system_a['cpu_cores']:<20}"
        f"{system_b['cpu_cores']}"
    )

    print(
        f"{'CPU Threads':<25}"
        f"{system_a['cpu_threads']:<20}"
        f"{system_b['cpu_threads']}"
    )

    print(
        f"{'CPU Frequency (MHz)':<25}"
        f"{system_a['cpu_frequency_mhz']:<20}"
        f"{system_b['cpu_frequency_mhz']}"
    )

    print(
        f"{'RAM (GB)':<25}"
        f"{system_a['total_ram_gb']:<20}"
        f"{system_b['total_ram_gb']}"
    )

    print(
        f"{'Storage Drives':<25}"
        f"{len(system_a['storage']):<20}"
        f"{len(system_b['storage'])}"
    )

    print(
        f"{'GPU Count':<25}"
        f"{len(system_a['gpu']):<20}"
        f"{len(system_b['gpu'])}"
    )

    print()
    print("-" * 65)
    print("CPU:")
    print("  System A:", system_a["processor"])
    print("  System B:", system_b["processor"])

    print()
    print("GPU:")
    print("  System A:", ", ".join(system_a["gpu"]))
    print("  System B:", ", ".join(system_b["gpu"]))

    print()
    print("STORAGE:")

    for drive in system_a["storage"]:
        print(
            "  System A:",
            drive["drive"],
            "-",
            drive["total_gb"],
            "GB"
        )

    for drive in system_b["storage"]:
        print(
            "  System B:",
            drive["drive"],
            "-",
            drive["total_gb"],
            "GB"
        )

    print()
    print("=" * 65)


# ==========================================
# MAIN PROGRAM
# ==========================================

profiles_folder = "profiles"

system_a_file = os.path.join(
    profiles_folder,
    "TARS_profile.json"
)

system_b_file = os.path.join(
    profiles_folder,
    "TEST_PC_profile.json"
)

system_a = load_profile(system_a_file)
system_b = load_profile(system_b_file)

compare_systems(system_a, system_b)