"""Exercise repository discovery and generated OKF copies in isolated Git repos."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import sync_knowledge as sync


DOCUMENT = '---\ntype: reference\ntitle: Test\ndescription: Test source.\ntags: [test]\n---\n\n# Test\n\nUnique searchable body.\n'


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)
        self.bundle = self.repo / 'docs/knowledge'
        self.bundle.mkdir(parents=True)
        (self.bundle / 'curated.md').write_text(DOCUMENT)

    def write(self, name, content=DOCUMENT):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def test_discovers_sources_without_recursing_into_bundle_or_runtime(self):
        self.write('AGENTS.md')
        self.write('profiles/artist/AGENTS.md')
        self.write('templates/example.md')
        self.write('.runtime/secret.md')
        self.write('profiles/.kilo/worktree/AGENTS.md')
        self.write('ignored/cache.md')
        self.write('.gitignore', 'ignored/\n')
        found = sync.discover_sources(self.repo)
        self.assertEqual([str(p) for p in found], [
            'AGENTS.md', 'profiles/artist/AGENTS.md', 'templates/example.md'])

    def test_copies_metadata_and_body_and_refreshes_without_editing_originals(self):
        source = self.write('profiles/artist/AGENTS.md')
        sync.sync_sources(self.repo)
        copy = self.bundle / 'repository/profiles/artist/AGENTS.md'
        self.assertEqual(copy.read_bytes(), source.read_bytes())
        self.assertFalse(copy.is_symlink())
        source.write_text(DOCUMENT + '\nNew source material.\n')
        sync.sync_sources(self.repo)
        self.assertEqual(copy.read_bytes(), source.read_bytes())
        self.assertEqual((self.bundle / 'curated.md').read_text(), DOCUMENT)

    def test_removes_deleted_sources_but_keeps_unmanaged_files(self):
        source = self.write('templates/example.md')
        sync.sync_sources(self.repo)
        manual = self.bundle / 'repository/manual.md'
        manual.write_text(DOCUMENT)
        source.unlink()
        sync.sync_sources(self.repo)
        self.assertFalse((self.bundle / 'repository/templates/example.md').exists())
        self.assertEqual(manual.read_text(), DOCUMENT)

    def test_reserved_source_filenames_are_searchable_concepts(self):
        self.write('examples/index.md')
        self.write('examples/log.md')
        sync.sync_sources(self.repo)
        self.assertEqual((self.bundle / 'repository/examples/index.source.md').read_text(), DOCUMENT)
        self.assertEqual((self.bundle / 'repository/examples/log.source.md').read_text(), DOCUMENT)

    def test_missing_frontmatter_fails_before_changing_bundle(self):
        self.write('profiles/artist/AGENTS.md', '# Missing metadata\n')
        with self.assertRaisesRegex(ValueError, 'frontmatter'):
            sync.sync_sources(self.repo)
        self.assertFalse((self.bundle / 'repository').exists())

    def test_check_detects_stale_copies_without_writing(self):
        source = self.write('templates/example.md')
        sync.sync_sources(self.repo)
        self.assertEqual(sync.sync_sources(self.repo, check=True), 1)
        source.write_text(DOCUMENT + '\nChanged.\n')
        with self.assertRaisesRegex(ValueError, 'stale'):
            sync.sync_sources(self.repo, check=True)
        self.assertEqual((self.bundle / 'repository/templates/example.md').read_text(), DOCUMENT)

    def test_rejects_symlinked_output_directory(self):
        self.write('templates/example.md')
        original = self.repo / 'templates'
        (self.bundle / 'repository').symlink_to(original, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            sync.sync_sources(self.repo)
        self.assertEqual(sorted(p.name for p in original.iterdir()), ['example.md'])

    @unittest.skipUnless(shutil.which('okf'), 'OKF CLI is not installed')
    def test_real_okf_indexes_searches_and_validates_copies(self):
        self.write('profiles/artist/AGENTS.md')
        self.write('templates/example.md')
        sync.sync_sources(self.repo)
        for command in ['index', 'validate']:
            subprocess.run(['okf', command, str(self.bundle)], check=True, capture_output=True)
        result = subprocess.run(['okf', 'search', str(self.bundle), '--text', 'Unique searchable body'],
                                check=True, capture_output=True, text=True)
        ids = {row['id'] for row in json.loads(result.stdout)['results']}
        self.assertEqual(ids, {'curated', 'repository/profiles/artist/AGENTS', 'repository/templates/example'})


if __name__ == '__main__':
    unittest.main()
