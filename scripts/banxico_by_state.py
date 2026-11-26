# Remittances to Mexico by US state of origin, Q3 2026 vs Q3 2025 (Banxico SIE table CE168), for the
# states that hold the ten metros in my Ria agent sample.
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'banxico_us_state_q3.csv'))):
    a, b = float(r['q3_2026_usd_m']), float(r['q3_2025_usd_m'])
    print(f"{r['state']:<11} ${a:>9,.1f}m vs ${b:>9,.1f}m  {a/b*100-100:+.1f}%  {r['tracker_metros']}")
# the four falling states together vs the three growing ones
import csv as _c
R = {x['state']: (float(x['q3_2026_usd_m']), float(x['q3_2025_usd_m'])) for x in _c.DictReader(open(os.path.join(HERE, '..', 'data', 'banxico_us_state_q3.csv')))}
for name, grp in (('Arizona+Florida+Texas+Georgia', ['Arizona', 'Florida', 'Texas', 'Georgia']), ('California+Illinois+New York', ['California', 'Illinois', 'New York'])):
    a = sum(R[s][0] for s in grp); b = sum(R[s][1] for s in grp)
    print(f"{name}: ${a:,.1f}m vs ${b:,.1f}m ({a/b*100-100:+.1f}%), {a/R['Total'][0]*100:.1f}% of Q3 2026 US-to-Mexico")
