# this_file: tests_docs/test_site.py
"""Check the actual generated payload, routes and public source boundaries."""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'
PREFIX = '/fontlab-python-plugmix/'
PAGES = ['index.html', 'installation/index.html', 'app-menu-scripts/index.html', 'compatibility-package/index.html', 'development-and-limits/index.html', 'licence/index.html']


NEW_PLUGINS = {
    'round-outline-to-grid': ('filters/RoundOutlineToGrid.fontlabFilter', 'Round Outline to Grid'),
    'move-outlines': ('filters/MoveOutlines.fontlabFilter', 'Move Outlines'),
    'scale-outlines': ('filters/ScaleOutlines.fontlabFilter', 'Scale Outlines'),
    'slant-outlines': ('filters/SlantOutlines.fontlabFilter', 'Slant Outlines'),
    'measurement-ruler': ('tools/MeasurementRuler.fontlabTool', 'Measurement Ruler'),
    'node-probe': ('tools/NodeProbe.fontlabTool', 'Node Probe'),
    'contour-picker': ('tools/ContourPicker.fontlabTool', 'Contour Picker'),
}
PAGES += [f'plugins/{slug}/index.html' for slug in NEW_PLUGINS]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.ids = set()
        self.links = []
        self.text = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for name in ('href', 'src'):
            if name in attrs:
                self.links.append(attrs[name])

    def handle_data(self, data):
        self.text.append(data)


class SiteTests(unittest.TestCase):
    def test_all_generated_internal_links_and_fragments_resolve(self):
        for path in SITE.rglob('*.html'):
            for link in Page(path.read_text()).links:
                url = urlsplit(link)
                if url.scheme or url.netloc:
                    continue
                target = unquote(url.path)
                if target.startswith('/'):
                    self.assertTrue(target.startswith(PREFIX), (path, link))
                    dest = SITE / target.removeprefix(PREFIX)
                else:
                    dest = path.parent / target if target else path
                if dest.is_dir():
                    dest = dest / 'index.html'
                self.assertTrue(dest.is_file(), (path, link, dest))
                self.assertTrue(dest.resolve().is_relative_to(SITE.resolve()), link)
                if url.fragment and dest.suffix == '.html':
                    self.assertIn(unquote(url.fragment), Page(dest.read_text()).ids, (path, link))

    def test_pages_have_light_menu_footer_local_search_and_correct_canonical(self):
        for route in PAGES:
            page = Page((SITE / route).read_text())
            with self.subTest(route=route):
                self.assertEqual([attrs.get('mode') for tag, attrs in page.tags if tag == 'fontlab-menu'], ['light'])
                self.assertEqual([attrs.get('mode') for tag, attrs in page.tags if tag == 'fontlab-footer'], ['light'])
                self.assertEqual([attrs.get('data-md-color-scheme') for tag, attrs in page.tags if tag == 'body'], ['default'])
                search = [attrs for tag, attrs in page.tags if attrs.get('data-md-component') == 'search-query']
                self.assertEqual(len(search), 1)
                self.assertFalse(any(attrs.get('data-md-component') == 'palette' for _, attrs in page.tags))
                canonical = [attrs['href'] for tag, attrs in page.tags if attrs.get('rel') == 'canonical']
                self.assertEqual(canonical, ['https://fontlabcom.github.io/fontlab-python-plugmix/' + route.removesuffix('index.html')])

    def test_search_indexes_every_authored_page(self):
        search = json.loads((SITE / 'search/search_index.json').read_text())
        locations = {row['location'].split('#')[0] for row in search['docs']}
        self.assertEqual(locations, {route.removesuffix('index.html') for route in PAGES})
        text = ' '.join(' '.join(Page(row['text']).text) for row in search['docs'])
        for term in ('Stem Thickness', 'Smart Select', 'fontlabapp.plugmix', 'fontlabapp.plugins', 'Extensions', 'plugin.json', 'Show Reporters.py', 'View > Reporters'):
            self.assertIn(term, text)

    def test_attribution_downloads_are_exact_and_no_private_payload_is_published(self):
        for name in ('LICENSE', 'NOTICE'):
            self.assertEqual((ROOT / name).read_bytes(), (ROOT / 'src_docs/md/assets' / name).read_bytes())
            self.assertEqual((ROOT / name).read_bytes(), (SITE / 'assets' / name).read_bytes())
        self.assertTrue((SITE / '.nojekyll').is_file())
        private_markers = (b'/Users/', b'/Volumes/', b'/private/', b'ghp_', b'github_pat_', b'-----BEGIN PRIVATE KEY-----')
        sources = [path.read_bytes() for folder in ('src', 'Scripts', 'Extensions', 'glyphs', 'examples') if (ROOT / folder).is_dir() for path in (ROOT / folder).rglob('*.py')]
        for path in SITE.rglob('*'):
            if path.is_file():
                self.assertNotIn('.DS_Store', path.parts)
                self.assertNotIn(path.suffix, ('.py', '.pyi', '.vfpy', '.whl', '.zip'))
                payload = path.read_bytes()
                for marker in private_markers:
                    self.assertFalse(marker in payload, (path, marker))
                for source in sources:
                    if len(source) > 80:
                        self.assertFalse(source in payload, path)

    def test_workflow_builds_every_main_push_and_requalifies_immutable_output(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/docs.yml').read_text())
        events = workflow.get('on', workflow.get(True))
        self.assertEqual(events['push'], {'branches': ['main']})
        self.assertNotIn('concurrency', workflow)
        build = workflow['jobs']['build']
        verify = workflow['jobs']['qualify-generated-output']
        self.assertNotIn('concurrency', build)
        self.assertEqual(verify['needs'], 'build')
        self.assertEqual(build['outputs']['epoch'], '${{ steps.epoch.outputs.value }}')
        for job, epoch in ((build, '${{ steps.epoch.outputs.value }}'), (verify, '${{ needs.build.outputs.epoch }}')):
            build_step = next(s for s in job['steps'] if s.get('run') == 'sh src_docs/build.sh')
            self.assertEqual(build_step['env']['SOURCE_DATE_EPOCH'], epoch)
        self.assertEqual(verify['steps'][0]['with']['ref'], '${{ needs.build.outputs.sha }}')
        self.assertEqual(verify['permissions'], {'contents': 'read'})
        for job in (build, verify):
            runs = '\n'.join(step.get('run', '') for step in job['steps'])
            self.assertIn('sh src_docs/build.sh', runs)
            self.assertIn('--require-hashes -r src_docs/requirements.txt', runs)
        self.assertIn('git diff --exit-code HEAD -- docs', '\n'.join(s.get('run', '') for s in verify['steps']))
        self.assertIn('git ls-files --others -- docs', '\n'.join(s.get('run', '') for s in verify['steps']))
        self.assertFalse(any('publish.sh' in s.get('run', '') for s in verify['steps']))

    def test_private_pages_hold_removes_automatic_request_and_permission(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/docs.yml').read_text())
        self.assertNotIn('pages', workflow['permissions'])
        for name, job in workflow['jobs'].items():
            with self.subTest(job=name):
                self.assertNotIn('pages', job['permissions'])
                commands = '\n'.join(step.get('run', '') for step in job['steps'])
                self.assertNotIn('request-pages.sh', commands)
                self.assertNotIn('/pages/builds', commands)

    def test_both_complete_reporter_catalogues_and_show_reporters_action_are_present(self):
        app = ' '.join(Page((SITE / 'app-menu-scripts/index.html').read_text()).text)
        bundles = sorted((ROOT / 'Extensions/reporters').glob('*.fontlabReporter'))
        self.assertEqual(len(bundles), 39)
        for bundle in bundles:
            with self.subTest(bundle=bundle.name):
                manifest_path = bundle / 'plugin.json'
                self.assertTrue(manifest_path.is_file())
                manifest = json.loads(manifest_path.read_text())
                self.assertEqual(manifest['kind'], 'reporter')
                self.assertIn(bundle.name, app)
                self.assertIn(manifest['name'], app)
        action = 'Scripts/Plugmix/Show Reporters.py'
        self.assertTrue((ROOT / action).is_file())
        self.assertIn(action, app)
        for term in ('plugin.json', 'fontlabapp.plugins', 'Reporters palette', 'View > Reporters'):
            self.assertIn(term, app)
        self.assertIn('up to 32 other', app)
        compat = ' '.join(Page((SITE / 'compatibility-package/index.html').read_text()).text)
        table = (ROOT / 'README.md').read_text().split('### Compatibility reporters', 1)[1].split('Anchor Cloud shows', 1)[0]
        names = [row.split('|')[1].strip() for row in table.splitlines() if row.startswith('| ')][2:]
        self.assertEqual(len(names), 19)
        for name in names:
            self.assertIn(name, compat)
        for term in ('Delete Small Paths', 'Step and Repeat', 'Smart Select', 'Zoom to Selection', 'fontlab_plugmix.plugins', 'fontlabapp.plugmix'):
            self.assertIn(term, compat)

    def test_new_plugin_pages_match_manifests_and_keep_scope_limits(self):
        search = json.loads((SITE / 'search/search_index.json').read_text())
        bundles = list((ROOT / 'Extensions').glob('*/*/plugin.json'))
        self.assertEqual(len(bundles), 50)
        self.assertEqual(sum(json.loads(p.read_text())['kind'] == 'filter' for p in bundles), 5)
        self.assertEqual(sum(json.loads(p.read_text())['kind'] == 'tool' for p in bundles), 4)
        for slug, (bundle, title) in NEW_PLUGINS.items():
            with self.subTest(plugin=slug):
                manifest = json.loads((ROOT / 'Extensions' / bundle / 'plugin.json').read_text())
                self.assertEqual(manifest['name'], title)
                text = ' '.join(Page((SITE / f'plugins/{slug}/index.html').read_text()).text)
                for term in (title, bundle, manifest['id'], 'unverified'):
                    self.assertIn(term, text)
                rows = [row for row in search['docs'] if row['location'].split('#')[0] == f'plugins/{slug}/']
                self.assertTrue(rows)
                self.assertTrue(any(title in row['title'] for row in rows))
                if bundle.startswith('filters/'):
                    for term in ('components', 'anchors', 'advance', 'native curve types', 'Undo/Redo'):
                        self.assertIn(term, text)
                elif slug != 'measurement-ruler':
                    self.assertIn('12 view pixels', text)
