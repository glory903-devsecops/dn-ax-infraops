# Runbook: [LATENCY_HIGH] Network Performance Degradation (ITIL/SRE Standard)

## 1. Incident Classification
*   **Severity**: Medium (SEV2) - Performance Degradation (Lags/Micro-bursts).
*   **Process Owner**: DN Solutions Global Infrastructure Ops.
*   **KPI Reference**: RTT Threshold > 200ms (Global), > 15ms (Local DC).

## 2. Detection & Validation
- [ ] **Establish Baseline**: Compare current latency with historical average for this segment.
- [ ] **Isolation Test**: Determine if latency is Global (WAN/VPN) or Local (LAN/Switching).
- [ ] **Check Jitter**: Is the latency consistent or varying (jitter)?

## 3. Standard Triage Checklist (Command Line)
*   **Path Tracking**: `traceroute [Target_IP]`, `mtr [Target_IP]` - Identify the specific bottleneck hop.
*   **CPU Utilization**: `show processes cpu history` - Check for L3 switch CPU spikes.
*   **Interface Load**: `show interfaces | include rate` - Review input/output bandwidth utilization.

## 4. Immediate Mitigation (Stop the Bleeding)
### Action 1: Traffic Shaping/QoS
Identify and deprioritize non-critical traffic (e.g., Software Updates, Cloud Sync).
### Action 2: Routing Reroute
If latency is detected in a specific ISP hop, shift traffic to the Secondary ISP path (PBR/BGP prepending).
### Action 3: MTU/MSS Check
Review for fragmentation issues: `ping -s 1472 -f [Target_IP]`.

## 5. Escalation Matrix
- **L1 (NOC)**: Triage and path isolation (0-30 mins).
- **L2 (Net Eng)**: Routing optimization or QoS re-shaping (30-60 mins).
- **L3 (Vendor)**: Capacity expansion or ISP troubleshooting if latency is in the carrier cloud.

## 6. Resolution & Closure
*   Monitor stability for 60 minutes.
*   Log incident in NPM (Network Performance Monitor) for trend analysis.

---
*Global Standard Protocol v2.0 - DN Solutions Operations Excellence*
