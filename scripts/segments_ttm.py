# Trailing twelve months operating income by segment: FY2025 - 9M2025 + 9M2026.
import os, csv
HERE = os.path.dirname(os.path.abspath(__file__))
tot, res = 0, []
for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'segments.csv'))):
    t = float(r['op_income_fy2025']) - float(r['op_income_9m2025']) + float(r['op_income_9m2026'])
    ch9 = float(r['op_income_9m2026']) / float(r['op_income_9m2025']) - 1
    res.append((r['segment'], t, ch9)); tot += t
seg_total = sum(t for s, t, c in res if s != 'Corporate')
for s, t, c in res:
    share = f"{t/seg_total*100:.1f}% of segment profit" if s != 'Corporate' else ''
    print(f"{s:24s} TTM ${t:6.1f}m  9M change {c*100:+.1f}%  {share}")
print(f"consolidated TTM operating income ${tot:.1f}m")
with open(os.path.join(HERE, '..', 'results', 'segments_ttm.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['segment', 'ttm_op_income_m', 'nine_month_change_pct'])
    for s, t, c in res: w.writerow([s, round(t, 1), round(c * 100, 1)])
