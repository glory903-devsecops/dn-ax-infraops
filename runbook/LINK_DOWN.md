# Runbook: [LINK_DOWN] Global Link Connectivity Outage (ITIL/SRE Standard)

## 1. Incident Classification
*   **Severity**: Critical (SEV1) - Potential Business Continuity Disruption.
*   **Process Owner**: DN Solutions Global Infrastructure Ops.
*   **Standard Reference**: ITIL Incident Management / Cisco L1-L3 Troubleshooting Guide.

## 2. Detection & Validation
- [ ] **Verify Alert Accuracy**: Cross-check with NMS (Network Management System) and external probes.
- [ ] **Scope Assessment**: Is this an isolated node (Factory-Line) or a site-wide outage (GE Site 13 experience)?
- [ ] **Correlated Events**: Check for concurrent power or environmental alerts.

## 3. Standard Triage Checklist (Command Line)
*   **Physical Layer**: `show interfaces status`, `show ip interface brief`
*   **Link Layer**: `show logging system` (Check for 'UP/DOWN' flapping)
*   **Connectivity**: `traceroute [Gateway_IP]`, `mtr [Destination]`

## 4. Immediate Mitigation (Stop the Bleeding)
### Action 1: Fault Isolation
Determine if the fault is Internal (Local Switch/Cable) or External (ISP/Carrier). 
### Action 2: Rollback (If applicable)
Check for recent configuration changes (`show archive config differences`) and rollback if necessary.
### Action 3: Layer 1 Recovery
Reset SFP modules or cycle the interface: `shutdown` -> `no shutdown`.

## 5. Escalation Matrix
- **L1 (NOC)**: Initial detection and triage (0-15 mins).
- **L2 (Net Eng)**: Deep dive and reconfiguration (15-30 mins).
- **L3 (Vendor/ISP)**: Call Carrier (e.g., KT/SKB Global) if external fiber cut suspected.

## 6. Resolution & Closure
*   Verify stability for at least 30 minutes post-recovery.
*   Update Root Cause Analysis (RCA) in the Incident Portal.

---
*Global Standard Protocol v2.0 - DN Solutions Operations Excellence*
