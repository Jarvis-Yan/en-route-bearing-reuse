"""Recompute paired summaries from published saved results; no simulation runs."""
import csv
import hashlib
import json
import math
import random
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def percentile(values, q):
    values = sorted(values)
    i = (len(values) - 1) * q
    lo = int(i)
    hi = min(lo + 1, len(values) - 1)
    return values[lo] if hi == lo else values[lo] * (hi - i) + values[hi] * (i - lo)

def analyze(spec):
    path = ROOT / spec['file']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == spec['sha256']
    with path.open(newline='') as source:
        rows = list(csv.DictReader(source))
    assert len(rows) == spec['cases']
    assert len({r['key'] for r in rows}) == len(rows)
    groups = {seed: [] for seed in spec['seed_order']}
    gains, saved, candidates, baselines = [], [], [], []
    for row in rows:
        candidate, baseline = float(row['candidate_time']), float(row['baseline_time'])
        assert math.isfinite(candidate) and math.isfinite(baseline) and candidate > 0 and baseline > 0
        gain, saving = 100 * (1 - candidate / baseline), baseline - candidate
        assert abs(gain - float(row['gain_percent'])) < 1e-10
        assert abs(saving - float(row['time_saved_seconds'])) < 1e-10
        groups[int(row['seed'])].append(gain)
        gains.append(gain); saved.append(saving)
        candidates.append(candidate); baselines.append(baseline)
    assert all(len(g) == spec['settings_per_cluster'] for g in groups.values())
    means = [statistics.mean(groups[s]) for s in spec['seed_order']]
    rng = random.Random(spec['bootstrap_seed'])
    draws = [statistics.mean(means[rng.randrange(len(means))] for _ in means)
             for _ in range(spec['bootstrap_samples'])]
    return dict(cases=len(rows), mean_paired_gain=statistics.mean(gains),
                mean_time_saved_seconds=statistics.mean(saved), median_gain=statistics.median(gains),
                p05_gain=percentile(gains, .05), worst_gain=min(gains),
                faster_tied_slower=[sum(g > 1e-9 for g in gains), sum(abs(g) <= 1e-9 for g in gains), sum(g < -1e-9 for g in gains)],
                candidate_mean_seconds=statistics.mean(candidates), baseline_mean_seconds=statistics.mean(baselines),
                ci95=[percentile(draws, .025), percentile(draws, .975)], seed_clusters=len(means))

def close(actual, expected):
    if isinstance(actual, list):
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected): close(a, e)
    else:
        assert math.isclose(actual, expected, rel_tol=0, abs_tol=1e-9), (actual, expected)

def main():
    protocol = json.loads((ROOT / 'data/protocol.json').read_text())
    expected = json.loads((ROOT / 'analysis/expected-results.json').read_text())
    output = {}
    for name, spec in protocol.items():
        result = analyze(spec)
        for key, value in result.items(): close(value, expected[name][key])
        output[name] = result
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
