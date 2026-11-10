"""Functional checks using synthetic research assets in temporary directories."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / "build-research-knowledge-base"
SCRIPTS = SKILL / "scripts"


def source_record() -> dict:
    return {
        "id": "EXAMPLE-001", "title": "Synthetic test source", "authors": ["Example Author"],
        "year": 2026, "doi": "", "source_type": "peer_reviewed",
        "asset_status": "fulltext_parsed", "evidence_grade": "A",
        "claim_admissibility": "conclusion", "priority": 1, "is_main_method": False,
        "source_url": "", "local_pdf": "raw/papers/example.pdf", "local_text": "",
        "source_card": "kb/sources/example.md", "reader": "", "sha256": "",
        "exclusion_reason": "", "notes": "Synthetic fixture only",
        "venue_quality": {
            "venue_name": "Synthetic venue", "venue_type": "journal", "tier": "unknown",
            "ranking_systems": [], "verified_at": "", "admission_floor_passed": None,
            "assessment_note": "No venue floor in this fixture"
        }
    }


class ScriptChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)

    def run_script(self, name, *arguments, expected=0):
        environment = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / name), *map(str, arguments)],
            capture_output=True, text=True, encoding="utf-8", env=environment
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        return result.stdout

    def write_json(self, name, data):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return target

    def test_all_script_help(self):
        for script in SCRIPTS.glob("*.py"):
            with self.subTest(script=script.name):
                self.run_script(script.name, "--help")

    def test_initialize_standard_tree_and_mainline(self):
        target = self.root / "research-topic"
        self.run_script("init_research_kb.py", target, "--with-mainline")
        for directory in ("raw/papers", "raw/standards", "raw/technical", "raw/text", "kb/readers"):
            self.assertTrue((target / directory).is_dir())
        self.assertTrue((target / "kb/research/research-topicV1.md").exists())
        self.run_script("validate_manifest.py", target / "manifest/sources.json")
        status = json.loads(self.run_script("kb_status.py", target))
        self.assertEqual(status["structural_candidate_state"], "draft")
        self.assertTrue(status["semantic_review_required"])

    def test_reinitialization_preserves_existing_content(self):
        target = self.root / "research-topic"
        self.run_script("init_research_kb.py", target)
        original = target / "AGENTS.md"
        original.write_text("User-maintained instructions\n", encoding="utf-8")
        manifest = target / "manifest/sources.json"
        manifest.write_text('{"sources": [], "custom": true}\n', encoding="utf-8")
        before = {path: path.read_bytes() for path in (original, manifest)}
        self.run_script("init_research_kb.py", target)
        for path, value in before.items():
            self.assertEqual(path.read_bytes(), value)

    def test_project_name_quotes_preserve_valid_json(self):
        target = self.root / "research-topic"
        self.run_script("init_research_kb.py", target, "--project-name", '研究 "A"')
        manifest = json.loads((target / "manifest/sources.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["project"], '研究 "A"')

    def test_project_name_cannot_escape_output_directory(self):
        target = self.root / "research-topic"
        for name in ("../outside", "..\\outside", ".."):
            with self.subTest(name=name):
                self.run_script("init_research_kb.py", target, "--project-name", name,
                                "--with-mainline", expected=2)
        self.assertFalse(target.exists())

    def test_backtick_search_status_is_recognized(self):
        self.write_json("manifest/sources.json", {"sources": [source_record()]})
        research = self.root / "kb/research"
        research.mkdir(parents=True)
        (research / "检索策略与日志.md").write_text(
            "检索状态：`complete`\nCodex 内置搜索\n本地仓库\n合并去重\n", encoding="utf-8")
        (research / "全文证据矩阵.md").write_text("Synthetic matrix", encoding="utf-8")
        report = json.loads(self.run_script("kb_status.py", self.root))
        self.assertEqual(report["structural_candidate_state"], "evidence-complete")

    def test_invalid_manifest_root_is_rejected(self):
        manifest = self.write_json("manifest/sources.json", [])
        self.run_script("validate_manifest.py", manifest, expected=1)
        self.run_script("audit_venue_quality.py", manifest, expected=1)
        self.run_script("kb_status.py", self.root, expected=1)

    def test_malformed_source_fields_are_reported(self):
        record = source_record()
        record["source_type"] = []
        record["venue_quality"]["tier"] = []
        manifest = self.write_json("manifest/sources.json", {"sources": [record]})
        self.run_script("validate_manifest.py", manifest, expected=1)
        self.run_script("audit_venue_quality.py", manifest, expected=1)
        self.write_json("manifest/sources.json", {"sources": [None]})
        self.run_script("kb_status.py", self.root, expected=1)

    def test_duplicate_normalized_doi_is_rejected(self):
        first, second = source_record(), source_record()
        first["doi"] = "https://doi.org/10.0000/EXAMPLE"
        second.update(id="EXAMPLE-002", doi="doi:10.0000/example")
        manifest = self.write_json("sources.json", {"sources": [first, second]})
        self.assertIn("duplicate DOI", self.run_script("validate_manifest.py", manifest, expected=1))

    def test_main_method_requires_fulltext(self):
        record = source_record()
        record.update(is_main_method=True, asset_status="metadata_only", evidence_grade="M")
        manifest = self.write_json("sources.json", {"sources": [record]})
        self.run_script("validate_manifest.py", manifest, expected=1)

    def test_unknown_venue_does_not_automatically_reject_evidence(self):
        record = source_record()
        record["is_main_method"] = True
        manifest = self.write_json("sources.json", {"sources": [record]})
        self.run_script("validate_manifest.py", manifest)
        self.run_script("audit_venue_quality.py", manifest)

    def test_local_links_resolve_encoded_names_and_detect_missing_files(self):
        (self.root / "paper one.pdf").write_bytes(b"%PDF-synthetic")
        page = self.root / "index.md"
        page.write_text("[paper](paper%20one.pdf)\n", encoding="utf-8")
        self.run_script("audit_local_links.py", self.root)
        page.write_text("[paper](missing.pdf)\n", encoding="utf-8")
        self.run_script("audit_local_links.py", self.root, expected=1)

    def test_missing_audit_root_is_an_error(self):
        missing = self.root / "missing"
        self.run_script("audit_local_links.py", missing, expected=1)
        self.run_script("audit_formula_closure.py", missing, expected=1)

    def test_numeric_citations_have_reference_entries(self):
        page = self.root / "citation-fixture.md"
        page.write_text("Synthetic statement [2].\n## References\n[1] Synthetic reference.\n", encoding="utf-8")
        self.run_script("audit_citations.py", page, expected=1)
        page.write_text("Synthetic statement [1].\n## References\n[1] Synthetic reference.\n", encoding="utf-8")
        self.run_script("audit_citations.py", page)

    def test_display_equations_need_symbol_explanation(self):
        page = self.root / "equation-negative-fixture.md"
        page.write_text("$$q = h A$$\n", encoding="utf-8")
        self.run_script("audit_formula_closure.py", page, expected=1)
        page.write_text("$$q = h A$$\n式中，q 为测试输出，h 为测试系数，A 为测试输入；三者均无量纲，= 表示相等，相邻符号表示乘法。\n", encoding="utf-8")
        self.run_script("audit_formula_closure.py", page)

    def test_anysearch_is_optional_unless_required(self):
        page = self.root / "search.md"
        page.write_text(
            "检索状态：`complete`\n## Codex 内置搜索\n日期 2026-11-10 查询 test 新增结果 1\n"
            "## 本地仓库\n日期 2026-11-10 查询 test 结果 1\n## 合并去重\n合并结果 1\n",
            encoding="utf-8")
        self.run_script("audit_search_channels.py", page)
        self.run_script("audit_search_channels.py", page, "--require-anysearch", expected=1)


if __name__ == "__main__":
    unittest.main()
