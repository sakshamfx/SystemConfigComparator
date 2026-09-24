import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import platform
import psutil
import subprocess
from datetime import datetime


# ==========================================
# LOAD PROFILE
# ==========================================

def load_profile(filepath):
    try:
        with open(filepath, "r") as file:
            return json.load(file)

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Could not load profile:\n{e}"
        )
        return None


# ==========================================
# SCAN CURRENT COMPUTER
# ==========================================

def scan_current_pc():

    system_info = {}

    # --------------------------------------
    # BASIC SYSTEM INFORMATION
    # --------------------------------------

    system_info["computer_name"] = platform.node()
    system_info["operating_system"] = platform.system()
    system_info["os_version"] = platform.version()
    system_info["architecture"] = platform.machine()

    # Get actual CPU name using PowerShell
    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_Processor | "
                "Select-Object -ExpandProperty Name"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        cpu_name = result.stdout.strip()

        if cpu_name:
            system_info["processor"] = cpu_name
        else:
            system_info["processor"] = platform.processor()

    except Exception:
        system_info["processor"] = platform.processor()

    # --------------------------------------
    # CPU INFORMATION
    # --------------------------------------

    system_info["cpu_cores"] = psutil.cpu_count(
        logical=False
    )

    system_info["cpu_threads"] = psutil.cpu_count(
        logical=True
    )

    cpu_frequency = psutil.cpu_freq()

    if cpu_frequency:
        system_info["cpu_frequency_mhz"] = round(
            cpu_frequency.current,
            2
        )
    else:
        system_info["cpu_frequency_mhz"] = None

    system_info["cpu_usage_percent"] = psutil.cpu_percent(
        interval=1
    )

    # --------------------------------------
    # RAM INFORMATION
    # --------------------------------------

    ram = psutil.virtual_memory()

    system_info["total_ram_gb"] = round(
        ram.total / (1024 ** 3),
        2
    )

    system_info["used_ram_gb"] = round(
        ram.used / (1024 ** 3),
        2
    )

    system_info["available_ram_gb"] = round(
        ram.available / (1024 ** 3),
        2
    )

    system_info["ram_usage_percent"] = ram.percent

    # --------------------------------------
    # STORAGE INFORMATION
    # --------------------------------------

    system_info["storage"] = []

    partitions = psutil.disk_partitions()

    for partition in partitions:

        try:
            usage = psutil.disk_usage(
                partition.mountpoint
            )

            drive_info = {
                "drive": partition.device,
                "mountpoint": partition.mountpoint,
                "filesystem": partition.fstype,
                "total_gb": round(
                    usage.total / (1024 ** 3),
                    2
                ),
                "used_gb": round(
                    usage.used / (1024 ** 3),
                    2
                ),
                "free_gb": round(
                    usage.free / (1024 ** 3),
                    2
                ),
                "usage_percent": usage.percent
            }

            system_info["storage"].append(
                drive_info
            )

        except (PermissionError, OSError):
            pass

    # --------------------------------------
    # GPU INFORMATION
    # --------------------------------------

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

    # --------------------------------------
    # SCAN TIME
    # --------------------------------------

    system_info["scan_time"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # --------------------------------------
    # SAVE PROFILE
    # --------------------------------------

    profiles_folder = "profiles"

    os.makedirs(
        profiles_folder,
        exist_ok=True
    )

    filename = (
        system_info["computer_name"]
        + "_profile.json"
    )

    filepath = os.path.join(
        profiles_folder,
        filename
    )

    with open(filepath, "w") as file:

        json.dump(
            system_info,
            file,
            indent=4
        )

    return system_info, filepath


# ==========================================
# FORMAT SYSTEM INFORMATION
# ==========================================

def get_system_summary(system):

    storage_total = sum(
        drive["total_gb"]
        for drive in system.get(
            "storage",
            []
        )
    )

    return {

        "Computer":
            system.get(
                "computer_name",
                "Unknown"
            ),

        "Operating System":
            system.get(
                "operating_system",
                "Unknown"
            ),

        "Processor":
            system.get(
                "processor",
                "Unknown"
            ),

        "CPU Cores":
            system.get(
                "cpu_cores",
                "Unknown"
            ),

        "CPU Threads":
            system.get(
                "cpu_threads",
                "Unknown"
            ),

        "CPU Frequency":
            str(
                system.get(
                    "cpu_frequency_mhz",
                    "Unknown"
                )
            ) + " MHz",

        "RAM":
            str(
                system.get(
                    "total_ram_gb",
                    "Unknown"
                )
            ) + " GB",

        "Storage":
            str(
                round(
                    storage_total,
                    2
                )
            ) + " GB",

        "GPU":
            ", ".join(
                system.get(
                    "gpu",
                    []
                )
            )
    }


# ==========================================
# DISPLAY SYSTEM
# ==========================================

def display_system(system):

    if not system:
        return

    summary = get_system_summary(system)

    for widget in system_text.winfo_children():
        widget.destroy()

    for key, value in summary.items():

        row = tk.Frame(
            system_text,
            bg="#1e1e1e"
        )

        row.pack(
            fill="x",
            padx=10,
            pady=5
        )

        label = tk.Label(
            row,
            text=key + ":",
            width=18,
            anchor="w",
            bg="#1e1e1e",
            fg="#aaaaaa",
            font=(
                "Arial",
                10,
                "bold"
            )
        )

        label.pack(
            side="left"
        )

        value_label = tk.Label(
            row,
            text=value,
            anchor="w",
            justify="left",
            wraplength=600,
            bg="#1e1e1e",
            fg="white",
            font=(
                "Arial",
                10
            )
        )

        value_label.pack(
            side="left",
            fill="x",
            expand=True
        )


# ==========================================
# SCAN BUTTON
# ==========================================

def scan_pc_button():

    try:

        root.config(
            cursor="watch"
        )

        root.update()

        system, filepath = scan_current_pc()

        display_system(system)

        loaded_system.set(
            "Scanned: "
            + system["computer_name"]
        )

        messagebox.showinfo(
            "Scan Complete",
            "System scan completed successfully!\n\n"
            "Profile saved to:\n"
            + filepath
        )

    except Exception as e:

        messagebox.showerror(
            "Scan Error",
            f"Could not scan the computer:\n{e}"
        )

    finally:

        root.config(
            cursor=""
        )


# ==========================================
# LOAD PROFILE BUTTON
# ==========================================

def load_profile_button():

    filepath = filedialog.askopenfilename(

        title="Select System Profile",

        filetypes=[
            (
                "JSON Files",
                "*.json"
            ),
            (
                "All Files",
                "*.*"
            )
        ]
    )

    if filepath:

        system = load_profile(filepath)

        if system:

            display_system(system)

            loaded_system.set(
                "Loaded: "
                + system.get(
                    "computer_name",
                    "Unknown"
                )
            )


# ==========================================
# COMPARE SYSTEMS
# ==========================================

def compare_systems():

    file_a = filedialog.askopenfilename(

        title="Select First System Profile",

        filetypes=[
            (
                "JSON Files",
                "*.json"
            )
        ]
    )

    if not file_a:
        return

    file_b = filedialog.askopenfilename(

        title="Select Second System Profile",

        filetypes=[
            (
                "JSON Files",
                "*.json"
            )
        ]
    )

    if not file_b:
        return

    system_a = load_profile(file_a)

    system_b = load_profile(file_b)

    if not system_a or not system_b:
        return

    comparison_window = tk.Toplevel(root)

    comparison_window.title(
        "System Configuration Comparison"
    )

    comparison_window.geometry(
        "1000x650"
    )

    comparison_window.configure(
        bg="#121212"
    )

    title = tk.Label(

        comparison_window,

        text="SYSTEM CONFIGURATION COMPARISON",

        bg="#121212",

        fg="white",

        font=(
            "Arial",
            20,
            "bold"
        )
    )

    title.pack(
        pady=20
    )

    frame = tk.Frame(
        comparison_window,
        bg="#121212"
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    summary_a = get_system_summary(
        system_a
    )

    summary_b = get_system_summary(
        system_b
    )

    name_a = system_a.get(
        "computer_name",
        "System A"
    )

    name_b = system_b.get(
        "computer_name",
        "System B"
    )

    headers = [
        "CATEGORY",
        name_a,
        name_b
    ]

    for column, text in enumerate(headers):

        label = tk.Label(

            frame,

            text=text,

            bg="#252525",

            fg="white",

            font=(
                "Arial",
                11,
                "bold"
            ),

            padx=10,

            pady=10
        )

        label.grid(

            row=0,

            column=column,

            sticky="nsew",

            padx=1,

            pady=1
        )

    categories = list(
        summary_a.keys()
    )

    for row_number, category in enumerate(
        categories,
        start=1
    ):

        value_a = summary_a[category]

        value_b = summary_b[category]

        category_label = tk.Label(

            frame,

            text=category,

            bg="#1e1e1e",

            fg="#aaaaaa",

            font=(
                "Arial",
                10,
                "bold"
            ),

            anchor="w",

            padx=10
        )

        category_label.grid(

            row=row_number,

            column=0,

            sticky="nsew",

            padx=1,

            pady=1
        )

        # Highlight differences

        if str(value_a) != str(value_b):

            color_a = "#4a3b20"
            color_b = "#4a3b20"

        else:

            color_a = "#1e1e1e"
            color_b = "#1e1e1e"

        label_a = tk.Label(

            frame,

            text=value_a,

            bg=color_a,

            fg="white",

            wraplength=300,

            justify="left",

            anchor="w",

            padx=10
        )

        label_a.grid(

            row=row_number,

            column=1,

            sticky="nsew",

            padx=1,

            pady=1
        )

        label_b = tk.Label(

            frame,

            text=value_b,

            bg=color_b,

            fg="white",

            wraplength=300,

            justify="left",

            anchor="w",

            padx=10
        )

        label_b.grid(

            row=row_number,

            column=2,

            sticky="nsew",

            padx=1,

            pady=1
        )

    for column in range(3):

        frame.grid_columnconfigure(
            column,
            weight=1
        )


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title(
    "System Configuration Comparator"
)

root.geometry(
    "900x700"
)

root.configure(
    bg="#121212"
)


# ==========================================
# TITLE
# ==========================================

title = tk.Label(

    root,

    text="SYSTEM CONFIGURATION COMPARATOR",

    bg="#121212",

    fg="white",

    font=(
        "Arial",
        24,
        "bold"
    )
)

title.pack(
    pady=(30, 5)
)


subtitle = tk.Label(

    root,

    text="Scan, save and compare computer configurations",

    bg="#121212",

    fg="#aaaaaa",

    font=(
        "Arial",
        11
    )
)

subtitle.pack(
    pady=(0, 25)
)


# ==========================================
# BUTTONS
# ==========================================

button_frame = tk.Frame(

    root,

    bg="#121212"
)

button_frame.pack(
    pady=10
)


# SCAN BUTTON

scan_button = tk.Button(

    button_frame,

    text="SCAN THIS PC",

    command=scan_pc_button,

    width=20,

    height=2,

    bg="#333333",

    fg="white",

    activebackground="#444444",

    activeforeground="white",

    font=(
        "Arial",
        10,
        "bold"
    )
)

scan_button.grid(

    row=0,

    column=0,

    padx=8
)


# LOAD BUTTON

load_button = tk.Button(

    button_frame,

    text="LOAD SYSTEM PROFILE",

    command=load_profile_button,

    width=20,

    height=2,

    bg="#333333",

    fg="white",

    activebackground="#444444",

    activeforeground="white",

    font=(
        "Arial",
        10,
        "bold"
    )
)

load_button.grid(

    row=0,

    column=1,

    padx=8
)


# COMPARE BUTTON

compare_button = tk.Button(

    button_frame,

    text="COMPARE TWO SYSTEMS",

    command=compare_systems,

    width=20,

    height=2,

    bg="#333333",

    fg="white",

    activebackground="#444444",

    activeforeground="white",

    font=(
        "Arial",
        10,
        "bold"
    )
)

compare_button.grid(

    row=0,

    column=2,

    padx=8
)


# ==========================================
# STATUS
# ==========================================

loaded_system = tk.StringVar()

loaded_system.set(
    "No profile loaded"
)

status_label = tk.Label(

    root,

    textvariable=loaded_system,

    bg="#121212",

    fg="#aaaaaa",

    font=(
        "Arial",
        10
    )
)

status_label.pack(
    pady=10
)


# ==========================================
# SYSTEM INFORMATION AREA
# ==========================================

system_frame = tk.Frame(

    root,

    bg="#1e1e1e",

    bd=1,

    relief="solid"
)

system_frame.pack(

    fill="both",

    expand=True,

    padx=40,

    pady=20
)


system_text = tk.Frame(

    system_frame,

    bg="#1e1e1e"
)

system_text.pack(

    fill="both",

    expand=True,

    pady=15
)


# ==========================================
# START APPLICATION
# ==========================================

root.mainloop()