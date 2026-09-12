from __future__ import annotations

import hashlib
import re
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
EXAMPLE_FILES = (
    "01-legacy-conversion.md",
    "02-migration-baseline.md",
    "03-cross-ai-conversion.md",
)
REQUIRED_HEADINGS = (
    "原始請求",
    "原始輸入",
    "實際交付輸出",
    "Changes",
    "Request settings",
    "QA／驗收",
    "驗證界線",
)


def heading_sections(markdown: str) -> dict[str, str]:
    matches = list(re.finditer(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", markdown, re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        level = len(match.group(1))
        end = len(markdown)
        for following in matches[index + 1 :]:
            if len(following.group(1)) <= level:
                end = following.start()
                break
        sections[match.group(2).strip()] = markdown[match.end() : end].strip()
    return sections


def first_fenced_block(section: str) -> str:
    match = re.search(r"```[^\n]*\n(.*?)\n```", section, re.DOTALL)
    if not match:
        raise AssertionError("Expected a fenced block")
    return match.group(1)


def markdown_table(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


class SharedMigrationExampleTests(unittest.TestCase):
    def test_three_existing_prompt_examples_have_complete_deliverables(self) -> None:
        available = {path.name for path in EXAMPLES.glob("[0-9][0-9]-*.md")}
        self.assertTrue(set(EXAMPLE_FILES).issubset(available))

        for filename in EXAMPLE_FILES:
            with self.subTest(example=filename):
                markdown = (EXAMPLES / filename).read_text(encoding="utf-8")
                sections = heading_sections(markdown)
                for heading in REQUIRED_HEADINGS:
                    self.assertIn(heading, sections)
                    self.assertTrue(sections[heading].strip())

                source_prompt = first_fenced_block(sections["原始輸入"])
                self.assertTrue(source_prompt.strip())
                self.assertIn("GPT Image 2.5", markdown)
                self.assertRegex(markdown, r"`migration_(?:convert|baseline)`")
                self.assertRegex(sections["QA／驗收"], r"(?m)^- \[ \] ")
                self.assertNotRegex(sections["QA／驗收"], r"(?im)^- \[[x✓]\] ")
                self.assertRegex(
                    sections["驗證界線"],
                    r"尚未|未呼叫|未執行|沒有呼叫|沒有執行",
                )


class LegacyConversionExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        markdown = (EXAMPLES / "01-legacy-conversion.md").read_text(encoding="utf-8")
        cls.sections = heading_sections(markdown)
        cls.source = first_fenced_block(cls.sections["原始輸入"])
        cls.converted = first_fenced_block(cls.sections["Converted prompt"])

    def test_preserves_source_but_produces_a_material_conversion(self) -> None:
        self.assertNotEqual(self.converted, self.source)
        self.assertIn("8K masterpiece", self.source)
        self.assertNotRegex(
            self.converted,
            r"(?i)\b8k\b|\bmasterpiece\b|\bIMAX\b|r/[a-z]+",
        )
        self.assertNotEqual(self.sections["Changes"].strip(), "[]")

    def test_replaces_quality_stacking_with_visible_physics(self) -> None:
        categories = {
            "localized moisture": ("潮濕", "受潮", "積水", "水痕"),
            "material response": ("材質", "石板", "金屬", "磚牆", "布面"),
            "gravity or contact": ("重力", "接觸", "向下", "垂落"),
            "light direction": ("光源", "光照", "環境光", "煤氣燈"),
        }
        for label, terms in categories.items():
            with self.subTest(category=label):
                self.assertTrue(any(term in self.converted for term in terms))

    def test_keeps_target_controls_out_of_the_prompt(self) -> None:
        settings = first_fenced_block(self.sections["Request settings"])
        self.assertIn("model: gpt-image-2.5-flare", settings)
        self.assertIn("size: 1536x1920", settings)
        self.assertNotIn("1536x1920", self.converted)


class MigrationBaselineExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        markdown = (EXAMPLES / "02-migration-baseline.md").read_text(encoding="utf-8")
        cls.sections = heading_sections(markdown)

    def test_source_converted_and_baseline_are_byte_identical(self) -> None:
        original_input = first_fenced_block(self.sections["原始輸入"])
        source = first_fenced_block(self.sections["Source prompt"])
        converted = first_fenced_block(self.sections["Converted prompt"])
        baseline = first_fenced_block(self.sections["Baseline prompt"])
        self.assertEqual(source, original_input)
        self.assertEqual(converted, source)
        self.assertEqual(baseline, source)
        self.assertRegex(self.sections["Changes"], r"^`?\[\]`?(?:\s|$)")
        self.assertRegex(self.sections["Baseline changes"], r"^`?\[\]`?(?:\s|$)")

    def test_model_is_the_only_changed_request_setting(self) -> None:
        rows = markdown_table(self.sections["Request settings"])
        settings = {
            row[0]: (row[1], row[2])
            for row in rows[1:]
            if len(row) >= 3
        }
        self.assertIn("model", settings)
        self.assertNotEqual(*settings["model"])
        for required in (
            "quality",
            "size",
            "background",
            "output_format",
            "重複次數",
        ):
            self.assertIn(required, settings)
            self.assertEqual(
                settings[required][0],
                settings[required][1],
                f"{required} drifted in the migration baseline",
            )


class CrossAiConversionExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        markdown = (EXAMPLES / "03-cross-ai-conversion.md").read_text(encoding="utf-8")
        cls.sections = heading_sections(markdown)
        cls.source = first_fenced_block(cls.sections["原始輸入"])
        cls.converted = first_fenced_block(cls.sections["Converted prompt"])

    def test_source_specific_syntax_is_not_forwarded_as_target_prompt_syntax(self) -> None:
        for token in ("--ar", "--stylize", "--chaos", "--seed", "::1.5"):
            self.assertIn(token, self.source)
            self.assertNotIn(token, self.converted)

    def test_non_equivalent_controls_are_disclosed_without_guessing_source_tool(self) -> None:
        handling = self.sections["Source syntax handling"]
        for control in ("stylize", "chaos", "seed"):
            self.assertRegex(handling, rf"{control}: no_direct_equivalent")
        classification = self.sections["Source classification"]
        self.assertIn("source_origin: other_image_ai", classification)
        self.assertIn("source_tool: unknown", classification)

    def test_required_text_and_target_settings_are_preserved(self) -> None:
        rows = markdown_table(self.sections["Required rendered text"])
        registered = {row[0] for row in rows[1:] if row}
        self.assertIn("AFTER RAIN", registered)
        self.assertIn('"AFTER RAIN"', self.converted)
        settings = first_fenced_block(self.sections["Request settings"])
        self.assertIn("model: gpt-image-2.5-sunburst", settings)
        self.assertIn("size: 1024x1536", settings)


class BuiltInGenerationEvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = (EXAMPLES / "04-built-in-generation-evaluation.md").read_text(
            encoding="utf-8"
        )

    def test_report_preserves_unknown_backend_and_failed_first_qa(self) -> None:
        self.assertIn("execution_backend: unknown", self.report)
        self.assertIn("不能證明輸出確實來自 GPT Image 2.5", self.report)
        self.assertIn("**未通過**", self.report)
        self.assertIn("migration_repair", self.report)

    def test_reported_assets_match_their_sha256_records(self) -> None:
        records = re.findall(
            r"\|\s*`([^`]+\.png)`\s*\|\s*`([0-9a-f]{64})`\s*\|",
            self.report,
        )
        self.assertEqual(len(records), 3)
        for filename, expected_hash in records:
            with self.subTest(asset=filename):
                asset = EXAMPLES / "assets" / filename
                self.assertTrue(asset.is_file())
                self.assertEqual(hashlib.sha256(asset.read_bytes()).hexdigest(), expected_hash)

    def test_png_dimensions_support_the_reported_evaluation(self) -> None:
        claimed_sizes = {
            (int(width), int(height))
            for width, height in re.findall(r"\b(\d{3,5})×(\d{3,5})\b", self.report)
        }
        self.assertEqual(len(claimed_sizes), 1)
        expected_size = claimed_sizes.pop()

        linked_assets = set(re.findall(r"\(assets/([^)]+\.png)\)", self.report))
        self.assertEqual(len(linked_assets), 3)
        for filename in linked_assets:
            with self.subTest(asset=filename):
                data = (EXAMPLES / "assets" / filename).read_bytes()
                self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(data[12:16], b"IHDR")
                width, height, bit_depth, color_type = struct.unpack(">IIBB", data[16:26])
                self.assertEqual((width, height), expected_size)
                self.assertEqual(bit_depth, 8)
                self.assertEqual(color_type, 2)


if __name__ == "__main__":
    unittest.main()
