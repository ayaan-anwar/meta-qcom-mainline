# SPDX-License-Identifier: MIT

import configparser
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "dynamic-layers/networking-layer/recipes-connectivity/networkmanager/networkmanager/nord-lab-mac"


class NordLabMacTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.machine_id = self.root / "machine-id"
        self.slot = self.root / "slot"
        self.output = self.root / "profiles"

    def generate(self, machine_id):
        self.machine_id.write_text(machine_id)
        return subprocess.run(
            ["sh", str(SCRIPT), str(self.machine_id), str(self.slot), str(self.output)],
            text=True, capture_output=True,
        )

    def profiles(self):
        profiles = []
        for port in range(2):
            path = self.output / f"nord-lab-ethernet{port}.nmconnection"
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            config = configparser.ConfigParser()
            config.read(path)
            profiles.append(config)
        return profiles

    def test_all_pairs_match_onboarding_list(self):
        addresses = []
        for slot in range(16):
            with self.subTest(slot=slot):
                result = self.generate("f" * 31 + f"{slot:x}\n")
                self.assertEqual(result.returncode, 0, result.stderr)
                profiles = self.profiles()
                pair = [p["ethernet"]["cloned-mac-address"] for p in profiles]
                self.assertNotEqual(*pair)
                addresses.extend(pair)
                for port, profile in enumerate(profiles):
                    path = ("platform-1a00000.ethernet", "platform-1a80000.ethernet")[port]
                    self.assertEqual(profile["match"]["path"], path)
                    self.assertNotIn("interface-name", profile["connection"])
                    self.assertEqual(profile["ipv4"]["method"], "auto")
                    self.assertEqual(profile["ipv4"]["dhcp-client-id"], "mac")
                    self.assertEqual(profile["connection"]["autoconnect"], "true")
        self.assertEqual(len(set(addresses)), 32)
        self.assertEqual(addresses, (REPO / "docs/nord-lab-macs.txt").read_text().splitlines())

    def test_restarts_and_same_slot_are_stable(self):
        self.assertEqual(self.generate("1" * 31 + "a").returncode, 0)
        original = [dict(p["ethernet"]) for p in self.profiles()]
        self.assertEqual(self.generate("1" * 31 + "a").returncode, 0)
        self.assertEqual(original, [dict(p["ethernet"]) for p in self.profiles()])
        self.assertEqual(self.generate("2" * 31 + "a").returncode, 0)
        self.assertEqual(original, [dict(p["ethernet"]) for p in self.profiles()])

    def test_slot_override(self):
        for slot in range(16):
            with self.subTest(slot=slot):
                self.slot.write_text(f"{slot}\n")
                result = self.generate("1" * 32)
                self.assertEqual(result.returncode, 0, result.stderr)
                pair = [p["ethernet"]["cloned-mac-address"] for p in self.profiles()]
                self.assertEqual(pair, [f"02:11:22:33:44:{0x60 + slot * 2 + port:02x}" for port in range(2)])

    def test_invalid_machine_ids_do_not_create_profiles(self):
        for value in ("", "uninitialized\n", "0" * 32, "1" * 31, "1" * 33,
                      "1" * 31 + "g", "A" * 32, "1" * 31 + " "):
            with self.subTest(value=value):
                self.assertNotEqual(self.generate(value).returncode, 0)
                self.assertFalse(self.output.exists())

    def test_missing_machine_id(self):
        result = subprocess.run(
            ["sh", str(SCRIPT), str(self.machine_id), str(self.slot), str(self.output)],
            text=True, capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_invalid_overrides_do_not_create_profiles(self):
        for value in ("", "-1", "16", "07", "0xf", "1 + 1", "7\n8"):
            with self.subTest(value=value):
                self.slot.write_text(value)
                self.assertNotEqual(self.generate("1" * 32).returncode, 0)
                self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
