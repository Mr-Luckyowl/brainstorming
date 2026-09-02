## REM All new TOPICs will assign above and not the End of this file.



## PCB Layout for a new TPM 2.0 Modul for a ASUS Z-97A.
KiCAD and Netlist.


# Fedora 44 RAM Hardening & Browser Containment (Brainstorming)

This repository serves as an open brainstorming space for securing Fedora 44 against extreme memory allocations (e.g., 32 GB RAM leaks caused by Chromium/Electron processes) without compromising system stability or proprietary graphics drivers (Nvidia).

## 🧠 Problem Statement
- **Root Cause:** Microsoft Edge and VS Code (Chromium/Electron architecture) can trigger massive memory leaks due to rogue tabs or faulty extensions.
- **Symptom:** Rogue processes attempt to reserve up to 32 GB of RAM, causing a complete system freeze.
- **Constraint:** Legacy tools like `ulimit` are ineffective against modern memory allocation methods (like `mmap`).

## 🛠️ Verified Solutions & Facts

### 1. Capping the User Space (systemd & cgroups v2)
Enforcing strict memory limits on user processes to safeguard the core operating system.
- **Command:** `sudo systemctl set-property user.slice MemoryHigh=7168M MemoryMax=8192M`
- **Effect:** Upon reaching the 8 GB hard limit, the cgroup-native OOM killer terminates the culprit. The desktop and OS remain stable and responsive.

### 2. System-Wide Early Warning System (PSI-Notify)
Since systemd-oomd kills rogue processes silently, `psi-notify` provides native desktop alerts before a crash happens.
- **Package:** `psi-notify.x86_64` (available in official Fedora repositories)
- **Activation (without sudo):** `systemctl --user enable --now psi-notify`

### 3. Internal Browser Regulation
- **Parameter:** `--max-old-space-size=3072`
- **Concept:** Passing this flag directly to the Chromium/Node.js engine via `.desktop` launchers forces individual tabs or extensions to catch themselves at 3 GB before system limits are triggered.

## ⚠️ Key Insights (IT Security & Stability)
- **No Third-Party Tools:** System hardening must rely strictly on core Linux utilities and official repository packages to prevent supply-chain attacks (e.g., trojans or credential stealers).
- **No Journal Access for Standard Users:** For security compliance, standard users must never be added to the global `systemd-journal` group, preventing accidental leaks of sensitive system data.
- **Nvidia Driver Protection:** Global kernel parameters (like `mem=8G`) break proprietary GPU memory layouts. Resource constraints must safely reside at the user-slice level (`user.slice`).

