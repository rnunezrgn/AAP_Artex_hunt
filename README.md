# ARTEX Detection Collection

**Version:** 1.1.0  
**Platform:** Red Hat Ansible Automation Platform 2.6  
**Automation:** Ansible Core and Event-Driven Ansible

## Overview

ARTEX Detection Collection is a defensive automation project designed to support security investigations across:

- Red Hat Enterprise Linux and Fedora
- Windows Server
- Kubernetes and OpenShift
- Microsoft Azure

The project provides a read-only framework for identifying configured indicators, suspicious artifacts, and potential security events.

It also includes an Event-Driven Ansible integration example for initiating investigations from incoming security alerts.

**Important:** Detection results are investigative leads, not proof of compromise or ARTEX attribution.

## Capabilities

### Ansible detection

The collection provides platform-specific investigation roles and playbooks.

### Event-Driven Ansible

The EDA rulebook can receive webhook events and launch an AAP investigation job template.

### IOC validation

The Python test module validates IOC data structure and syntax before the data is used by detection roles.

### Read-only operation

The project is intended for investigation and reporting. It does not automatically remediate systems.

## Repository structure

```text
artex_detection_collection/
├── rulebooks/
│   └── artex_detection.yml
├── playbooks/
│   ├── artex_hunt.yml
│   └── test_local.yml
├── roles/
│   ├── linux/
│   ├── windows/
│   ├── kubernetes/
│   └── azure/
├── vars/
│   └── iocs.yml
├── tests/
│   └── test_ioc_data.py
├── docs/
│   ├── aap-integration.md
│   ├── eda-rulebook.md
│   └── ioc-testing.md
├── CONTRIBUTING.md
├── LICENSE
├── requirements.yml
└── galaxy.yml
```

## Installation

Install the required Ansible collections:

```bash
ansible-galaxy collection install -r requirements.yml
```

Run the investigation playbook:

```bash
ansible-playbook -i inventory playbooks/artex_hunt.yml
```

## EDA integration

The example rulebook is located at:

`rulebooks/artex_detection.yml`

It receives webhook events, evaluates security-alert conditions, and launches an AAP job template.

See `docs/eda-rulebook.md` for configuration and testing instructions.

## IOC data validation

The IOC test file is:

`tests/test_ioc_data.py`

Run:

```bash
python -m pip install PyYAML
python -m unittest discover -s tests -v
```

See `docs/ioc-testing.md` for the validation methodology and limitations.

## AAP 2.6 integration

The recommended workflow is:

1. Import the repository into an AAP project.
2. Create an investigation job template.
3. Configure the EDA credential.
4. Create a Rulebook Activation.
5. Select `rulebooks/artex_detection.yml`.
6. Configure the webhook source.
7. Test the event-to-job workflow.

## Security considerations

- Use least-privilege credentials.
- Restrict webhook access.
- Protect event payloads.
- Validate event-supplied host information.
- Use trusted threat-intelligence sources.
- Review false positives.
- Keep investigation tasks read-only.

## Limitations

This project is a defensive detection framework, not a certified ARTEX detection product.

Actual detection coverage depends on verified threat intelligence, platform support, available telemetry, and testing.

The included EDA rulebook is a webhook integration example and requires validation in the target AAP environment.

## License

Apache License 2.0.
