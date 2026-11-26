# Weights Ria's price gap by where the money goes: the four Latin American corridors, weighted by each
# country's 2025 remittance inflows (World Bank BX.TRF.PWKR.CD.DT). Most of that money comes from the US.
import csv, os
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
W = {'MX': 65086.8, 'GT': 25675.5, 'HN': 11927.4, 'SV': 10098.9}   # $m, World Bank 2025
rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'data', 'price_index.csv'))))
run = '2026-11-26T17:31Z'
by = defaultdict(dict)
for r in rows:
    if r['run_utc'] == run: by[r['corridor']][r['provider']] = float(r['all_in_cost_usd'])
def weighted(cs):
    tot = sum(W[c] for c in cs); g = 0
    for c in cs:
        d = by[c]; others = [v for k, v in d.items() if not k.startswith('ria')]
        gap = d['ria-bank'] - min(others); g += W[c] / tot * gap
        print(f"  {c}: weight {W[c]/tot*100:.1f}%, Ria ${d['ria-bank']:.2f} vs best other ${min(others):.2f} ({gap:+.2f}, {len(others)} others)")
    return g
print("all four:"); print(f"weighted gap ${weighted(['MX','GT','HN','SV']):+.2f}")
print("without El Salvador (only Wise to compare):"); print(f"weighted gap ${weighted(['MX','GT','HN']):+.2f}")
