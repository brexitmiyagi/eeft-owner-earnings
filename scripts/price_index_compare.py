# Compares every run that has Ria in it, corridor by corridor: Ria bank-funded cost and rank
# against the cheapest of Western Union, Remitly, Xoom and Wise in the same run.
import csv, os
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'data', 'price_index.csv'))))
runs = sorted({r['run_utc'] for r in rows if r['provider'] == 'ria-bank'})
for run in runs:
    by = defaultdict(dict)
    for r in rows:
        if r['run_utc'] == run:
            by[r['corridor']][r['provider']] = float(r['all_in_cost_usd'])
    line = []
    for c in ('MX', 'GT', 'HN', 'SV'):
        d = by.get(c, {})
        if 'ria-bank' not in d: continue
        others = {k: v for k, v in d.items() if not k.startswith('ria')}
        best = min(others, key=others.get) if others else None
        rank = 1 + sum(v < d['ria-bank'] for v in others.values())
        line.append(f"{c} Ria ${d['ria-bank']:.2f} rank {rank}/{len(others)+1}" + (f" (best other {best} ${others[best]:.2f})" if best else ''))
    print(run, ' | '.join(line))
