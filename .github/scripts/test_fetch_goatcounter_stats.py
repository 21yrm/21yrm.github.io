#!/usr/bin/env python3
"""Tests for the GoatCounter stats publisher."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("fetch_goatcounter_stats.py")


def load_module():
    spec = importlib.util.spec_from_file_location("fetch_goatcounter_stats", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GoatCounterStatsTest(unittest.TestCase):
    def test_default_code_matches_goatcounter_site(self):
        module = load_module()

        self.assertEqual(module.DEFAULT_CODE, "yaorunmao")

    def test_default_start_matches_goatcounter_launch_window(self):
        module = load_module()

        self.assertEqual(module.DEFAULT_START, "2026-06-01T00:00:00Z")

    def test_extract_total_views_reads_goatcounter_total_field(self):
        module = load_module()

        self.assertEqual(module.extract_total_views({"total": 1234, "total_events": 12}), 1234)

    def test_merge_legacy_offset_adds_previous_views(self):
        module = load_module()

        self.assertEqual(module.merge_legacy_offset(12), 2220)

    def test_read_existing_total_recovers_goatcounter_views_from_final_total(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "goatcounter.json"
            output.write_text(json.dumps({"total_views": 2220}), encoding="utf-8")

            self.assertEqual(module.read_existing_total(output), 12)

    def test_extract_total_views_rejects_missing_total_field(self):
        module = load_module()

        self.assertIsNone(module.extract_total_views({"stats": []}))


if __name__ == "__main__":
    unittest.main()
