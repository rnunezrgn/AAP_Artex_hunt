# ARTEX Detection – Event-Driven Ansible Integration

## 1. Overview

This document explains how to integrate the ARTEX Detection Collection with Event-Driven Ansible (EDA) and Ansible Automation Platform (AAP) 2.6.

The integration allows security monitoring systems to initiate an ARTEX investigation automatically when a qualifying security event is received.

The architecture separates event processing from investigation:

- EDA receives and evaluates incoming security events.
- AAP launches the investigation job template.
- Ansible executes the read-only detection roles.
- The resulting findings are made available for security investigation.

## 2. Architecture

```text
SIEM / Security Monitoring
          |
          | Webhook event
          v
EDA Rulebook Activation
          |
          | Evaluate event conditions
          v
AAP 2.6 Job Template
          |
          | Execute Ansible playbook
          v
ARTEX Detection Collection
          |
          v
Investigation Results
```

## 3. Event format

The example rulebook expects a JSON event similar to:

```json
{
  "event_type": "security_alert",
  "hostname": "server01.example.com",
  "source_ip": "192.0.2.10",
  "event_id": "SOC-2026-001"
}
```

This is an illustrative event. The IP address is reserved for documentation and is not an ARTEX indicator.

The event fields are:

| Field | Description |
|---|---|
| event_type | Event category used by the rulebook |
| hostname | Target system |
| source_ip | Source IP associated with the alert |
| event_id | SIEM or security-platform event identifier |

Your SIEM integration may require a transformation layer to produce this structure.

## 4. Configure the AAP job template

Create an AAP job template named:

`ARTEX Detection - Investigation`

Suggested configuration:

- Inventory: approved investigation inventory
- Project: ARTEX detection repository
- Playbook: `playbooks/artex_hunt.yml`
- Credentials: minimum required read-only credentials
- Execution Environment: one containing the required Ansible collections
- Privilege escalation: only where required by the detection tasks

The playbook must accept the extra variables passed by EDA.

For example:

```yaml
target_host: server01.example.com
source_ip: 192.0.2.10
event_id: SOC-2026-001
```

The playbook and roles must validate target selection and must not trust arbitrary event-supplied inventory names.

## 5. Configure the Rulebook Activation

1. Import the repository into an AAP project.
2. Ensure the rulebook is available in the project.
3. Create an EDA credential with the appropriate AAP connection.
4. Create a Rulebook Activation.
5. Select `rulebooks/artex_detection.yml`.
6. Select an execution environment containing `ansible.eda`.
7. Configure the webhook source and activation settings.
8. Start the activation.
9. Verify that the activation reports a running state.

Exact interface labels can vary by AAP release.

## 6. Test the webhook

Send a test event to the configured webhook endpoint:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "security_alert",
    "hostname": "server01.example.com",
    "source_ip": "192.0.2.10",
    "event_id": "TEST-001"
  }' \
  http://EDA_HOST:5000/
```

Replace `EDA_HOST` with your actual EDA endpoint.

Use only an authorized test environment.

Verify:

- The webhook receives the event.
- The rulebook condition matches.
- The AAP job template launches.
- The expected extra variables are passed.
- The investigation completes.
- Results are available for review.

## 7. Security considerations

- Authenticate and restrict webhook access.
- Use TLS through an approved ingress or reverse proxy.
- Do not expose the webhook directly to untrusted networks.
- Use least-privilege AAP credentials.
- Validate hostnames and event fields before launching investigations.
- Do not allow arbitrary inventory selection from untrusted event payloads.
- Protect event payloads from containing passwords, tokens, or sensitive data.
- Apply rate limiting and event deduplication.
- Keep the detection workflow read-only.

## 8. Operational limitations

The initial rulebook is a webhook demonstration. It does not provide a complete SIEM connector, event correlation engine, or ARTEX attribution mechanism.

An incoming security alert is not proof of ARTEX compromise. The investigation results must be assessed alongside trusted threat intelligence and other forensic evidence.

## 9. Future enhancements

- Integration with Microsoft Sentinel.
- Integration with Splunk.
- Integration with QRadar.
- Event deduplication.
- Severity-based investigation.
- Separate workflows for Linux, Windows, Kubernetes, and Azure.
- Centralized investigation reporting.
