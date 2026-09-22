"""Check generated pages, local links, fragment targets, and social metadata."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent.parent / 'dist'
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids, self.headings, self.titles, self.images = [], set(), 0, 0, []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'Duplicate id: {a["id"]}'
            self.ids.add(a['id'])
        if tag == 'h1': self.headings += 1
        if tag == 'title': self.titles += 1
        if tag == 'img': assert 'alt' in a, 'Image without alt text'
        for attr in ['href', 'src']:
            if attr in a: self.links.append(a[attr])
        if tag == 'meta' and a.get('property') == 'og:image':
            self.images.append(a['content'])

docs = {p: Document(p.read_text()) for p in ROOT.glob('*.html')}
for path, doc in docs.items():
    assert doc.headings == 1 and doc.titles == 1, f'{path.name}: expected one heading and title'
    for link in doc.links:
        url = urlsplit(link)
        if url.scheme or url.netloc: continue
        local = unquote(url.path).removeprefix('/time-echo-website/')
        target = path if not local else ROOT / local
        if target.is_dir(): target /= 'index.html'
        assert target.exists(), f'{path.name}: missing {link}'
        if url.fragment and target.suffix == '.html':
            assert unquote(url.fragment) in docs[target].ids, f'{path.name}: missing fragment {link}'
    for image in doc.images:
        assert (ROOT / image.split('/time-echo-website/')[-1]).is_file(), 'Missing social image'
assert 'IN PREPARATION' in (ROOT / 'changelog.html').read_text()
assert 'Coming soon' in (ROOT / 'index.html').read_text()
print(f'Passed: {len(docs)} pages, internal links, fragments, metadata, release status.')
