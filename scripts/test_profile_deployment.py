"""Regression coverage for the wrong-runtime and split-instruction incidents."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import profile_guard as guard
import deploy_multica_profiles as deploy


class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / 'script-architect'
        self.home.mkdir()
        (self.home / 'AGENTS.md').write_text('current instructions\n')
        self.receipt = {
            'role': 'architect', 'agent_id': 'architect-agent',
            'runtime_id': 'architect-runtime', 'runtime_profile_id': 'architect-profile',
            'home': str(self.home), 'executable': '/bin/script-architect',
            'workspace_id': 'workspace', 'revision': 'fixture-revision',
            'instructions': 'bootstrap', 'skill_id': 'architect-skill',
            'skill_sha256': guard.digest('current skill'),
            'files': {'AGENTS.md': guard.digest('current instructions\n')},
            'workflow_sha256': guard.digest('Workflow version: test\n'),
        }
        self.agent = {'id': 'architect-agent', 'runtime_id': 'architect-runtime',
                      'instructions': 'bootstrap', 'archived_at': None,
                      'custom_args': [], 'runtime_config': {},
                      'skills': [{'id': 'architect-skill', 'name': 'script-architect', 'enabled': True}]}
        self.runtime = {'id': 'architect-runtime', 'profile_id': 'architect-profile', 'provider': 'hermes'}
        self.profile = {'id': 'architect-profile', 'command_name': '/usr/bin/env', 'enabled': True,
                        'fixed_args': ['HERMES_HOME=' + str(self.home), '/bin/script-architect']}

    def check(self, **kw):
        return guard.validate(self.receipt, self.agent, self.runtime, self.profile,
                              {'id': 'architect-skill', 'content': 'current skill'}, **kw)

    def test_matching_configuration_passes(self):
        self.assertEqual([], self.check())

    def test_architect_on_artist_runtime_is_rejected(self):
        self.agent['runtime_id'] = 'artist-runtime'
        self.assertTrue(any('runtime' in e for e in self.check()))

    def test_correct_runtime_id_with_wrong_home_is_rejected(self):
        self.profile['fixed_args'][0] = 'HERMES_HOME=/profiles/script-writer'
        self.assertTrue(any('launch' in e for e in self.check()))

    def test_wrong_executing_profile_is_rejected(self):
        self.assertTrue(any('HERMES_HOME' in e for e in self.check(actual_home='/profiles/script-artist')))

    def test_stale_remote_prompt_and_skill_are_rejected(self):
        self.agent['instructions'] = 'Use Phase and Pipeline'
        errors = guard.validate(self.receipt, self.agent, self.runtime, self.profile,
                                {'id': 'architect-skill', 'content': 'old skill'})
        self.assertTrue(any('instructions' in e for e in errors))
        self.assertTrue(any('skill' in e for e in errors))

    def test_missing_or_disabled_assigned_skill_is_rejected(self):
        self.agent['skills'][0]['enabled'] = False
        self.assertTrue(any('assignment' in e for e in self.check()))

    def test_installed_file_drift_is_rejected(self):
        (self.home / 'AGENTS.md').write_text('old instructions')
        self.assertTrue(any('AGENTS.md' in e for e in self.check()))

    def test_executable_changed_to_another_role_is_rejected(self):
        wrapper = Path(self.tmp.name) / 'architect-launcher'
        wrapper.write_text('exec hermes -p script-architect "$@"\n')
        self.receipt['executable'] = str(wrapper)
        self.receipt['executable_sha256'] = guard.digest(wrapper.read_text())
        self.profile['fixed_args'][1] = str(wrapper)
        self.assertEqual([], self.check())
        wrapper.write_text('exec hermes -p script-artist "$@"\n')
        self.assertTrue(any('executable' in e for e in self.check()))

    def test_pending_deployment_blocks_guard(self):
        (self.home / 'deployment.pending').write_text('incomplete')
        self.assertTrue(any('pending' in e for e in self.check()))

    def test_partial_remote_failure_keeps_every_role_blocked(self):
        channel = Path(self.tmp.name) / 'channel'
        channel.mkdir()
        (channel / 'WORKFLOW.md').write_text('Workflow version: old\n')
        plans = []
        for role in ['architect', 'artist']:
            home = Path(self.tmp.name) / ('script-' + role)
            home.mkdir(exist_ok=True)
            receipt = dict(self.receipt, role=role, home=str(home))
            plans.append({'receipt': receipt, 'files': {'profile_guard.py': 'guard', 'SKILL.md': 'skill'},
                          'agent': self.agent, 'skill': {'content': 'old'}})
        updates = []
        def remote(*args):
            if args[:2] == ('agent', 'tasks'):
                return []
            updates.append(args)
            if len(updates) == 3:
                raise ValueError('simulated remote failure')
            return {}
        with patch.object(deploy, 'cli', side_effect=remote), \
                patch.object(deploy.subprocess, 'run'), \
                patch.object(guard, 'check_live', return_value=[]):
            with self.assertRaisesRegex(ValueError, 'simulated'):
                deploy.apply(plans, channel, Path(self.tmp.name) / 'backup')
        for plan in plans:
            home = Path(plan['receipt']['home'])
            self.assertTrue((home / 'deployment.pending').exists())
            self.assertFalse((home / 'deployment.json').exists())

    def test_channel_header_allowed_but_contract_drift_rejected(self):
        channel = Path(self.tmp.name) / 'channel'
        channel.mkdir()
        workflow = channel / 'WORKFLOW.md'
        workflow.write_text('# Local integration\n\nWorkflow version: test\n')
        self.assertEqual([], self.check(channel_root=channel))
        workflow.write_text('Workflow version: old\n')
        self.assertTrue(any('WORKFLOW' in e for e in self.check(channel_root=channel)))

    def test_overriding_launch_args_is_rejected(self):
        self.agent['custom_args'] = ['-p', 'script-writer']
        self.assertTrue(any('override' in e for e in self.check()))

    def test_active_runs_prevent_deployment(self):
        with self.assertRaisesRegex(ValueError, 'active'):
            deploy.require_idle([{'status': 'running', 'id': 'run'}])
        deploy.require_idle([{'status': 'failed', 'id': 'run'}])

    def test_channel_sync_preserves_local_header(self):
        current = '# Channel integration\nLocal rules\n\nWorkflow version: old\nold rules\n'
        canonical = '# WORKFLOW\n\nWorkflow version: new\nnew rules\n'
        self.assertEqual('# Channel integration\nLocal rules\n\nWorkflow version: new\nnew rules\n',
                         deploy.sync_workflow(current, canonical))

    def test_missing_contract_marker_is_not_silently_overwritten(self):
        with self.assertRaises(ValueError):
            deploy.sync_workflow('unrelated document', 'Workflow version: new\n')

    def test_revision_changes_when_role_sources_change(self):
        self.assertNotEqual(deploy.revision({'a': 'one'}), deploy.revision({'a': 'two'}))
        self.assertEqual(deploy.revision({'a': 'one', 'b': 'two'}),
                         deploy.revision({'b': 'two', 'a': 'one'}))


if __name__ == '__main__':
    unittest.main()
