"""Check the published lightweight example's artifact and numeric index contracts."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'examples/bank-term-deposit-marketing'

def test_public_asset_index_has_verified_distinct_deliverables():
    d = json.loads((ROOT / 'assets.json').read_text(encoding='utf-8'))
    artifacts = {Path(a['name']).suffix: a for a in d['assets'] if Path(a['name']).suffix in {'.mp4', '.pdf', '.zip'}}
    assert set(artifacts) == {'.mp4', '.pdf', '.zip'}
    assert artifacts['.mp4']['sha256'] == 'f522ae7366868e641c9b08fefd0a3353f7ef1a8a1398f1b399fe903e0cf8c55d'
    assert artifacts['.mp4']['bytes'] == 14533990
    assert artifacts['.pdf']['bytes'] == 640851 and d['pdf_pages'] == 30
    assert d['voice'] == 'ivan-advanced' and d['speech_model'] == 'Eleven v4 standard'
    for item in d['assets']:
        assert item['url'].startswith(d['release_url'].replace('/tag/', '/download/') + '/')
        assert item['url'].endswith('/' + item['name'])
        assert len(item['sha256']) == 64 and item['bytes'] > 0
    assert d['verification']['public_download_HTTP'] == 200
    assert not d['native_invocation_verified'] and not d['human_listening_verified']

def test_focal_index_preserves_observed_counts_units_and_all_information_sets():
    with (ROOT / 'focal-policy.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 6
    assert {(r['information_set'], r['procedure']) for r in rows} == {(i, p) for i in ['S0', 'S1', 'S2'] for p in ['random', 'ordered']}
    for r in rows:
        assert int(r['selected_records']) == 1647
        assert abs(float(r['observed_subscription_fraction']) - int(r['observed_subscriptions']) / int(r['selected_records'])) < 1e-12
    focal = {r['procedure']: int(r['observed_subscriptions']) for r in rows if r['information_set'] == 'S0'}
    assert focal == {'random': 1021, 'ordered': 1019}
