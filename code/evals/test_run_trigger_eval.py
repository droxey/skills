import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("run_trigger_eval.py")


def load_module():
    spec = importlib.util.spec_from_file_location("run_trigger_eval", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RunTriggerEvalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_parse_bool_accepts_json_booleans_zero_one_integers_and_boolean_strings(self):
        self.assertIs(self.module.parse_bool(True, "triggered", "T01"), True)
        self.assertIs(self.module.parse_bool(False, "triggered", "T01"), False)
        self.assertIs(self.module.parse_bool(1, "triggered", "T01"), True)
        self.assertIs(self.module.parse_bool(0, "triggered", "T01"), False)
        self.assertIs(self.module.parse_bool("true", "triggered", "T01"), True)
        self.assertIs(self.module.parse_bool(" false ", "triggered", "T01"), False)

    def test_parse_bool_rejects_other_string_values(self):
        with self.assertRaisesRegex(ValueError, "must be a JSON boolean, true/false string, or 0/1 integer"):
            self.module.parse_bool("yes", "triggered", "T01")

    def test_build_index_rejects_duplicate_ids(self):
        rows = [
            {"id": "T01", "triggered": True},
            {"id": "T01", "triggered": False},
        ]

        with self.assertRaisesRegex(ValueError, "Duplicate id 'T01' found in observed.jsonl"):
            self.module.build_index(rows, "triggered", "observed.jsonl")

    def test_script_accepts_string_boolean_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            expected_path = temp_path / "expected.jsonl"
            observed_path = temp_path / "observed.jsonl"
            out_path = temp_path / "out.md"

            expected_path.write_text(
                '{"id":"T01","should_trigger":true}\n{"id":"F01","should_trigger":false}\n',
                encoding="utf-8",
            )
            observed_path.write_text(
                '{"id":"T01","triggered":"true"}\n{"id":"F01","triggered":"false"}\n',
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--expected",
                    str(expected_path),
                    "--observed",
                    str(observed_path),
                    "--out",
                    str(out_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            report = out_path.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Status: PASS", result.stdout)
        self.assertIn("- FP: 0", report)
        self.assertIn("- FN: 0", report)
        self.assertIn("- Precision: 1.0000", report)
        self.assertIn("- Recall: 1.0000", report)


if __name__ == "__main__":
    unittest.main()
