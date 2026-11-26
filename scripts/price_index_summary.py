# Summarise the latest run of data/price_index.csv: where Ria's bank-funded price ranks, and the cash premium.
import csv, os, statistics
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'data', 'price_index.csv'))))
last = max(r['run_utc'] for r in rows if r['provider'].startswith('ria'))   # latest run that has Ria in it (Ria blocks cloud runs)
rows = [r for r in rows if r['run_utc'] == last]
by = {}
for r in rows: by.setdefault(r['corridor'], {})[r['provider']] = float(r['all_in_cost_usd'])
cheapest = 0; n = 0; prem = []; gaps = []
for c, d in by.items():
    if 'ria-bank' in d:
        others = {k: v for k, v in d.items() if not k.startswith('ria')}
        if others:
            n += 1
            best_other = min(others.values())
            if d['ria-bank'] <= best_other: cheapest += 1
            gaps.append(d['ria-bank'] - best_other)
    if 'ria-bank' in d and 'ria-cash' in d:
        prem.append(d['ria-cash'] - d['ria-bank'])
print(f"run {last}: Ria bank-funded is cheapest in {cheapest} of {n} corridors with a comparison")
print(f"median gap to the cheapest other provider: ${statistics.median(gaps):+.2f}")
if prem: print(f"Ria cash premium over bank-funded: median ${statistics.median(prem):.2f}, range ${min(prem):.2f} to ${max(prem):.2f}, across {len(prem)} corridors (includes the $4.00 tax)")
