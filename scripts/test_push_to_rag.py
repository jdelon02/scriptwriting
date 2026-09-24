"""Verify OKF ingestion, credential isolation, and restart safety without live services."""
import importlib.util
import json
from pathlib import Path
import subprocess
import shutil
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).with_name('push_to_rag.py')


class RagTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.exists(), 'The ingestion script must exist')
        spec = importlib.util.spec_from_file_location('push_to_rag', SCRIPT)
        self.rag = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.rag)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)

    def test_env_is_data_and_vector_stores_is_a_json_list(self):
        env = self.repo / '.env'
        env.write_text('primary_vector_store_id="vs-demo"\nvector_stores=\'["vs-demo","vs-two"]\'\nother=$(touch SHOULD_NOT_EXIST)\n')
        config = self.rag.read_env(env)
        self.assertEqual(config['primary_vector_store_id'], 'vs-demo')
        self.assertEqual(json.loads(config['vector_stores']), ['vs-demo', 'vs-two'])
        self.assertFalse((self.repo / 'SHOULD_NOT_EXIST').exists())

    def test_chunking_preserves_text_and_ignores_headings_in_fences(self):
        text = '# Title\n\n## First\n```md\n## example\n```\ntext\n## Second\nend\n'
        chunks = self.rag.chunk_text(text, 300)
        self.assertEqual(''.join(c['content'] for c in chunks), text)
        self.assertEqual([c['section'] for c in chunks], ['Title', 'First', 'Second'])
        long = '世界 long text\n' * 100
        chunks = self.rag.chunk_text(long, 100)
        self.assertEqual(''.join(c['content'] for c in chunks), long)
        self.assertTrue(all(len(c['content']) <= 100 for c in chunks))

    def test_embeddings_are_reordered_and_bad_dimensions_rejected(self):
        response = {'data': [{'index': 1, 'embedding': [2.0] * 1536},
                             {'index': 0, 'embedding': [1.0] * 1536}]}
        self.assertEqual(self.rag.embedding_vectors(response, 2)[0][0], 1.0)
        with self.assertRaises(ValueError):
            self.rag.embedding_vectors({'data': [{'index': 0, 'embedding': [1.0]}]}, 1)
        with self.assertRaises(ValueError):
            self.rag.embedding_vectors({'data': [{'index': 0, 'embedding': [float('nan')] * 1536}]}, 1)

    def test_large_section_prefers_paragraph_boundary(self):
        text = 'a' * 60 + '\n\n' + 'b' * 30 + '\n' + 'c' * 40
        chunks = self.rag.chunk_text(text, 100)
        self.assertEqual(chunks[0]['content'], 'a' * 60 + '\n\n')
        self.assertEqual(''.join(c['content'] for c in chunks), text)

    def test_credentials_read_from_hermes_and_vector_key_can_differ(self):
        config = self.repo / 'config.yaml'
        config.write_text('model:\n  base_url: https://proxy.example/v1\n  api_key: proxy-secret\n')
        urls = self.rag.connection_settings({'rag_base_url': 'https://vectors.example',
                                             'rag_api_key': 'store-secret'}, config)
        self.assertEqual(urls, ('https://proxy.example/v1', 'proxy-secret',
                                'https://vectors.example', 'store-secret'))

    def test_hermes_environment_reference_and_missing_key(self):
        config = self.repo / 'config.yaml'
        config.write_text('model:\n  base_url: https://proxy.example/v1\n  api_key: ${RAG_TEST_KEY}\n')
        with patch.dict('os.environ', {'RAG_TEST_KEY': 'secret-value'}):
            values = self.rag.connection_settings({'rag_base_url': 'https://vectors.example'}, config)
            self.assertEqual(values[1], 'secret-value')
            self.assertEqual(values[3], 'secret-value')
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaisesRegex(ValueError, 'unset'):
                self.rag.connection_settings({'rag_base_url': 'https://vectors.example'}, config)

    def test_invalid_credential_is_not_echoed_in_error(self):
        secret = 'secret-do-not-print\n'
        with self.assertRaises(ValueError) as raised:
            self.rag.post_json('https://example.invalid', secret, {})
        self.assertNotIn('secret-do-not-print', str(raised.exception))

    def test_real_okf_body_is_ingested_not_index_summaries(self):
        bundle = self.repo / 'docs/knowledge'
        bundle.mkdir(parents=True)
        (bundle / 'example.md').write_text('---\ntype: reference\ntitle: Example\ndescription: A document.\ntags: [test]\n---\n# Example\n\nUnique body text.\n')
        subprocess.run(['okf', 'index', str(bundle)], check=True, capture_output=True)
        chunks = self.rag.collect_chunks(self.repo, 3000)
        self.assertEqual(len(chunks), 1)
        self.assertIn('Unique body text.', chunks[0]['content'])
        self.assertEqual(chunks[0]['metadata']['concept_id'], 'example')
        self.assertEqual(chunks[0]['metadata']['filename'], 'example.md')

    def upload(self, post):
        chunks = [{'content': 'Hello', 'metadata': {'chunk_id': 'chunk-a', 'concept_id': 'doc'}}]
        return self.rag.upload_chunks(chunks, self.repo / 'state.json', 'https://proxy/v1',
                                     'proxy-key', 'https://store', 'store-key', 'vs-a', post=post)

    def test_confirmed_upload_is_skipped_on_second_run(self):
        calls = []
        def post(url, key, body):
            calls.append((url, key, body))
            if url.endswith('/embeddings'):
                return {'data': [{'index': 0, 'embedding': [0.5] * 1536}]}
            return {'data': [{'id': 'saved-id'}]}
        self.assertEqual(self.upload(post), 1)
        self.assertEqual(self.upload(post), 0)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][2]['model'], 'embedding-model')
        self.assertEqual(calls[1][0], 'https://store/v1/vector_stores/vs-a/embeddings/batch')
        self.assertEqual(calls[1][1], 'store-key')
        self.assertEqual(calls[1][2]['embeddings'][0]['content'], 'Hello')
        self.assertNotIn('key', (self.repo / 'state.json').read_text())

    def test_ambiguous_upload_blocks_automatic_retry(self):
        def post(url, key, body):
            if url.endswith('/embeddings'):
                return {'data': [{'index': 0, 'embedding': [0.5] * 1536}]}
            raise TimeoutError('test timeout')
        with self.assertRaises(TimeoutError):
            self.upload(post)
        with self.assertRaisesRegex(ValueError, 'unconfirmed'):
            self.upload(post)

    def test_empty_store_hook_skips_without_credentials_or_network(self):
        (self.repo / '.env').write_text('primary_vector_store_id=\nvector_stores=[]\n')
        result = subprocess.run(['python3', str(SCRIPT), '--repo', str(self.repo), '--hook'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('skipped', result.stdout)

    def test_hook_rejects_unstaged_markdown_before_upload(self):
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)
        subprocess.run(['git', '-C', str(self.repo), '-c', 'user.name=Test', '-c',
                        'user.email=test@example.invalid', '-c', 'core.hooksPath=/dev/null',
                        'commit', '--allow-empty', '-qm', 'fixture'], check=True)
        (self.repo / '.env').write_text('primary_vector_store_id=vs-test\n')
        (self.repo / 'draft.md').write_text('Unstaged document')
        result = subprocess.run(['python3', str(SCRIPT), '--repo', str(self.repo), '--hook'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Stage or stash Markdown', result.stderr)
        self.assertFalse((self.repo / '.rag').exists())

    def test_hook_refresh_stages_indexes_without_staging_unrelated_changes(self):
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)
        bundle = self.repo / 'docs/knowledge'
        bundle.mkdir(parents=True)
        (self.repo / 'scripts').mkdir()
        shutil.copy(SCRIPT.with_name('sync_knowledge.py'), self.repo / 'scripts/sync_knowledge.py')
        (self.repo / '.gitignore').write_text('docs/knowledge/repository/\n')
        doc = '---\ntype: reference\ntitle: Example\ndescription: Example document.\ntags: [test]\n---\n# Example\n\nOriginal text.\n'
        (bundle / 'example.md').write_text(doc)
        (self.repo / 'unrelated.py').write_text('original = True\n')
        subprocess.run(['okf', 'index', str(bundle)], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(self.repo), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(self.repo), '-c', 'user.name=Test', '-c',
                        'user.email=test@example.invalid', '-c', 'core.hooksPath=/dev/null',
                        'commit', '-qm', 'fixture'], check=True)
        (bundle / 'example.md').write_text(doc.replace('title: Example', 'title: Updated'))
        new_dir = bundle / 'new'
        new_dir.mkdir()
        (new_dir / 'added.md').write_text(doc)
        subprocess.run(['git', '-C', str(self.repo), 'add', 'docs/knowledge'], check=True)
        (self.repo / 'unrelated.py').write_text('unstaged = True\n')
        self.rag.prepare_commit_bundle(self.repo)
        staged = subprocess.check_output(['git', '-C', str(self.repo), 'diff', '--cached', '--name-only'], text=True)
        self.assertIn('docs/knowledge/index.md', staged)
        self.assertIn('docs/knowledge/new/index.md', staged)
        self.assertNotIn('unrelated.py', staged)
        self.assertNotIn('repository/', staged)
        unstaged = subprocess.check_output(['git', '-C', str(self.repo), 'diff', '--name-only'], text=True)
        self.assertEqual(unstaged.strip(), 'unrelated.py')
        subprocess.run(['git', '-C', str(self.repo), '-c', 'user.name=Test', '-c',
                        'user.email=test@example.invalid', '-c', 'core.hooksPath=/dev/null',
                        'commit', '-qm', 'include refreshed indexes'], check=True)
        markdown_dirty = subprocess.check_output(['git', '-C', str(self.repo), 'status', '--porcelain', '--', '*.md'], text=True)
        self.assertEqual(markdown_dirty, '')

    def test_hook_refuses_partial_markdown_staging(self):
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)
        path = self.repo / 'draft.md'
        path.write_text('Staged version')
        subprocess.run(['git', '-C', str(self.repo), 'add', 'draft.md'], check=True)
        path.write_text('Unstaged version')
        with self.assertRaisesRegex(ValueError, 'Stage or stash Markdown'):
            self.rag.prepare_commit_bundle(self.repo)
        staged = subprocess.check_output(['git', '-C', str(self.repo), 'show', ':draft.md'], text=True)
        self.assertEqual(staged, 'Staged version')


if __name__ == '__main__':
    unittest.main()
