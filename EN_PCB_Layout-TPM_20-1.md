J1 (Mainboard-Header): 
Connector_Generic:Conn_02x10_Odd_Even (Rastermaß: Standard 2,54 mm).
⚠️ Crucial Correction:
In the footprint editor, mark Pin 4 on the female header as "Not Connected" (NC) 
and delete its corresponding copper pad.
Place a small cross at that location on the silkscreen layer (F.SilkS).
This represents the physically blocked hole (KEY), ensuring the module is keyed and protected against reverse polarity.

U1 (TPM-Chip):
Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm (Passend für den Infineon SLB9665TT20 oder SLB9670 LPC).
C1, C2, C3, C4 :
Capacitor_SMD:C_0603_1608Metric ( 0603 it is still easy-to solid ).
                ++ Wert: 100nF.
(Pull-Up-Ressistor):
        R1, R2 : Resistor_SMD:R_0603_1608Metric. 
                ++ Wert: 10kΩ.

Das korrigierte Routing-Diagramm (Netlist).
Man muß die Pins, im KiCad-Schaltplan-Editor (eeschema) genau nach diesem Layout-Plan, verbinden:

Netz-Name    | Von Pfostenleiste (J1)  | Zu Infineon-Chip (U1) | Zusatz-Verbindung / Hinweis
-------------+-------------------------+-----------------------+----------------------------------
+3V3         | Pin 1                   | Pin 28 & Pin 18       | C1-C4 an diese Leitung hängen
GND          | Pin 2, Pin 12, Pin 17   | Pin 14 & Pin 24       | Gegenpol von C1-C4 hier anbinden
LAD0         | Pin 3                   | Pin 4                 | LPC Data 0
[KEY]        | Pin 4                   | [GEBLOCKT]            | Kein Pin, kein Loch, kein Kupfer!
LAD1         | Pin 5                   | Pin 5                 | LPC Data 1
LAD2         | Pin 7                   | Pin 7                 | LPC Data 2
LAD3         | Pin 8                   | Pin 8                 | LPC Data 3
LFRAME#      | Pin 9                   | Pin 2                 | LPC Frame-Signal
LCLK         | Pin 10                  | Pin 1                 | 33 MHz Systemtakt (KRITISCH!)
LRESET#      | Pin 11                  | Pin 3                 | Bus-Reset
SERIRQ       | Pin 16                  | Pin 10                | Serieller Interrupt
CLKRUN#      | Pin 18                  | Pin 11                | Über R1 (10k) an +3V3 hängen
LPCPD#       | Pin 19                  | Pin 12                | Über R2 (10k) an +3V3 hängen



### PCB Layout Guidelines for Traces (Design Rules).

## 1. Clock Line (LCLK):
## The connection from J1-Pin 10 to U1-Pin 1 transmits a continuous 33 MHz signal.
## Route this trace as short as possible, keeping it flat and direct to the chip without major detours or excessive vias (layer changes).

## 2. Capacitor Placement:
## Place C1 and C2 directly adjacent to Pin 28 of the IC, and capacitors C3 and C4 directly adjacent to Pin 18. If the capacitors are placed too far away on the board, their decoupling effect against voltage ## spikes is lost, causing the system to fail during BIOS POST.
## 3. Trace Width: Use a width of 0.25 mm for all signal lines. For the power supply lines (+3V3 and GND), use 0.50 mm to keep resistance as low as possible.
