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