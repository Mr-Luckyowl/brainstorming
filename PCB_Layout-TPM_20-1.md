## PCB Layout for a new TPM 2.0 Modul for a ASUS Z-97A.
KiCAD and Netlist.

### 📐 KiCAD Netlist (20-1 Pin Header)
```lisp
(export (version D)
  (design
...
```


<FollowUp>
### 🔀 Corrected Hardware Routing Matrix (Netlist Schematic)

When connecting nets inside the KiCAD Schematic Editor (`eeschema`), follow this exact layout plan to link the Motherboard Header (`J1`) directly to the Infineon Security Chip (`U1`):

| Net Name | From Header (J1) | To Infineon IC (U1) | Additional Connections / Engineering Notes |
| :--- | :--- | :--- | :--- |
| **+3V3** | Pin 1 | Pin 28 & Pin 18 | Connect the positive side of decoupling capacitors `C1-C4` to this line. |
| **GND** | Pin 2, Pin 12, Pin 17 | Pin 14 & Pin 24 | Connect the negative side of decoupling capacitors `C1-C4` to this ground plane. |
| **LAD0** | Pin 3 | Pin 4 | LPC Data Line 0. |
| **[KEY]** | Pin 4 | **[BLOCKED]** | **No Pin, no hole, no copper!** Physical polarization safety key. |
| **LAD1** | Pin 5 | Pin 5 | LPC Data Line 1. |
| **LAD2** | Pin 7 | Pin 7 | LPC Data Line 2. |
| **LAD3** | Pin 8 | Pin 8 | LPC Data Line 3. |
| **LFRAME#**| Pin 9 | Pin 2 | LPC Frame Signal (Active Low). |
| **LCLK** | Pin 10 | Pin 1 | **CRITICAL:** 33 MHz PCI/LPC system clock line. |
| **LRESET#**| Pin 11 | Pin 3 | Bus Hardware Reset (Active Low). |
| **SERIRQ** | Pin 16 | Pin 10 | Serialized Interrupt Request line. |
| **CLKRUN#**| Pin 18 | Pin 11 | Must be pulled up to **+3V3** via resistor **R1 (10 kΩ)**. |
| **LPCPD#** | Pin 19 | Pin 12 | Must be pulled up to **+3V3** via resistor **R2 (10 kΩ)**. |

---


</FollowUp>

# Source: 
### 📐 KiCAD Netlist (20-1 Pin Header Source)

```lisp
(export (version D)
  (design
    (source "ASUS_Z97A_TPM20.kicad_sch")
    (date "2026-10-29")
    (tool "Eeschema 9.0.0"))
  (components
    (component (ref "J1")
      (value "ASUS_TPM_Header_20-1")
      (footprint "Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical")
      (sheetpath (names "/") (tstamps "/"))
      (tstamps "00000000-0000-0000-0000-00005fcd1a02"))
    (component (ref "U1")
      (value "SLB9665_LPC")
      (footprint "Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm")
      (sheetpath (names "/") (tstamps "/"))
      (tstamps "00000000-0000-0000-0000-00005fcd2f10"))
    (component (ref "C1")
      (value "100nF")
      (footprint "Resistor_SMD:R_0805_2012Metric")
      (sheetpath (names "/") (tstamps "/"))
      (tstamps "00000000-0000-0000-0000-00005fcd3a44")))
  (nets
    (net (code "1") (name "GND")
      (node (ref "J1") (pin "2"))
      (node (ref "J1") (pin "12"))
      (node (ref "J1") (pin "17"))
      (node (ref "U1") (pin "14"))
      (node (ref "U1") (pin "24"))
      (node (ref "C1") (pin "2")))
    (net (code "2") (name "+3.3V")
      (node (ref "J1") (pin "1"))
      (node (ref "U1") (pin "28"))
      (node (ref "U1") (pin "18"))
      (node (ref "C1") (pin "1")))
    (net (code "3") (name "LPC_LAD0")
      (node (ref "J1") (pin "3"))
      (node (ref "U1") (pin "4")))
    (net (code "4") (name "LPC_LAD1")
      (node (ref "J1") (pin "5"))
      (node (ref "U1") (pin "5")))
    (net (code "5") (name "LPC_LAD2")
      (node (ref "J1") (pin "7"))
      (node (ref "U1") (pin "7")))
    (net (code "6") (name "LPC_LAD3")
      (node (ref "J1") (pin "8"))
      (node (ref "U1") (pin "8")))
    (net (code "7") (name "LPC_LFRAME")
      (node (ref "J1") (pin "9"))
      (node (ref "U1") (pin "2")))
    (net (code "8") (name "LPC_LCLK")
      (node (ref "J1") (pin "10"))
      (node (ref "U1") (pin "1")))
    (net (code "9") (name "LPC_LRESET")
      (node (ref "J1") (pin "11"))
      (node (ref "U1") (pin "3")))
    (net (code "10") (name "LPC_SERIRQ")
      (node (ref "J1") (pin "16"))
      (node (ref "U1") (pin "10")))
    (net (code "11") (name "CLKRUN")
      (node (ref "J1") (pin "18"))
      (node (ref "U1") (pin "11")))
    (net (code "12") (name "LPCPD")
      (node (ref "J1") (pin "19"))
      (node (ref "U1") (pin "12")))
  )
)
```

---


# Control: ## 📐 PCB Layout & Netlist Specification for ASUS Z-97A TPM 2.0 Module (LPC Bus)

This document contains the exact hardware routing matrix, bill of materials (BOM) footprint assignments, and critical high-frequency PCB design rules for building a custom TPM 2.0 security module tailored for the legacy 20-1 pin ASUS motherboard header.

### 📦 Component & Footprint Architecture

*   **J1 (Mainboard Header):** 
    *   **Footprint:** `Connector_Generic:Conn_02x10_Odd_Even` (Standard 2.54 mm pitch pin header).
    *   **⚠️ CRITICAL HARDWARE MODIFICATION:** Open this footprint inside the KiCAD Footprint Editor. Mark **Pin 4** as *Not Connected (NC)*, completely **delete its copper pad**, and place a small cross/X on the silk screen layer (`F.SilkS`). This acts as the physical polarization key (blocked hole) to prevent incorrect or reversed orientation on the motherboard.
*   **U1 (TPM IC):** 
    *   **Footprint:** `Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm`. Fully compatible with hardware chips like **Infineon SLB9665TT20** or **SLB9670 (LPC interface variant)**.
*   **C1, C2, C3, C4 (Decoupling Capacitors):** 
    *   **Footprint:** `Capacitor_SMD:C_0603_1608Metric`. The 0603 package size balances compact design with manageable hand-soldering.
    *   **Value:** `100nF`.
*   **R1, R2 (Bus Pull-Up Resistors):** 
    *   **Footprint:** `Resistor_SMD:R_0603_1608Metric`.
    *   **Value:** `10 kΩ`.

---

### 🔀 Corrected Hardware Routing Matrix (Netlist Schematic)

When connecting nets inside the KiCAD Schematic Editor (`eeschema`), follow this exact layout plan to link the Motherboard Header (`J1`) directly to the Infineon Security Chip (`U1`):

| Net Name | From Header (J1) | To Infineon IC (U1) | Additional Connections / Engineering Notes |
| :--- | :--- | :--- | :--- |
| **+3V3** | Pin 1 | Pin 28 & Pin 18 | Connect the positive side of decoupling capacitors `C1-C4` to this line. |
| **GND** | Pin 2, Pin 12, Pin 17 | Pin 14 & Pin 24 | Connect the negative side of decoupling capacitors `C1-C4` to this ground plane. |
| **LAD0** | Pin 3 | Pin 4 | LPC Data Line 0. |
| **[KEY]** | Pin 4 | **[BLOCKED]** | **No Pin, no hole, no copper!** Physical polarization safety key. |
| **LAD1** | Pin 5 | Pin 5 | LPC Data Line 1. |
| **LAD2** | Pin 7 | Pin 7 | LPC Data Line 2. |
| **LAD3** | Pin 8 | Pin 8 | LPC Data Line 3. |
| **LFRAME#**| Pin 9 | Pin 2 | LPC Frame Signal (Active Low). |
| **LCLK** | Pin 10 | Pin 1 | **CRITICAL:** 33 MHz PCI/LPC system clock line. |
| **LRESET#**| Pin 11 | Pin 3 | Bus Hardware Reset (Active Low). |
| **SERIRQ** | Pin 16 | Pin 10 | Serialized Interrupt Request line. |
| **CLKRUN#**| Pin 18 | Pin 11 | Must be pulled up to **+3V3** via resistor **R1 (10 kΩ)**. |
| **LPCPD#** | Pin 19 | Pin 12 | Must be pulled up to **+3V3** via resistor **R2 (10 kΩ)**. |

---

### 📐 PCB Tracing & Design Rules (High-Frequency Guidelines)

To prevent data corruption, signal reflections, or transmission dropouts on the 33 MHz LPC bus, adhere to these three manufacturing rules inside the KiCAD PCB Layout Editor (`pcbnew`):

1. **The Clock Line (LCLK) Routing:** The link between `J1 (Pin 10)` and `U1 (Pin 1)` carries a continuous high-frequency 33 MHz square wave. Route this trace using the shortest possible path. Keep it flat, avoid large routing loops, and minimize layer changes (**Vias**) to reduce parasitic inductance.
2. **Decoupling Capacitor Placement:** 
    * Place capacitors `C1` and `C2` **immediately adjacent** to power `Pin 28` of the IC.
    * Place capacitors `C3` and `C4` **immediately adjacent** to power `Pin 18` of the IC.
    * *Why?* If these capacitors are placed too far away on the board, their ability to filter out high-frequency voltage spikes drops significantly, causing the module to fail during the motherboard's BIOS POST sequence.
3. **Trace Width Configurations:** 
    * Use a standard width of **0.25 mm** for all high-speed digital signallines (`LAD0-3`, `LCLK`, `LFRAME#`, etc.).
    * Use a reinforced width of **0.50 mm** for the power distribution tracks (**+3V3** and **GND**) to minimize trace resistance and voltage drops across the module.


# deleted #