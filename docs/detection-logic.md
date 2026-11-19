# Detection logic and interpretation

## ARTEX-associated artifacts

Name/path matches are low-confidence leads because strings can be copied, renamed, or used by legitimate security teams. Confirm package provenance, executable hash/signature, parent process, user, execution time, and surrounding telemetry.

## Network indicators

`vars/iocs.yml` includes historical IP addresses and `xcai.pro` from FBI FLASH-20261113-001. IP addresses can be reassigned or shared. This collection does not query DNS, inspect live sockets for remote IPs, or block indicators. Correlate firewall, proxy, DNS, EDR, and cloud flow logs over the relevant campaign window.

## Behavioral leads

Unexpected LLM API calls are not inherently malicious. Correlate with asset owner/business purpose, identity context, request rate, endpoint path, response volume, and other intrusion evidence. Sequential enumeration, webshells, suspicious identity changes, and unusual outbound transfers should be investigated in context.

## Severity and confidence

Severity describes investigation priority, not proof. Confidence is the strength of the match to the stated rule. A low-confidence ARTEX name match is not a confirmed compromise. A high-confidence IOC match still requires context because infrastructure may be stale or shared.
