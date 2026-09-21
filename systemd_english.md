# Fedora 44 Process Containment: 
Hardening Microsoft Edge via systemd-run
Modern web browsers utilizing the Chromium architecture can trigger unpredictable memory loops or massive leaks via faulty scripts and extensions.
On systems running Fedora 44, a rogue browser process can # attempt to reserve up to 32 GB of RAM, exhausting available resources and leading to a complete operating system freeze. 
Legacy #resource-limiting tools such as ulimit are largely ineffective against modern # memory allocation methods like mmap.
To maintain system responsiveness and ensure that the core desktop environment remains uncompromised,
workloads can be isolated using cgroups v2 directly through the # # native systemd-run command interface.

# Sandboxing command; like:
systemd-run --user --scope -p MemoryMax=8G -p MemoryHigh=7.5G -p AllowedCPUs=2-3 /usr/bin/microsoft-edge-stable >/dev/null 2>&1
# Watching with HTOP in realtime:
htop -F /usr/bin/microsoft-edge-stable


# Linux Commands

# Check if resource limits are enabled?
cat /etc/systemd/system.control/user.slice.d/50-MemoryMax.conf

# Enable user.slice memory restriction:
sudo systemctl set-property user.slice MemoryHigh=7168M MemoryMax=8192M

# Or restrict a specific program/application:
systemd-run --user --scope -p MemoryMax=4G -p MemoryHigh=3.5G code

# Watching with HTOP in realtime:
htop -F /usr/bin/microsoft-edge-stable


# e.g., Fedora-44
# /etc/systemd/system.control/user.slice.d/50-MemoryHigh.conf

#
# Does not work in WSL2!
#
# Because psi-notify requires the PSI interfaces (/proc/pressure/memory) to be active in the Linux kernel.
# Search for documentation under Fedora-44:
# Note: It is important to include the quotation marks " " !!!
dnf5 search "*-doc"
#
# For Fedora-44 and any other Linux distribution, you should install 'links' or 'lynx' to read all man pages and docs directly in the TERMINAL!!
#
# Like this: links /usr/share/doc/python-systemd/html/index.html
# Simple and efficient. Press (F10) for the menu within the terminal.

Docs:
man systemctl
man systemd-system.conf
man systemd-oomd.service

man systemd.slice
man systemd.resource.control
man cgroups

man cgroup_namespaces
man proc
man bootparam


journal-user_slice.py::python3
#!/usr/bin/env python3
from systemd import journal

# Creates the reader for the system journal
j = journal.Reader()

# Correct filtering: Filter by the _SYSTEMD_SLICE field
j.add_match(_SYSTEMD_SLICE="user.slice")

# Displays the last 5 log entries
print("Latest log messages from your user.slice:")

# Fetch the entries (list(j) converts the matches)
entries = list(j)

if not entries:
    print("No log entries found for user.slice.")
else:
    for entry in entries[-5:]:
        # Retrieves the timestamp and the actual message string
        zeit = entry.get('__REALTIME_TIMESTAMP', 'Unknown time')
        nachricht = entry.get('MESSAGE', '')
        print(f"[{zeit}] {nachricht}")

python3 journal-user_slice.py