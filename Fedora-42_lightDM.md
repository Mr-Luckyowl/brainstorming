# Reset failed state (kein Paketwechsel)
sudo systemctl reset-failed lightdm.service

# Versuch, den DM einmal zu starten und live Logs beobachten
sudo systemctl start lightdm.service
sudo journalctl -f -u lightdm.service


# Suche nach xrandr-Aufrufen mit && in typischen LightDM- und X-Konfigpfaden
sudo grep -R --line-number -E "xrandr.*&&" /etc/lightdm /etc/X11 /usr/share/lightdm /usr/share/X11 /usr/local 2>/dev/null || true

# Suche allgemein im System (kann länger dauern)
sudo grep -R --line-number -E "xrandr.*&&" /etc /usr/share /usr/local /home 2>/dev/null || true

# Prüfe lightdm-Konfigs
sudo grep -R --line-number -E "display-setup-script|greeter-setup-script|session-setup-script" /etc/lightdm /usr/share/lightdm 2>/dev/null || true

sudo tee /usr/local/bin/lightdm-display-setup.sh > /dev/null <<'EOF'
#!/bin/sh
# LightDM display setup wrapper
# Beispiel: zwei xrandr-Befehle nacheinander
/usr/bin/xrandr --output HDMI-1 --auto
/usr/bin/xrandr --output eDP-1 --off
EOF

sudo chmod +x /usr/local/bin/lightdm-display-setup.sh


sudo mkdir -p /etc/lightdm/lightdm.conf.d
sudo tee /etc/lightdm/lightdm.conf.d/50-display-setup.conf > /dev/null <<'EOF'
[Seat:*]
display-setup-script=/usr/local/bin/lightdm-display-setup.sh
EOF

sudo systemctl reset-failed lightdm.service
sudo systemctl start lightdm.service
sudo journalctl -u lightdm.service -n 200 --no-pager

# Liste der xgreeters (Greeter-Desktopdateien)
ls -l /usr/share/xgreeters

# Falls nichts da ist, suche nach greeter-desktopdateien
sudo find /usr/share -maxdepth 3 -type f -iname '*greeter*.desktop' -print

# Paket, das die installierte Datei liefert (falls vorhanden)
rpm -qf /usr/share/xgreeters/* 2>/dev/null || true




# Zeige alle Greeter-Dateien mit vollständigem Pfad
printf '%s\n' /usr/share/xgreeters/*

# Welches RPM liefert die Datei (falls vorhanden)
for f in /usr/share/xgreeters/*; do
  echo "=== $f ==="
  rpm -qf "$f" 2>/dev/null || echo "Kein Paket gefunden"
  sed -n '1,200p' "$f"
done



ODER als absoluter Hack:

[Seat:*]
display-setup-script=/bin/sh -c '/usr/bin/xrandr --setprovideroutputsource modesetting NVIDIA-0 && /usr/bin/xrandr --auto'


