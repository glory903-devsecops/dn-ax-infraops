# Runbook: [DNS_ISSUE] Domain Service Accessibility (ITIL/SRE Standard)

## 1. Incident Classification
*   **Severity**: High (SEV2) - Global Application Access Failure.
*   **Process Owner**: DN Solutions Global Infrastructure Ops.
*   **KPI Reference**: Recursive Query Timeout < 2.0s.

## 2. Detection & Validation
- [ ] **Check Scope**: Is it a local resolution issue (single client) or global (all clients)?
- [ ] **Internal vs. External**: Determine if Internal AD DNS or External Public DNS (ISP/Cloudflare/Google) is at fault.
- [ ] **Health Probe**: Check if DNS Server IP (UDP 53) is pingable.

## 3. Standard Triage Checklist (Command Line)
*   **Trace Queries**: `dig +trace [Domain_Name]` - Identify failure in Root, TLD, or Authoritative zone.
*   **Local Lookup**: `nslookup [Domain_Name] [Internal_DNS_IP]` - Test specific server.
*   **Cache Review**: `rndc dumpdb -all` (Linux/BIND) or `Get-DnsServerCache` (Windows).
*   **Reverse Lookups**: `dig -x [IP_Address]` - Check for Pointer (PTR) record health.

## 4. Immediate Mitigation (Stop the Bleeding)
### Action 1: Cache Flush
Clear client and server Resolver caches: `dnscmd /clearcache` or `systemd-resolve --flush-caches`.
### Action 2: Failover (Secondary DNS)
Temporarily point client DHCP to a secondary/public DNS (8.8.8.4 / 1.1.1.1) to restore business continuity.
### Action 3: Rollback
If a recent zone change occurred, revert the serial number and reload the configuration.

## 5. Escalation Matrix
- **L1 (NOC)**: Initial trace and cache flush (0-15 mins).
- **L2 (Net Eng)**: Zone file correction and replication check (15-30 mins).
- **L3 (Domain Registrar/ISP)**: If TLD/Glue record issue detected at Registrar level.

## 6. Resolution & Closure
*   Ensure resolution works across all global branch points.
*   Update any stale records in the DC/AD environment.

---
*Global Standard Protocol v2.0 - DN Solutions Operations Excellence*
