
import tempfile
import unittest
from pathlib import Path

from infra_mind.analyzer import analyze_log


class TestInfraMind(unittest.TestCase):

    def test_detects_out_of_memory(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "test.log"
            log.write_text("ERROR: Out of memory: Killed process")

            report = analyze_log(log)

            self.assertEqual(report["total_findings"], 1)
            self.assertEqual(
                report["findings"][0]["issue"],
                "OUT_OF_MEMORY"
            )

    def test_empty_log(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "empty.log"
            log.write_text("Application started successfully")

            report = analyze_log(log)

            self.assertEqual(report["total_findings"], 0)


if __name__ == "__main__":
    unittest.main()
