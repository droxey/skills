from pathlib import Path
import subprocess


def test_installer_copies_runtime_skill_files(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    target = tmp_path / "skills"

    completed = subprocess.run(
        ["bash", str(root / "scripts" / "install.sh"), str(target)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    installed = target / "reasoning-router"
    assert (installed / "SKILL.md").read_bytes() == (root / "SKILL.md").read_bytes()
    assert (installed / "README.md").read_bytes() == (root / "README.md").read_bytes()
    assert (installed / "scripts" / "select_reasoning.py").read_bytes() == (
        root / "scripts" / "select_reasoning.py"
    ).read_bytes()
    assert "Installed reasoning-router" in completed.stdout
