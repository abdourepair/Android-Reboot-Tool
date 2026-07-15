
A simple Python CLI to reboot an Android device between modes (system,
recovery, bootloader/fastboot, fastbootd, Samsung download/Odin mode,
Qualcomm EDL) and grab a screenshot of the current device interface —
built on top of the official `adb` and `fastboot` binaries.

<img width="300" height="100" alt="banner" src="https://github.com/user-attachments/assets/93e3fe23-d3a7-449e-91fb-44fae60b67bf" />


No Python knowledge required to run it: just double-click `run.bat`
(Windows) or `run.sh` (macOS/Linux).

## Features

- Reboot **system → recovery**
- Reboot **system → bootloader (fastboot)**
- Reboot **system → fastbootd**
- Reboot **system → download mode** (Samsung/Odin)
- Reboot **system → EDL/9008 mode** (Qualcomm emergency download)
- Reboot **bootloader → system**
- Reboot **fastbootd → system**
- Reboot back to system from any adb-accessible mode
- Capture a **screenshot of the device's current interface** (saved to `screenshots/`)
- One-click launcher for people who don't want to touch the command line

## Requirements

- A Windows, macOS, or Linux PC
- Python 3.8+ ([download here](https://www.python.org/downloads/)) — the
  launcher will tell you if it's missing
- USB debugging enabled on the Android device (Settings → About phone →
  tap "Build number" 7 times → Developer options → USB debugging)
- The official adb/fastboot binaries (see setup below)

## Setup

### 1. Get the code

```bash
git clone https://github.com/YOUR-USERNAME/android-multitool.git
cd android-multitool
```

### 2. Add adb / fastboot binaries

This repo does **not** ship adb/fastboot itself (Google's own binaries,
best to always get the latest official copy). Download the official
Android SDK Platform Tools:

👉 https://developer.android.com/tools/releases/platform-tools

Unzip it, then copy the following files into the `platform-tools/`
folder of this project (same names, same folder):

| File | Where it goes |
|---|---|
| `adb.exe` | `android-multitool/platform-tools/adb.exe` |
| `fastboot.exe` | `android-multitool/platform-tools/fastboot.exe` |
| `AdbWinApi.dll` | `android-multitool/platform-tools/AdbWinApi.dll` |
| `AdbWinUsbApi.dll` | `android-multitool/platform-tools/AdbWinUsbApi.dll` |

(macOS/Linux users only need `adb` and `fastboot`, no `.dll` files.)

Final layout:

```
android-multitool/
├── platform-tools/
│   ├── adb.exe
│   ├── fastboot.exe
│   ├── AdbWinApi.dll
│   └── AdbWinUsbApi.dll
├── src/
├── run.bat
└── run.sh
```

### 3. Run it

- **Windows:** double-click `run.bat`
- **macOS/Linux:** `./run.sh`
- **Or manually:** `python src/main.py`

The launcher checks for Python, installs any dependencies, and starts
the menu automatically.

## Usage

```
==================================================
   Android Multitool - adb / fastboot helper
==================================================
[adb]      connected: [('R58N30ABCDE', 'device')]

Reboot options:
  1. Reboot: system -> recovery
  2. Reboot: system -> bootloader (fastboot)
  3. Reboot: system -> fastbootd
  4. Reboot: system -> download mode (Samsung/Odin)
  5. Reboot: system -> EDL / 9008 mode (Qualcomm)
  6. Reboot: bootloader -> system
  7. Reboot: fastbootd -> system
  8. Reboot: back to system (from adb-accessible mode)
  9. Capture screenshot of device interface
  0. Refresh device status
  q. Quit
```

## Notes & limitations

- Download mode and EDL reboots depend on the device/vendor exposing
  that reboot target to adb; not every phone supports every mode.
- This tool only calls the standard, documented `adb reboot <target>`
  and `fastboot reboot` commands — it does not use exploits or bypass
  any device protections.
- Always be careful with fastboot commands on a real device; wrong
  flashing/erasing commands can brick a phone. This tool intentionally
  only exposes reboot and screenshot actions.

## Contributing

Pull requests are welcome! Ideas for contributions:

- A GUI (Tkinter/PyQt) on top of the same `src/` logic
- `adb backup` / `adb pull` helpers
- Batch operations across multiple connected devices
- Linux `.desktop` launcher / macOS `.command` double-click launcher
- Auto-download of platform-tools on first run

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit your changes
4. Open a pull request

## License

[MIT](LICENSE)
