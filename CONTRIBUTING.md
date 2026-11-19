# Contributing

Thank you for contributing to ARTEX Detection Collection.

## Security requirements

- Keep detection tasks read-only.
- Do not add automatic remediation without a separate approved design.
- Do not commit credentials, tokens, or customer data.
- Use trusted sources for threat-intelligence indicators.
- Document indicator provenance, confidence, and review dates.
- Document false-positive considerations.

## Development requirements

- Use fully qualified Ansible collection names.
- Keep platform-specific tasks in their respective roles.
- Add tests for new detection logic.
- Update documentation for behavior changes.
- Validate YAML and Ansible syntax.

## Testing

```bash
python -m pip install PyYAML ansible-core ansible-lint yamllint

python -m unittest discover -s tests -v

yamllint .

ansible-lint

ansible-playbook -i tests/inventory \
  playbooks/artex_hunt.yml --syntax-check
```

## Pull request checklist

- [ ] Detection remains read-only.
- [ ] IOC sources are documented.
- [ ] Tests have been added or updated.
- [ ] Documentation has been updated.
- [ ] No credentials or sensitive information are included.
- [ ] Validation checks pass.
