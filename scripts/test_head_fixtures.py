"""Exercise scratch fixture generation, not an imaginary orchestration engine."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("make_head_fixtures.py")


class FixtureTests(unittest.TestCase):
    def run_generator(self, root, scenario, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(root), scenario, *args],
                              capture_output=True, text=True)

    def test_refuses_to_overwrite_existing_content(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            p = root / "series/SERIES.md"
            p.parent.mkdir()
            p.write_text("Creator's existing work\n")
            result = self.run_generator(root, "success")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(p.read_text(), "Creator's existing work\n")
            self.assertIn("empty", result.stderr)

    def test_success_writes_test_evidence_and_four_content_files(self):
        with tempfile.TemporaryDirectory() as temp:
            result = self.run_generator(Path(temp), "success")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((Path(temp) / "test-data/scenario.json").is_file())
            evidence = json.loads((Path(temp) / "test-data/scenario.json").read_text())
            self.assertTrue(evidence["test_data_only"])
            self.assertEqual(len(evidence["issues"]), 4)
            self.assertEqual([i["stage"] for i in evidence["issues"]], [1, 2, 3, 4])
            self.assertEqual(len(list((Path(temp) / "series/episodes/s01e04-why-scripts-fail").glob("0*.md"))), 4)

    def test_unknown_scenario_leaves_destination_untouched(self):
        with tempfile.TemporaryDirectory() as temp:
            result = self.run_generator(Path(temp), "not-a-scenario")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_legacy_marker_variants_keep_same_external_evidence(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            for dest, marker in ((a, "checked"), (b, "unchecked")):
                result = self.run_generator(Path(dest), "legacy-marker", "--legacy-marker", marker)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((Path(dest) / "test-data/scenario.json").is_file())
            self.assertEqual((Path(a) / "test-data/scenario.json").read_bytes(),
                             (Path(b) / "test-data/scenario.json").read_bytes())
            self.assertNotEqual((Path(a) / "series/SERIES.md").read_bytes(),
                                (Path(b) / "series/SERIES.md").read_bytes())

    def test_active_episode_has_accepted_predecessors_and_undispatched_successors(self):
        from scripts.make_head_fixtures import build_scenario
        for stage in range(1, 5):
            data = build_scenario("ready", stage)
            for issue in data["issues"]:
                if issue["stage"] < stage:
                    self.assertEqual(issue["status"], "done")
                elif issue["stage"] > stage:
                    self.assertEqual(issue["status"], "backlog")
                    self.assertEqual(issue["linked_pull_requests"], [])

    def test_submission_link_failure_is_owned_by_worker(self):
        from scripts.make_head_fixtures import build_scenario
        data = build_scenario("missing-pr-link", 1)
        self.assertEqual(data["issues"][0]["status"], "in_progress")
        self.assertEqual(data["issues"][0]["assignee_id"], "test-artist")

    def test_parent_case_supplies_real_parent_scope_and_identity(self):
        from scripts.make_head_fixtures import build_scenario
        data = build_scenario("parent-index", 2)
        self.assertIn("parent_issue", data)
        parent = data["parent_issue"]
        self.assertIn("## Doneness", parent["description"])
        self.assertEqual(parent["metadata"]["original_assignee_id"], "test-head")
        self.assertEqual(parent["metadata"]["branch"], parent["identifier"])
        self.assertEqual(data["actor"], "head")

    def test_test_directory_and_actor_are_explicit(self):
        from scripts.make_head_fixtures import build_scenario
        data = build_scenario("return", 3)
        self.assertIn("test_agent_directory", data)
        self.assertEqual(data["test_agent_directory"]["writer"]["id"], "test-writer")
        self.assertEqual(data["actor"], "writer")

    def test_artist_marker_case_uses_own_external_state_without_fake_prerequisite(self):
        from scripts.make_head_fixtures import build_scenario
        data = build_scenario("legacy-marker", 1)
        self.assertEqual(data["issues"][0]["status"], "in_progress")
        self.assertEqual(data["issues"][0]["metadata"]["prerequisite_issue_ids"], [])
        self.assertTrue(data["runtime"]["upstream_on_main"])

    def test_oracle_is_separate_from_agent_observations(self):
        with tempfile.TemporaryDirectory() as temp:
            result = self.run_generator(Path(temp), "submission")
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((Path(temp) / "test-data/scenario.json").read_text())
            self.assertNotIn("expected_action", data)
            self.assertTrue((Path(temp) / "operator-only/expected.md").is_file())

    def test_stage_one_cannot_have_cancelled_predecessor(self):
        with tempfile.TemporaryDirectory() as temp:
            result = self.run_generator(Path(temp), "cancelled-prerequisite", "--stage", "1")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(Path(temp).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
