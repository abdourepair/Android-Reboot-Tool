"""
main.py
Android Multitool - simple CLI to reboot a device between modes and
grab a screenshot of the current interface, using the local adb/fastboot
binaries in platform-tools/.
"""

import sys

from adb_utils import (
    ensure_platform_tools_present,
    list_adb_devices,
    list_fastboot_devices,
    ToolNotFoundError,
)
from reboot_modes import MENU_ACTIONS
from screenshot import capture_screenshot


def print_header():
    print("=" * 50)
    print("   Android Multitool - adb / fastboot helper")
    print("=" * 50)


def print_status():
    missing = ensure_platform_tools_present()
    if missing:
        print("[!] Missing files in platform-tools/:", ", ".join(missing))
        print("    See README.md for download instructions.\n")
        return False

    adb_devices = list_adb_devices()
    fastboot_devices = list_fastboot_devices()
    if adb_devices:
        print(f"[adb]      connected: {adb_devices}")
    if fastboot_devices:
        print(f"[fastboot] connected: {fastboot_devices}")
    if not adb_devices and not fastboot_devices:
        print("[!] No device detected in adb or fastboot mode.")
        print("    Plug in your device, enable USB debugging, and try again.")
    print()
    return True


def print_menu():
    print("Reboot options:")
    for key, (label, _) in MENU_ACTIONS.items():
        print(f"  {key}. {label}")
    print("  9. Capture screenshot of device interface")
    print("  0. Refresh device status")
    print("  q. Quit")


def main():
    print_header()
    ok = print_status()

    while True:
        print_menu()
        choice = input("\nSelect an option: ").strip().lower()

        if choice == "q":
            print("Bye.")
            sys.exit(0)

        if choice == "0":
            print()
            print_status()
            continue

        if choice == "9":
            print("Capturing screenshot...")
            try:
                path, error = capture_screenshot()
            except ToolNotFoundError as e:
                print(f"[!] {e}")
                continue
            if path:
                print(f"[+] Saved to {path}")
            else:
                print(f"[!] Failed to capture screenshot: {error}")
            continue

        if choice in MENU_ACTIONS:
            label, action = MENU_ACTIONS[choice]
            print(f"Running: {label}")
            try:
                code, out, err = action()
            except ToolNotFoundError as e:
                print(f"[!] {e}")
                continue
            if code == 0:
                print("[+] Command sent successfully.")
            else:
                print(f"[!] Command failed: {err or out}")
            continue

        print("Invalid option, try again.\n")


if __name__ == "__main__":
    main()
