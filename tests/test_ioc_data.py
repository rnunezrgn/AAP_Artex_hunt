
import hashlib
import ipaddress
import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
IOC_FILE = ROOT / "vars" / "iocs.yml"

REQUIRED_FIELDS = {"type", "value", "source"}

SHA256_PATTERN = re.compile(r"^[a-fA-F0-9]{64}$")
SHA1_PATTERN = re.compile(r"^[a-fA-F0-9]{40}$")
MD5_PATTERN = re.compile(r"^[a-fA-F0-9]{32}$")


def load_iocs():
    with IOC_FILE.open(encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError("IOC YAML must contain a dictionary")

    indicators = data.get("indicators")

    if not isinstance(indicators, list):
        raise ValueError("'indicators' must be a YAML list")

    return indicators


def valid_domain(value):
    if not isinstance(value, str) or len(value) > 253:
        return False

    value = value.rstrip(".")

    if not value or "." not in value:
        return False

    labels = value.split(".")

    return all(
        label
        and len(label) <= 63
        and re.fullmatch(
            r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?",
            label,
        )
        for label in labels
    )


class TestIOCData(unittest.TestCase):

    def test_ioc_file_exists(self):
        self.assertTrue(
            IOC_FILE.is_file(),
            f"IOC file not found: {IOC_FILE}",
        )

    def test_ioc_yaml_is_valid(self):
        indicators = load_iocs()
        self.assertIsInstance(indicators, list)

    def test_required_fields(self):
        for index, indicator in enumerate(load_iocs()):
            with self.subTest(indicator=index):
                self.assertIsInstance(indicator, dict)
                self.assertTrue(
                    REQUIRED_FIELDS.issubset(indicator.keys()),
                    f"Indicator {index} is missing required fields",
                )

    def test_indicator_values_are_nonempty(self):
        for index, indicator in enumerate(load_iocs()):
            with self.subTest(indicator=index):
                self.assertIsInstance(indicator["value"], str)
                self.assertTrue(indicator["value"].strip())

    def test_ip_addresses(self):
        for indicator in load_iocs():
            if indicator["type"].lower() in ("ipv4", "ipv6", "ip"):
                with self.subTest(value=indicator["value"]):
                    ipaddress.ip_address(indicator["value"])

    def test_domain_format(self):
        for indicator in load_iocs():
            if indicator["type"].lower() == "domain":
                with self.subTest(value=indicator["value"]):
                    self.assertTrue(
                        valid_domain(indicator["value"]),
                        "Invalid domain syntax",
                    )

    def test_hash_format(self):
        patterns = {
            "md5": MD5_PATTERN,
            "sha1": SHA1_PATTERN,
            "sha256": SHA256_PATTERN,
        }

        for indicator in load_iocs():
            indicator_type = indicator["type"].lower()

            if indicator_type in patterns:
                with self.subTest(value=indicator["value"]):
                    self.assertRegex(
                        indicator["value"],
                        patterns[indicator_type],
                    )

    def test_no_duplicate_type_value_pairs(self):
        seen = set()

        for indicator in load_iocs():
            key = (
                indicator["type"].lower(),
                indicator["value"].strip().lower(),
            )

            with self.subTest(indicator=key):
                self.assertNotIn(
                    key,
                    seen,
                    f"Duplicate IOC: {key}",
                )

            seen.add(key)

    def test_source_is_nonempty(self):
        for index, indicator in enumerate(load_iocs()):
            with self.subTest(indicator=index):
                self.assertIsInstance(indicator["source"], str)
                self.assertTrue(indicator["source"].strip())


if __name__ == "__main__":
    unittest.main()
