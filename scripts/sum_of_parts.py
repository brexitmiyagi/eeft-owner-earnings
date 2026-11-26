# Cross-check: each segment at a listed peer's forward EV/EBITDA.
# Segment EBITDA = TTM operating income + TTM D&A. Share comp sits in corporate, so corporate is negative.
import os, csv
HERE = os.path.dirname(os.path.abspath(__file__))
seg = {r['segment']: r for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'segments.csv')))}
da = {r['segment']: r for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'segment_da_assets.csv')))}
ev, rows = 0, []
for name in seg:
    oi = float(seg[name]['op_income_fy2025']) - float(seg[name]['op_income_9m2025']) + float(seg[name]['op_income_9m2026'])
    d = float(da[name]['da_fy2025']) - float(da[name]['da_9m2025']) + float(da[name]['da_9m2026'])
    m = float(da[name]['peer_ev_ebitda_fy1'])
    v = (oi + d) * m; ev += v
    ret = oi / float(da[name]['assets_sep2026'])
    rows.append((name, oi, d, oi + d, m, v, ret))
    print(f"{name:24s} EBITDA ${oi+d:6.1f}m x {m:4.2f} = ${v:7.0f}m | pre-tax return on segment assets {ret*100:4.1f}%")
debt, cash, atm_cash, shares = 2198.6, 955.4, 912.7, 36.737747
eq = ev - (debt - cash)
print(f"EV ${ev:,.0f}m, less net debt ${debt-cash:,.1f}m (ATM cash not netted) = equity ${eq:,.0f}m = ${eq/shares:.2f} a share")
print(f"if the ${atm_cash}m of ATM cash is netted too: ${(eq+atm_cash)/shares:.2f} a share")
with open(os.path.join(HERE, '..', 'results', 'sum_of_parts.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['segment', 'ttm_op_income', 'ttm_da', 'ttm_ebitda', 'peer_multiple', 'value_m', 'pretax_return_on_assets_pct'])
    for r in rows: w.writerow([r[0]] + [round(x, 2) for x in r[1:6]] + [round(r[6] * 100, 1)])
