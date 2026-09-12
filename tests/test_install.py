from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.py"


def load_installer():
    spec = importlib.util.spec_from_file_location("public_skill_installer", INSTALLER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load installer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InstallerTests(unittest.TestCase):
    def test_installs_exactly_one_skill(self) -> None:
        installer = load_installer()
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "skills"
            target = installer.install(destination)

            self.assertEqual(target.name, installer.SKILL_NAME)
            self.assertTrue((target / "SKILL.md").is_file())
            self.assertEqual(
                [path.name for path in destination.iterdir()],
                [installer.SKILL_NAME],
            )

            source_files = {
                path.relative_to(ROOT / "skills" / installer.SKILL_NAME)
                for path in (ROOT / "skills" / installer.SKILL_NAME).rglob("*")
                if path.is_file()
            }
            installed_files = {
                path.relative_to(target) for path in target.rglob("*") if path.is_file()
            }
            self.assertEqual(installed_files, source_files)

    def test_existing_install_requires_explicit_force(self) -> None:
        installer = load_installer()
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "skills"
            target = installer.install(destination)
            marker = target / "local-marker.txt"
            marker.write_text("preserve", encoding="utf-8")
            unrelated = destination / "unrelated-skill" / "SKILL.md"
            unrelated.parent.mkdir()
            unrelated.write_text("unrelated", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                installer.install(destination)
            self.assertTrue(marker.exists())
            self.assertTrue(unrelated.exists())

            installer.install(destination, force=True)
            self.assertFalse(marker.exists())
            self.assertEqual(unrelated.read_text(encoding="utf-8"), "unrelated")

    def test_cli_can_install_to_an_explicit_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "skills"
            result = subprocess.run(
                [sys.executable, "-X", "utf8", str(INSTALLER), "--destination", str(destination)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((destination / "image25-prompt-migrator" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
