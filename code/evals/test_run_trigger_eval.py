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

    def test_parse_bool_accepts_json_booleans_and_zero_one_integers(self):
        self.assertIs(self.module.parse_bool(True, "triggered", "T01"), True)
        self.assertIs(self.module.parse_bool(False, "triggered", "T01"), False)
        self.assertIs(self.module.parse_bool(1, "triggered", "T01"), True)
        self.assertIs(self.module.parse_bool(0, "triggered", "T01"), False)

    def test_build_index_rejects_duplicate_ids(self):
        rows = [
            {"id": "T01", "triggered": True},
            {"id": "T01", "triggered": False},
        ]

        with self.assertRaisesRegex(ValueError, "Duplicate id 'T01' found in observed.jsonl"):
            self.module.build_index(rows, "triggered", "observed.jsonl")

    def test_script_rejects_string_boolean_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            expected_path = temp_path / "expected.jsonl"
            observed_path = temp_path / "observed.jsonl"
            out_path = temp_path / "out.md"

            expected_path.write_text('{"id":"T01","should_trigger":true}\n', encoding="utf-8")
            observed_path.write_text('{"id":"T01","triggered":"false"}\n', encoding="utf-8")

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

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be a JSON boolean or 0/1 integer", result.stderr)


if __name__ == "__main__":
    unittest.main()
