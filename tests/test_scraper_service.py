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

app = import_module('app')


def test_scrape_by_name(monkeypatch):
    dummy_data = {
        'unites_legales': [{
            'siren': '552081317',
            'siret_siege': '55208131700017',
            'denomination': 'THALES',
            'activite_principale': '2611Z',
            'numero_voie': '10',
            'type_voie': 'RUE',
            'libelle_voie': 'DE GRENELLE',
            'code_postal': '75015',
            'libelle_commune': 'PARIS'
        }]
    }

    class DummyResp:
        def __init__(self, data):
            self._data = data

        def raise_for_status(self):
            pass

        def json(self):
            return self._data

    def fake_get(url, params=None, timeout=10):
        assert 'unites_legales' in url
        return DummyResp(dummy_data)

    monkeypatch.setattr(app.requests, 'get', fake_get)
    data = app._fetch_company_info('Thales')
    assert data['siren'] == '552081317'
    assert data['siret_siege'] == '55208131700017'
    assert data['denomination'] == 'THALES'
