"""
reboot_modes.py
Handles switching an Android device between its different boot modes:

  system (normal)  <--adb-->  recovery
  system (normal)  <--adb-->  bootloader / fastboot
  bootloader       <--fastboot-->  system
  system (normal)  <--adb-->  download mode (Samsung Odin)
  system (normal)  <--adb-->  EDL / 9008 mode (Qualcomm emergency download)
  fastbootd        <--fastboot-->  system

All of this is just adb/fastboot's own documented reboot subcommands,
nothing vendor-locked or exploit based.
"""

from adb_utils import run


def reboot_system_to_recovery():
    return run(["reboot", "recovery"], tool="adb")


def reboot_system_to_bootloader():
    return run(["reboot", "bootloader"], tool="adb")


def reboot_system_to_fastbootd():
    return run(["reboot", "fastboot"], tool="adb")


def reboot_system_to_download_mode():
    """
    Samsung 'Download mode' (Odin mode). Works on most Samsung devices
    with a rooted or unrooted shell that allows this reboot target.
    """
    return run(["reboot", "download"], tool="adb")


def reboot_system_to_edl():
    """
    Qualcomm Emergency Download mode (9008). Requires the device/kernel
    to expose the edl reboot target; not all devices support this from adb.
    """
    return run(["reboot", "edl"], tool="adb")


def reboot_bootloader_to_system():
    return run(["reboot"], tool="fastboot")


def reboot_fastbootd_to_system():
    return run(["reboot"], tool="fastboot")


def reboot_to_system_from_adb():
    """Normal reboot back to system, used from adb when already in a
    special adb-accessible mode (e.g. sideload)."""
    return run(["reboot"], tool="adb")


MENU_ACTIONS = {
    "1": ("Reboot: system -> recovery", reboot_system_to_recovery),
    "2": ("Reboot: system -> bootloader (fastboot)", reboot_system_to_bootloader),
    "3": ("Reboot: system -> fastbootd", reboot_system_to_fastbootd),
    "4": ("Reboot: system -> download mode (Samsung/Odin)", reboot_system_to_download_mode),
    "5": ("Reboot: system -> EDL / 9008 mode (Qualcomm)", reboot_system_to_edl),
    "6": ("Reboot: bootloader -> system", reboot_bootloader_to_system),
    "7": ("Reboot: fastbootd -> system", reboot_fastbootd_to_system),
    "8": ("Reboot: back to system (from adb-accessible mode)", reboot_to_system_from_adb),
}
