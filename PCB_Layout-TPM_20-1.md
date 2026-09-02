## J1 (Mainboard-Header): 
## Connector_Generic:Conn_02x10_Odd_Even (Rastermaß: Standard 2,54 mm).
## ⚠️ Wichtigste Korrektur:
## Im Footprint-Editor markieren an der Buchsenleiste Pin 4 als "Nicht belegt" und lösche das dazugehörige Kupfer-Pad.
## Setze auf dem Bestückungsdruck (F.SilkS) ein kleines Kreuz dorthin.
## Das ist das physisch geschlossene Loch (KEY), damit das Modul verpolungssicher ist.

## U1 (TPM-Chip):
## Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm (Passend für den Infineon SLB9665TT20 oder SLB9670 LPC).
## C1, C2, C3, C4 :
## Capacitor_SMD:C_0603_1608Metric (Größe 0603 lässt sich noch gut von Hand löten).
##                 ++ Wert: 100nF.
## (Pull-Up-Widerstände):
##         R1, R2 : Resistor_SMD:R_0603_1608Metric. 
##                 ++ Wert: 10kΩ.

## Das korrigierte Routing-Diagramm (Netlist).
## Man muß die Pins, im KiCad-Schaltplan-Editor (eeschema) genau nach diesem Layout-Plan, verbinden:
##
## Netz-Name    | Von Pfostenleiste (J1)  | Zu Infineon-Chip (U1) | Zusatz-Verbindung / Hinweis
## -------------+-------------------------+-----------------------+----------------------------------
## +3V3         | Pin 1                   | Pin 28 & Pin 18       | C1-C4 an diese Leitung hängen
## GND          | Pin 2, Pin 12, Pin 17   | Pin 14 & Pin 24       | Gegenpol von C1-C4 hier anbinden
## LAD0         | Pin 3                   | Pin 4                 | LPC Data 0
## [KEY]        | Pin 4                   | [GEBLOCKT]            | Kein Pin, kein Loch, kein Kupfer!
## LAD1         | Pin 5                   | Pin 5                 | LPC Data 1
## LAD2         | Pin 7                   | Pin 7                 | LPC Data 2
## LAD3         | Pin 8                   | Pin 8                 | LPC Data 3
## LFRAME#      | Pin 9                   | Pin 2                 | LPC Frame-Signal
## LCLK         | Pin 10                  | Pin 1                 | 33 MHz Systemtakt (KRITISCH!)
## LRESET#      | Pin 11                  | Pin 3                 | Bus-Reset
## SERIRQ       | Pin 16                  | Pin 10                | Serieller Interrupt
## CLKRUN#      | Pin 18                  | Pin 11                | Über R1 (10k) an +3V3 hängen
## LPCPD#       | Pin 19                  | Pin 12                | Über R2 (10k) an +3V3 hängen
##
##
## 
## Layout-Leitlinien für die Leiterbahnen (Design Rules).
## Wenn man im Layout-Editor die Leiterbahnen (Traces) verbindet - graphisch sieht es aus als zieht man es, halte man sich an diese drei Regeln; damit der LPC-Bus bei der Übertragung nicht aussteigt:
## 1. Die Taktleitung (LCLK): Die Verbindung von J1-Pin 10 zu U1-Pin 1 überträgt ein permanentes 33-MHz-Signal.
## Man muß diese Leitung so kurz wie möglich verlegen und ziehe sie flach und ohne große Umwege oder unzählige Vias (Lagenwechsel) direkt zum Chip.
## 2. Platzierung der Kondensatoren:
## Man platziere C1 und C2 unmittelbar neben den Pin 28 des ICs und den Kondensatoren C3 und C4 unmittelbar neben den Pin 18.
## Wenn die Kondensatoren zu weit entfernt auf der Platine sitzen, verpufft ihre Schutzwirkung gegen Spannungsspitzen, und das System schlägt beim BIOS-POST fehl.
## 3. Leiterbahndicke: Man verwende für alle Signalleitungen eine Dicke von 0,25 mm.
## Für die Stromversorgungslinien (+3V3 und GND) nehme man 0,50 mm, um den Widerstand so gering wie möglich zu halten.