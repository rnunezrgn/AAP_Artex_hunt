# IOC Data Validation – test_ioc_data.py

## 1. Purpose

`test_ioc_data.py` is a Python unit-test module used to validate the quality and consistency of the Indicator of Compromise (IOC) database.

It does not execute Ansible playbooks, scan endpoints, or determine whether a system has been compromised.

Its responsibility is to catch malformed or incomplete threat-intelligence data before that data is used by the detection roles.

## 2. What is an IOC?

An Indicator of Compromise is an artifact that may be associated with malicious activity.

Examples include:

| IOC type | Example |
|---|---|
| IPv4 address | 192.0.2.10 |
| Domain | example.invalid |
| SHA-256 hash | 64 hexadecimal characters |
| Filename | suspicious-example.exe |
| Process name | suspicious-process |

These examples are illustrative and are not confirmed ARTEX indicators.

## 3. What does the test validate?

### YAML parsing

Checks that the IOC file is valid YAML.

### Required fields

Checks that each indicator contains the expected information, such as:

- Type
- Value
- Source
- Confidence
- Description

### IP address validation

Uses Python's standard `ipaddress` module to check IPv4 and IPv6 syntax.

### Domain validation

Checks basic domain syntax and rejects malformed values.

### Hash validation

Checks SHA-256 and other supported hash lengths and hexadecimal characters.

### Duplicate detection

Identifies repeated indicators so that redundant data does not unnecessarily complicate investigations.

### Source attribution

Checks that each indicator identifies its source.

A syntactically valid IOC is not automatically trustworthy. Source quality and ARTEX attribution must be independently reviewed.

## 4. Running the tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

Example output:

```text
test_ioc_file_exists ... ok
test_ioc_yaml_is_valid ... ok
test_required_fields ... ok
test_ip_address_format ... ok
test_hash_format ... ok
test_duplicate_indicators ... ok
```

The actual output depends on the tests and IOC data included in the repository.

## 5. What passing tests means

Passing tests means that the IOC data meets the structural and syntax requirements implemented by the test module.

It does NOT mean:

- The indicators are malicious.
- The indicators are associated with ARTEX.
- A host is compromised.
- The detection roles successfully detect every attack.
- The IOC database is current.

## 6. Recommended development workflow

1. Obtain indicators from an approved threat-intelligence source.
2. Review source credibility and attribution.
3. Add indicators to the IOC YAML file.
4. Run `test_ioc_data.py`.
5. Review failures and correct the data.
6. Run Ansible lint and syntax checks.
7. Test detection against controlled test artifacts.
8. Review and approve changes before deployment.

## 7. Security recommendation

Never automatically add unverified indicators to production detection rules.

Every IOC should have documented provenance, confidence, and review information. Indicators should also have an expiration or review date where appropriate.
