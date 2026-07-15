"""
screenshot.py
Captures a PNG screenshot of the connected device's current interface
using `adb exec-out screencap`, saved locally with a timestamp.
"""

import os
import subprocess
from datetime import datetime

from adb_utils import ADB_BIN, PLATFORM_TOOLS_DIR, ROOT_DIR, _check_binary

OUTPUT_DIR = os.path.join(ROOT_DIR, "screenshots")


def capture_screenshot():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    binary = _check_binary(ADB_BIN)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(OUTPUT_DIR, f"screenshot_{timestamp}.png")

    with open(out_path, "wb") as f:
        result = subprocess.run(
            [binary, "exec-out", "screencap", "-p"],
            stdout=f,
            stderr=subprocess.PIPE,
        )

    if result.returncode != 0 or os.path.getsize(out_path) == 0:
        if os.path.exists(out_path):
            os.remove(out_path)
        return None, result.stderr.decode(errors="ignore")

    return out_path, None
