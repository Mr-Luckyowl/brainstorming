# OpenSource Projects & Hardware Labs
> 🚀 **Support My Work:** If these fixes and hardware layouts saved your system or time, consider supporting my work, starring the repo, or following me directly on my GitHub profile: **[github.com/Mr-Luckyowl](https://github.com/Mr-Luckyowl)**!

For more see this link **(https://github.com/Mr-Luckyowl?tab=repositories )**

---

## 🛠️ REM ---> All new TOPICs will assign above and not the End of this file.

---

## 📐 PCB Layout for a new TPM 2.0 Module for an ASUS Z-97A
- **Tools:** KiCAD 8.x / 9.x
- **Deliverables:** Schematic, PCB Layout, and Netlist compatibility files.
- **Description:** A custom hardware security module breakout board tailored specifically to fit the legacy ASUS Z-97A motherboard TPM header footprint, enabling modern cryptographic standard verification on legacy Intel Haswell setups.

---

# 🧠 Fedora 44 RAM Hardening & Browser Containment

Modern web browsers utilizing the Chromium architecture can trigger unpredictable memory loops or massive leaks via faulty scripts and extensions. On systems running Fedora 44, a rogue browser process can attempt to reserve up to 32 GB of RAM, exhausting available resources and leading to a complete operating system freeze. Legacy resource-limiting tools such as `ulimit` are largely ineffective against modern memory allocation methods like `mmap`. 

To maintain system responsiveness and ensure that the core desktop environment remains uncompromised, workloads are isolated using **cgroups v2** directly through the native `systemd-run` command interface.

## 🛠️ Eradicated Mistakes & Corrected Implementations

Legacy guides contain crucial mistakes that break GUI applications or crash the desktop environment. Here is the corrected engineering approach for Fedora 44:

### 1. Fixed the `--scope` vs. Service Isolation Flaw
- **The Mistake:** Using `systemd-run --scope` executes the browser inside the exact same session hierarchy as your Xfce desktop environment shell. If the browser hits an unmanageable memory loop, it can drag the entire Xfce graphical session down with it.
- **The Correction:** Dropping `--scope` forces systemd to spin up a fully isolated, transient **Service Unit** (`--unit=msedge-sandbox`). If it hits the hard limit, only the service container crashes. Your desktop remains 100% stable and responsive.

### 2. Fixed the `sudo` / Root Elevation Security Anti-Pattern
- **The Mistake:** Running `sudo systemd-run` runs the browser under the root context. This immediately shatters X11/Wayland display authority permissions (causing the GUI application to refuse to open) and opens up severe security vulnerabilities.
- **The Correction:** Explicitly utilizing the `--user` flag. The sandbox container runs strictly within the unprivileged user space context, maintaining flawless access to the Xfce display server while possessing zero root capabilities.

### 3. Precision Memory Bounds (cgroups v2)
- **The Correction:** Instead of ambiguous global restrictions, we feed precise cgroups v2 attributes directly via `--property`:
  - `MemoryHigh`: The soft throttle line. Systemd aggressively reclaims page cache and slows down memory allocations for the processes inside once hit.
  - `MemoryMax`: The absolute ceiling. If a rogue tab pushes past this number, the kernel's native cgroup OOM-killer instantly terminates the offender.

### The Corrected Production Command:
```bash
systemd-run --user --slice=browser-containment.slice --unit=msedge-sandbox --property=MemoryHigh=6G --property=MemoryMax=8G msedge
```

---

## 🛠️ System-Wide Protection Configurations

### 1. User Slice-Level Hardening
As a general fallback to protect the OS from any rogue user processes:
```bash
sudo systemctl set-property user.slice MemoryHigh=7168M MemoryMax=8192M
```

### 2. Desktop Early Warning Alerts (`psi-notify`)
Since systemd's OOM-killer terminates rogue processes silently in the background, you can use the Pressure Stall Information tracker to receive desktop notifications before an OOM occurs.
```bash
# Install from official Fedora repositories
sudo dnf install psi-notify

# Activate as a standard user (No root/sudo required)
systemctl --user enable --now psi-notify
```

### 3. Internal Engine Control
Force individual tabs and Electron nodes to trigger internal V8 garbage collection routines at 3 GB before system limits intervene:
```bash
msedge --max-old-space-size=3072
```

⚠️ **Security Compliance Note:** Standard non-privileged users must never be added to the global `systemd-journal` group to prevent potential privilege escalations and sensitive kernel log exposures. Furthermore, global kernel limitations like `mem=8G` must be avoided as they break proprietary Nvidia GPU memory mapping layouts.

---

## 🖥️ Hardware Fix: Intel Haswell & Nvidia DisplayPort Freeze

### The Problem
On hybrid GPU systems featuring an Intel Haswell CPU (Integrated HD Graphics) alongside a proprietary Nvidia graphics card, connection over a **DisplayPort (DP)** cable frequently triggers an immediate kernel/X-server freeze during transitions into low-power states. Because modern browsers like Edge leverage heavy hardware acceleration, they instantly trigger this driver hang when the hardware tries to drop into Display C-States (specifically DC6).

### The Solution
Forcing the Intel `i915` graphics driver to completely disable these unstable display power states (`i915.enable_dc=0`). This prevents the DisplayPort connection link training from breaking during idle cycles.

### Implementation on Fedora (BLS Compliant)
Since Fedora utilizes the modern Boot Loader Specification (BLS), modifying `/etc/default/grub` alone does not automatically push parameters to active kernels. The native `grubby` tool must be used:

```bash
# 1. Apply the parameter to all installed kernel entries
sudo grubby --update-kernel=ALL --args="i915.enable_dc=0"

# 2. Verify that the parameter is properly staged for the next boot
sudo grubby --info=DEFAULT
```
*Look for `i915.enable_dc=0` inside the `args=` output string.*

---

## 📊 Diagnostics & Real-Time Monitoring Scripts

Keep these commands active in your terminal to monitor hardware behaviors and memory performance:

### Real-Time Kernel Graphics Diagnostics
Track driver training, failures, or handshakes on the fly:
```bash
sudo dmesg -w | grep -E "i915|drm|nvidia"
```

### zRAM Pool Compression Performance
Track how efficiently your compressed RAM space handles swapping allocations:
```bash
watch -n 1 zramctl
```

### Process-Specific Swap Allocation Aggregator
Calculate exactly how many megabytes of uncompressed memory Microsoft Edge has pushed out to your zRAM backing store:
```bash
grep -i swap /proc/\$(pgrep -d ',' msedge)/smaps 2>/dev/null | awk '{sum+=\$2} END {print sum/1024 " MB"}'
```

---

## 📄 License
This documentation and accompanying script concepts are shared as Open Source under the terms of the **Apache License 2.0**. Feel free to fork, modify, and distribute!