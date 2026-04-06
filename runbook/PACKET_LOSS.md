# Runbook: [PACKET_LOSS] Critical Network Packet Integrity (ITIL/SRE Standard)

## 1. Incident Classification
*   **Severity**: High (SEV2) - Data Loss/Application Errors/Jitter.
*   **Process Owner**: DN Solutions Global Infrastructure Ops.
*   **Reference**: Cisco Interface Statistics / Netstat Analysis.

## 2. Detection & Validation
- [ ] **Measure Loss Rate**: Determine if loss is sustained (%) or bursty (spikes).
- [ ] **ICMP Testing**: Run extended ping with large packet sizes (1200+ bytes).
- [ ] **Correlated Apps**: Check if specific apps (e.g., ERP, Video, SIP) are failing.

## 3. Standard Triage Checklist (Command Line)
*   **Interface Stats**: `show interfaces [ID] | include errors|drops|crc|input|output`
*   **Duplex Conflict**: Check for Half-Duplex/Full-Duplex mismatch.
*   **Buffer Tracking**: `show controllers` - Look for internal buffer overflows.
*   **Flow Monitoring**: `show ip cache flow` - Any specific rogue source?

## 4. Immediate Mitigation (Stop the Bleeding)
### Action 1: Component Replacement
If CRC errors are increasing, immediately swap the SFP/Transceiver or cable.
### Action 2: Traffic Reshaping
Apply WRED or Policing for bursty traffic causing buffer tail-drops.
### Action 3: MTU/MSS Alignment
Mismatched MTU in a VPN tunnel is a common cause. Set `ip tcp adjust-mss 1360`.

## 5. Escalation Matrix
- **L1 (NOC)**: Detect and cable check (0-30 mins).
- **L2 (Net Eng)**: Traffic analysis and MTU tuning (30-60 mins).
- **L3 (Vendor)**: Replace core line-cards if internal ASIC errors detected.

## 6. Resolution & Closure
*   Ensure loss < 0.1% over a 15-minute period.
*   Document cable replacement in the hardware inventory log.

---
*Global Standard Protocol v2.0 - DN Solutions Operations Excellence*
