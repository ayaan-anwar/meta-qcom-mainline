# SPDX-License-Identifier: MIT

from pathlib import Path
import shlex

from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import runCmd


class QcomNordLabMacTests(OESelftestTestCase):
    def test_mac_assignment(self):
        repo = Path(__file__).resolve().parents[4]
        runCmd("python3 " + shlex.quote(str(repo / "tests/test_nord_lab_mac.py")))
