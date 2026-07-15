"""
adb_utils.py
Locates and wraps the adb / fastboot executables that ship inside the
platform-tools/ folder next to this project.

Nothing here talks to the network. It only shells out to the local
adb.exe / fastboot.exe binaries the user has placed in platform-tools/.
"""

import os
import subprocess
import sys

# Root of the repo -> android-multitool/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATFORM_TOOLS_DIR = os.path.join(ROOT_DIR, "platform-tools")

IS_WINDOWS = os.name == "nt"

ADB_BIN = os.path.join(PLATFORM_TOOLS_DIR, "adb.exe" if IS_WINDOWS else "adb")
FASTBOOT_BIN = os.path.join(PLATFORM_TOOLS_DIR, "fastboot.exe" if IS_WINDOWS else "fastboot")


class ToolNotFoundError(Exception):
    pass


def _check_binary(path):
    if not os.path.isfile(path):
        raise ToolNotFoundError(
            f"'{os.path.basename(path)}' not found in {PLATFORM_TOOLS_DIR}\n"
            "Download the Android SDK Platform Tools from Google and copy "
            "adb.exe, fastboot.exe, AdbWinApi.dll and AdbWinUsbApi.dll "
            "into the platform-tools/ folder. See README.md."
        )
    return path


def run(cmd, tool="adb", timeout=30):
    """
    Run a command against adb or fastboot.
    cmd: list of args, e.g. ["reboot", "recovery"]
    tool: "adb" or "fastboot"
    """
    binary = _check_binary(ADB_BIN if tool == "adb" else FASTBOOT_BIN)
    full_cmd = [binary] + cmd
    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except FileNotFoundError:
        raise ToolNotFoundError(f"Could not execute {binary}")


def list_adb_devices():
    code, out, err = run(["devices"], tool="adb")
    devices = []
    for line in out.splitlines()[1:]:
        line = line.strip()
        if line and "\t" in line:
            serial, state = line.split("\t")
            devices.append((serial, state))
    return devices


def list_fastboot_devices():
    code, out, err = run(["devices"], tool="fastboot")
    devices = []
    for line in out.splitlines():
        line = line.strip()
        if line:
            parts = line.split()
            if len(parts) >= 2:
                devices.append((parts[0], parts[1]))
    return devices


def ensure_platform_tools_present():
    """Quick sanity check used at startup, does not raise, just reports."""
    missing = []
    for name in ["adb.exe", "fastboot.exe", "AdbWinApi.dll", "AdbWinUsbApi.dll"] if IS_WINDOWS else ["adb", "fastboot"]:
        if not os.path.isfile(os.path.join(PLATFORM_TOOLS_DIR, name)):
            missing.append(name)
    return missing
