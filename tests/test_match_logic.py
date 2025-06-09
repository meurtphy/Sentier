import os
import sys
import types

# Ensure engine directory is importable as for legacy imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'engine'))

# Stub external dependencies used by bloc_2_ou
requests_stub = types.ModuleType('requests')
class DummyResponse:
    def raise_for_status(self):
        pass
    def json(self):
        return []
requests_stub.get = lambda *a, **k: DummyResponse()
sys.modules.setdefault('requests', requests_stub)

geopy_stub = types.ModuleType('geopy')
distance_stub = types.ModuleType('geopy.distance')
class _Geo:
    def __init__(self, km=0):
        self.km = km

def fake_geodesic(a, b):
    return _Geo(0)

distance_stub.geodesic = fake_geodesic
geopy_stub.distance = distance_stub
sys.modules.setdefault('geopy', geopy_stub)
sys.modules.setdefault('geopy.distance', distance_stub)

from importlib import import_module
match = import_module('match')

import pytest


def test_match_success(monkeypatch):
    monkeypatch.setattr(match, 'bloc_2_zone', lambda s, c: (True, 'ok'))
    seeker = {
        'type': 'association',
        'target': ['entreprise'],
        'constraints': ['logistique'],
        'budget_needed': 0,
        'zone': 'Paris',
        'when': 'urgent'
    }
    candidate = {
        'type': 'entreprise',
        'target': ['association'],
        'engagement': ['logistique'],
        'budget_available': 0,
        'zone': 'Paris',
        'when': 'urgent'
    }
    result, _ = match.match(seeker, candidate)
    assert result == 'MATCH'


def test_match_failure_when_need_unmet(monkeypatch):
    monkeypatch.setattr(match, 'bloc_2_zone', lambda s, c: (True, 'ok'))
    seeker = {
        'type': 'association',
        'target': ['entreprise'],
        'constraints': ['financier'],
        'budget_needed': 1000,
        'zone': 'Paris',
        'when': 'urgent'
    }
    candidate = {
        'type': 'entreprise',
        'target': ['association'],
        'engagement': ['logistique'],
        'budget_available': 0,
        'zone': 'Paris',
        'when': 'urgent'
    }
    result, _ = match.match(seeker, candidate)
    assert result == 'NON'

