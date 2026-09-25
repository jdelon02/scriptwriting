"""Verify OKF ingestion, credential isolation, and restart safety without live services."""
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import shutil
import tempfile
import unittest
from unittest.mock import Mock, patch


SCRIPT = Path(__file__).with_name('push_to_rag.py')


class RagTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.exists(), 'The ingestion script must exist')
        spec = importlib.util.spec_from_file_location('push_to_rag', SCRIPT)
        self.rag = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.rag)
        self.rag.MODEL = 'embedding-model'
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)

    def test_env_is_data_and_vector_stores_is_a_json_list(self):
        env = self.repo / '.env'
        env.write_text('primary_vector_store_name="Demo"\nvector_stores=\'["Demo","Second"]\'\nother=$(touch SHOULD_NOT_EXIST)\n')
        config = self.rag.read_env(env)
        self.assertEqual(config['primary_vector_store_name'], 'Demo')
        self.assertEqual(json.loads(config['vector_stores']), ['Demo', 'Second'])
        self.assertFalse((self.repo / 'SHOULD_NOT_EXIST').exists())

    def test_store_name_resolves_exactly_to_server_id(self):
        def get(url, key):
            self.assertEqual(url, 'https://store/v1/vector_stores?limit=100')
            self.assertEqual(key, 'store-key')
            return {'data': [
                {'id': 'other', 'name': 'delongpa_channel_archive'},
                {'id': '79ac5af9-8471-4aeb-8f0e-bc415185418c', 'name': 'delongpa_channel'}],
                'has_more': False}
        result = self.rag.resolve_store_name('https://store/v1', 'store-key', 'delongpa_channel', get=get)
        self.assertEqual(result, '79ac5af9-8471-4aeb-8f0e-bc415185418c')

    def test_name_lookup_rejects_missing_ambiguous_or_incomplete_listing(self):
        cases = [
            ({'data': [], 'has_more': False}, 'not found'),
            ({'data': [{'id': 'a', 'name': 'Demo'}, {'id': 'b', 'name': 'Demo'}], 'has_more': False}, 'ambiguous'),
            ({'data': [{'id': 'a', 'name': 'Demo'}], 'has_more': True}, 'incomplete'),
        ]
        for payload, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    self.rag.resolve_store_name('https://store', 'key', 'Demo', get=lambda url, key: payload)

    def test_main_uploads_to_resolved_id_and_keeps_id_based_state(self):
        (self.repo / '.env').write_text('primary_vector_store_name=Demo\nvector_stores=\'["Demo"]\'\n')
        settings = ('https://proxy/v1', 'key', 'https://store', 'key')
        with patch.dict('os.environ', {}, clear=True), \
                patch.object(self.rag, 'connection_settings', return_value=settings), \
                patch.object(self.rag, 'resolve_store_name', return_value='resolved-id') as lookup, \
                patch.object(self.rag, 'collect_chunks', return_value=[]), \
                patch.object(self.rag, 'upload_chunks', return_value=0) as upload:
            self.assertEqual(self.rag.main(['--repo', str(self.repo), '--batch-size', '32']), 0)
        lookup.assert_called_once_with('https://store', 'key', 'Demo')
        args = upload.call_args.args
        self.assertEqual(args[-1], 'resolved-id')
        self.assertEqual(upload.call_args.kwargs['batch_size'], 32)
        expected = self.rag.digest(['https://store', 'resolved-id', 'https://proxy/v1', 'embedding-model', 1536])
        self.assertEqual(args[1].name, expected + '.json')

    def test_legacy_id_configuration_is_not_silently_treated_as_a_name(self):
        (self.repo / '.env').write_text('primary_vector_store_id=vs-old\n')
        with patch.dict('os.environ', {}, clear=True):
            self.assertEqual(self.rag.main(['--repo', str(self.repo), '--hook']), 1)

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
                                             'rag_api_key': 'store-secret', 'NANOGPT_API_KEY': 'nano-secret'}, config)
        self.assertEqual(urls, ('https://nano-gpt.com/api/v1', 'nano-secret',
                                'https://vectors.example', 'store-secret'))
        self.assertEqual(self.rag.connection_settings({'rag_base_url': 'https://vectors.example',
                         'rag_api_key': 'store-secret', 'NANOGPT_API_KEY': 'nano-secret'},
                         self.repo / 'missing.yaml'), urls)

    def test_hermes_environment_reference_and_missing_key(self):
        config = self.repo / 'config.yaml'
        config.write_text('model:\n  base_url: https://proxy.example/v1\n  api_key: ${RAG_TEST_KEY}\n')
        with patch.dict('os.environ', {'RAG_TEST_KEY': 'secret-value'}):
            values = self.rag.connection_settings({'rag_base_url': 'https://vectors.example', 'NANOGPT_API_KEY': 'nano-secret'}, config)
            self.assertEqual(values[1], 'nano-secret')
            self.assertEqual(values[3], 'secret-value')
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaisesRegex(ValueError, 'unset'):
                self.rag.connection_settings({'rag_base_url': 'https://vectors.example', 'NANOGPT_API_KEY': 'nano-secret'}, config)

    def test_nanogpt_key_is_required_without_proxy_key_fallback(self):
        with self.assertRaisesRegex(ValueError, 'NANOGPT_API_KEY'):
            self.rag.connection_settings({'rag_base_url': 'https://vectors.example',
                                          'rag_api_key': 'store-secret'}, self.repo / 'missing.yaml')

    def test_invalid_credential_is_not_echoed_in_error(self):
        secret = 'secret-do-not-print\n'
        with self.assertRaises(ValueError) as raised:
            self.rag.post_json('https://example.invalid', secret, {})
        self.assertNotIn('secret-do-not-print', str(raised.exception))

    def test_http_error_shows_response_and_redacts_request_key(self):
        secret = 'secret-do-not-print'
        response = self.rag.requests.Response()
        response.status_code = 400
        response._content = json.dumps({'error': 'Unmapped provider', 'key': secret}).encode()
        with patch.object(self.rag.requests, 'post', return_value=response):
            with self.assertRaises(ValueError) as raised:
                self.rag.post_json('https://proxy/embeddings', secret, {})
        self.assertIn('HTTP 400', str(raised.exception))
        self.assertIn('Unmapped provider', str(raised.exception))
        self.assertIn('[REDACTED]', str(raised.exception))
        self.assertNotIn(secret, str(raised.exception))

    def test_debug_shows_embedding_request_without_key(self):
        secret = 'secret-do-not-print'
        body = {'model': 'embedding-model', 'input': ['Hello']}
        output = io.StringIO()
        response = self.rag.requests.Response()
        response.status_code = 200
        response._content = b'{}'
        with patch.dict('os.environ', {'RAG_DEBUG': '1'}), patch.object(self.rag.sys, 'stderr', output), patch.object(self.rag.requests, 'post', return_value=response) as post:
            self.rag.post_json('https://proxy/embeddings', secret, body)
        post.assert_called_once_with('https://proxy/embeddings',
                                     headers={'Authorization': 'Bearer ' + secret, 'Content-Type': 'application/json'},
                                     json=body, timeout=90, allow_redirects=False)
        self.assertIn('POST https://proxy/embeddings', output.getvalue())
        self.assertIn(json.dumps(body), output.getvalue())
        self.assertIn('Authorization: Bearer [REDACTED]', output.getvalue())
        self.assertNotIn(secret, output.getvalue())

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
        self.assertEqual(calls[0][0], 'https://proxy/v1/embeddings')
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

    def test_configurable_batches_preserve_chunk_vector_alignment(self):
        chunks = [{'content': str(i), 'metadata': {'chunk_id': str(i)}} for i in range(5)]
        calls, saved = [], []
        def post(url, key, body):
            if url.endswith('/embeddings'):
                calls.append(body)
                return {'data': [{'index': i, 'embedding': [float(text)] * 1536}
                                 for i, text in reversed(list(enumerate(body['input'])))],
                        'usage': {'total_tokens': len(body['input'])}}
            saved.extend(body['embeddings'])
            return {'data': [{'id': c['metadata']['chunk_id']} for c in body['embeddings']]}
        output = io.StringIO()
        with patch.object(self.rag.sys, 'stdout', output):
            count = self.rag.upload_chunks(chunks, self.repo / 'state.json', 'https://proxy',
                                          'key', 'https://store', 'key', 'vs', post=post, batch_size=2)
        self.assertEqual(count, 5)
        self.assertEqual([b['input'] for b in calls], [['0', '1'], ['2', '3'], ['4']])
        self.assertTrue(all(b['encoding_format'] == 'float' for b in calls))
        self.assertEqual([c['embedding'][0] for c in saved], [0., 1., 2., 3., 4.])
        self.assertIn('Embedding batch 3/3', output.getvalue())
        self.assertIn('total_tokens=1', output.getvalue())

    def test_embedding_retries_are_bounded_and_do_not_retry_bad_requests(self):
        for status, attempts in [(429, 4), (500, 4), (400, 1), (401, 1)]:
            with self.subTest(status=status), patch.object(self.rag.time, 'sleep') as sleep:
                failure = self.rag.APIHTTPError(status, 'test error')
                post = Mock(side_effect=failure)
                with self.assertRaises(self.rag.APIHTTPError):
                    self.rag.embed_batch(['hello'], 'https://proxy', 'key', post=post)
                self.assertEqual(post.call_count, attempts)
                self.assertEqual(sleep.call_count, attempts - 1)

    def test_embedding_retry_can_recover_without_repeating_insert(self):
        post = Mock(side_effect=[self.rag.APIHTTPError(429, 'rate limited'),
                                {'data': [{'index': 0, 'embedding': [0.5] * 1536}]},
                                {'data': [{'id': 'saved'}]}])
        with patch.object(self.rag.time, 'sleep'):
            self.assertEqual(self.upload(post), 1)
        self.assertEqual(post.call_count, 3)
        self.assertEqual(post.call_args_list[0], post.call_args_list[1])
        self.assertNotIn('pending', json.loads((self.repo / 'state.json').read_text()))

    def test_insert_http_failure_is_not_retried(self):
        post = Mock(side_effect=[{'data': [{'index': 0, 'embedding': [0.5] * 1536}]},
                                self.rag.APIHTTPError(500, 'insert outcome unknown')])
        with patch.object(self.rag.time, 'sleep') as sleep:
            with self.assertRaises(self.rag.APIHTTPError):
                self.upload(post)
            with self.assertRaisesRegex(ValueError, 'unconfirmed'):
                self.upload(post)
        self.assertEqual(post.call_count, 2)
        sleep.assert_not_called()

    def test_batch_size_validation_precedes_network(self):
        (self.repo / '.env').write_text('primary_vector_store_name=Demo\nrag_batch_size=0\n')
        with patch.dict('os.environ', {}, clear=True), patch.object(self.rag, 'connection_settings') as settings:
            self.assertEqual(self.rag.main(['--repo', str(self.repo)]), 1)
            settings.assert_not_called()

    def test_empty_store_hook_skips_without_credentials_or_network(self):
        (self.repo / '.env').write_text('primary_vector_store_name=\nvector_stores=[]\n')
        result = subprocess.run(['python3', str(SCRIPT), '--repo', str(self.repo), '--hook'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('skipped', result.stdout)

    def test_hook_rejects_unstaged_markdown_before_upload(self):
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)
        subprocess.run(['git', '-C', str(self.repo), '-c', 'user.name=Test', '-c',
                        'user.email=test@example.invalid', '-c', 'core.hooksPath=/dev/null',
                        'commit', '--allow-empty', '-qm', 'fixture'], check=True)
        (self.repo / '.env').write_text('primary_vector_store_name=Test\n')
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
