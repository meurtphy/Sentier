import os
import sys
from importlib import import_module
import types

# Make paibot2 importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'paibot2'))

# Stub Flask so the module can be imported without the real package
flask_stub = types.ModuleType('flask')

class _FakeApp:
    def __init__(self, *a, **k):
        pass

    def post(self, *a, **k):
        def decorator(fn):
            return fn
        return decorator

    def run(self, *a, **k):
        pass

flask_stub.Flask = _FakeApp
flask_stub.request = types.SimpleNamespace(get_json=lambda force=True: {})
flask_stub.jsonify = lambda x: x

sys.modules.setdefault('flask', flask_stub)

# Minimal BeautifulSoup stub for tests
bs4_stub = types.ModuleType('bs4')

def _fake_bs(html, parser='html.parser'):
    class _Soup:
        def __init__(self, html):
            self._html = html

        def find(self, tag, id=None):
            if tag == 'script' and id == '__NEXT_DATA__':
                start = self._html.find('{')
                end = self._html.rfind('}')
                if start != -1 and end != -1:
                    return types.SimpleNamespace(string=self._html[start:end + 1])
            return None

    return _Soup(html)

bs4_stub.BeautifulSoup = _fake_bs
sys.modules.setdefault('bs4', bs4_stub)

app = import_module('app')


def test_scrape_by_name(monkeypatch):
    html = """
    <html><head></head><body>
    <script id="__NEXT_DATA__" type="application/json">
    {"props": {"pageProps": {"entreprise": {
        "siren": "552081317",
        "siret_siege": "55208131700017",
        "denomination": "THALES",
        "activite_principale": "2611Z",
        "numero_voie": "10",
        "type_voie": "RUE",
        "libelle_voie": "DE GRENELLE",
        "code_postal": "75015",
        "libelle_commune": "PARIS"
    }}}}
    </script></body></html>
    """

    class DummyResp:
        def __init__(self, text):
            self.text = text

        def raise_for_status(self):
            pass

    def fake_get(url, params=None, timeout=10):
        return DummyResp(html)

    monkeypatch.setattr(app.requests, 'get', fake_get)
    data = app._fetch_company_info('Thales')
    assert data['siren'] == '552081317'
    assert data['siret_siege'] == '55208131700017'
    assert data['denomination'] == 'THALES'


def test_fetch_by_number(monkeypatch):
    dummy = {'etablissement': {'siret': '12345678900011'}}

    class DummyResp:
        def __init__(self, data):
            self._data = data

        def raise_for_status(self):
            pass

        def json(self):
            return self._data

    def fake_get(url, timeout=10, params=None):
        assert 'etablissements' in url
        return DummyResp(dummy)

    monkeypatch.setattr(app.requests, 'get', fake_get)
    data = app._fetch_company_info('12345678900011')
    assert data['siret'] == '12345678900011'
