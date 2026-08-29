# Linux Commands

# Check if resource limits are enabled?
cat /etc/systemd/system.control/user.slice.d/50-MemoryMax.conf

# Enable user.slice memory restriction:
sudo systemctl set-property user.slice MemoryHigh=7168M MemoryMax=8192M

# Or restrict a specific program/application:
systemd-run --user --scope -p MemoryMax=4G -p MemoryHigh=3.5G code

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