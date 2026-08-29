# Linux Befehle
# abfragen, ob aktiviert? 
cat /etc/systemd/system.control/user.slice.d/50-MemoryMax.conf

# user.slice aktivieren:
sudo systemctl set-property user.slice MemoryHigh=7168M MemoryMax=8192M

# oder bestimmtes Programm restriktieren:
systemd-run --user --scope -p MemoryMax=4G -p MemoryHigh=3.5G code

# e.g. Fedora-44
# /etc/systemd/system.control/user.slice.d/50-MemoryHigh.conf

#
# WSL2 funktioniert es nicht! 
#
# weil es psi-notify setzt voraus, dass die PSI-Schnittstellen (/proc/pressure/memory) im Linux-Kernel aktiv sind.
# Nach docs suchen unter Fedora-44:
# wichtig die " " mit eintippen!!!
dnf5 search "*-doc"
#
# Für Fedora-44 und jedes andere Linux solltet Ihr Euch links oder Lynx installieren, um alle mans und docs zu lesen im TERMINAL!!
#
# und zwar so: links /usr/share/doc/python-systemd/html/index.html
# einfach und effizient. ( F10) Menu im Terminal.

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

# Erstellt den Reader für das System-Tagebuch
j = journal.Reader()

# Hier ist die korrekte Filterung: Wir filtern nach dem Feld _SYSTEMD_SLICE
j.add_match(_SYSTEMD_SLICE="user.slice")

# Zeigt die letzten 5 Einträge an
print("Die letzten Meldungen aus Ihrer user.slice:")

# Wir holen die Einträge ab (list(j) konvertiert die Treffer)
entries = list(j)

if not entries:
    print("Keine Einträge in der user.slice gefunden.")
else:
    for entry in entries[-5:]:
        # Holt den Zeitstempel und die eigentliche Nachricht
        zeit = entry.get('__REALTIME_TIMESTAMP', 'Unbekannte Zeit')
        nachricht = entry.get('MESSAGE', '')
        print(f"[{zeit}] {nachricht}")

python3 journal-user_slice.py
