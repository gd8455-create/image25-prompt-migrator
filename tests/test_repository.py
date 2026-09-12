from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_repo.py"
SKILL_NAME = "image25-prompt-migrator"
SKILL_ROOT = ROOT / "skills" / SKILL_NAME


def load_validator():
    spec = importlib.util.spec_from_file_location("public_repo_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepositoryTests(unittest.TestCase):
    def test_public_repository_contract(self) -> None:
        validator = load_validator()
        self.assertEqual(validator.validate(ROOT), [])

    def test_only_one_publishable_skill_exists(self) -> None:
        skill_dirs = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
        self.assertEqual(skill_dirs, [SKILL_NAME])

    def test_skill_requires_an_existing_source_prompt(self) -> None:
        validator = load_validator()
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = validator.parse_frontmatter(skill_text)
        self.assertEqual(frontmatter["name"], SKILL_NAME)
        self.assertIn("existing prompt", frontmatter["description"])
        self.assertIn("Requires a source prompt", frontmatter["description"])
        self.assertIn("If it is missing, request it", skill_text)
        self.assertIn("Do not use this skill as a general prompt writer", skill_text)

    def test_agent_metadata_invokes_only_the_migrator(self) -> None:
        metadata = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "GPT Image 2.5 Prompt Migrator"', metadata)
        self.assertIn("$image25-prompt-migrator", metadata)
        self.assertIn("existing source prompt", metadata)

    def test_source_adapter_boundaries_cover_common_prompt_origins(self) -> None:
        guidance = (SKILL_ROOT / "references" / "source-adapters.md").read_text(
            encoding="utf-8"
        )
        for heading in (
            "## 舊 GPT Image 或 DALL·E 系列",
            "## Midjourney",
            "## Stable Diffusion 與 ComfyUI",
            "## FLUX",
            "## Gemini 與 Microsoft Copilot 的自然語言提示詞",
            "## 未知來源",
        ):
            self.assertIn(heading, guidance)
        for boundary in (
            "no_direct_equivalent",
            "unknown_syntax",
            "不自行解碼",
            "不能原樣放入 GPT Image 2.5 提示詞",
        ):
            self.assertIn(boundary, guidance)

    def test_validator_detects_broken_relative_links(self) -> None:
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text("[missing](docs/missing.md)", encoding="utf-8")
            errors = validator.validate_relative_links(root)
        self.assertTrue(any("broken link" in error for error in errors))

    def test_validator_detects_local_paths_and_secret_patterns(self) -> None:
        validator = load_validator()
        samples = {
            "path.md": "C:" + "\\" + "Users" + "\\" + "sample-person" + "\\notes",
            "secret.md": "sk-" + ("x" * 24),
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, content in samples.items():
                (root / name).write_text(content, encoding="utf-8")
            errors = validator.validate_public_content(root)

        labels = "\n".join(errors)
        self.assertIn("user profile path", labels)
        self.assertIn("secret", labels)


if __name__ == "__main__":
    unittest.main()
